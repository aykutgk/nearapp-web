import logging
import requests
import boto3

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext, gettext_lazy as _



logger = logging.getLogger('django')

class OwnerManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        return self._create_user(email, password, **extra_fields)



class Owner(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name = 'Email address',
        max_length = 255,
        unique = True,
    )
    phone_number = models.CharField(
        'Phone number',
        validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$')],
        max_length= 20, unique=True, null=True, blank=True, default=None
    )
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=150)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=False,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = OwnerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    class Meta:
        verbose_name = 'owner'
        verbose_name_plural = 'owners'
        permissions = (
            ("can_resend_sms_verification_code", "Can resend sms verification code"),
            ("can_resend_email_verification_code", "Can resend email verification code")
        )


    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "{0} {1}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def sms_user(self, message, **kwargs):
        """
        Not implemented yet
        """
        if self.phone_number:
            try:
                client = boto3.client(
                    'sns',
                    region_name = 'us-east-1',
                    aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
                )
                response = client.publish(PhoneNumber="+1{0}".format(self.phone_number), Message="Hi {0}, How are you?".format(self.get_short_name()))
                logger.info(response)
            except Exception as e:
                logger.error(e)
                return False
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)
