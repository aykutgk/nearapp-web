import logging

from django.conf import settings
from django.views.generic.base import TemplateView


logger = logging.getLogger('django')


class registerTemplate(TemplateView):
    template_name = 'places/register.html'

    def get_context_data(self, **kwargs):
        #logger.debug(request.__dict__)
        context = super(registerTemplate, self).get_context_data(**kwargs)
        context['google_map_api_key'] = settings.GOOGLE_MAP_API_KEY
        return context
