# NearApp-Web
Django and AngularJs

- This project will combine Django Framework, Django Rest Api, Angular Js and Angular Material technologies.
- Project initially will use django template engine and combine html/css and angular logic in html and separate the javascript from html.
- Angular part will be built by using components so that it will be easy to manage components and will be easy to migrate to Angular 2.

# Dev Environment
- There will be provisioning in Vagrantfile will handle installing required packages
- for future, there will be docker base image and dockerfile to easy spin up this project.
- Seperate db instance for mysql and redis like AWS RDS.
- Steps to setup dev Environment
  - create a new folder called vagrants
  - create a sub-folder named near-web-portal under vagrants
  - download Vagrantfile from (https://github.com/aykutgk/dev_environment_files) under near-web-portal
  - create a new folder called data under near-web-portal
  - git clone this repo under near-web-portal
  - go back to main folder where Vagrantfile is
  - run --> vagrant up
  - to get into machine for mac --> vagrant ssh
  - for windows, download puttykey generator, and convert exisitng private_key to ptty by using that tool
  - download putty, put host info and import private_key from ssh/auth on right panel.
- Steps to set up project Environment
  - create virtual python environment under home folder (run cd to go to home folder)
  - python3.5 -m venv venv_name
  - Activate the venv -> source venv_name/bin/activate
  - go to /vagrant_data
  - pip install --upgrade pip (for some wheel errors update pip version)
  - go into the project where requirements.txt exists
  - run --> pip install -r requirements.txt (this will install all required packages)
  - set up mysql server either in your local or in another vagrant instance
  - to install mysql-server --> sudo apt-get install mysql-server
  - username: root, password: 123456
  - go to project folder and open app/app/settings/dev.py
  - find DATABASE part and edit the host info. for localhost, change host to "localhost"
  - if you create seperate vagrant instance for db, dont forget to open it to public by editing bind_address in mysqld.conf to 0.0.0.0
  - and create new user and grant permissinon
  - Create user: CREATE USER 'mysql_django_user_external'@'192.168.10.1' IDENTIFIED BY '123456'; if you want to reach from eveywhere change that ip to %
  - Grant permissions: GRANT ALL PRIVILEGES ON db.* to 'mysql_django_user_external'@'192.168.10.1' WITH GRANT OPTION;
- Run Django project
  -  python manage.py runserver 0.0.0.0:8080 --settings=app.settings.dev (0.0.0.0 to reach it in your laptop from ip address in vagrantfile)
- Migrations
  - initial migration --> python manage.py migrate --settings=app.settings.dev
  - after table changes -->  python manage.py makemigrations --settings=app.settings.dev
