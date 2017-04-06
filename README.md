# NearApp-Web
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

# Initial set up on Google Cloud (you can get $300 free trial almost for 3 months it is free)
- Web app set up
  - Spin up a new ubuntu 16.04 LTS instance (1 vCPU, 2 GB memory, 10GB SSD)
      - sudo apt-get update
  - install required python libraries
    - sudo apt-get install python3-pip
    - sudo apt-get install python3.5-venv
    - apt-get install libmysqlclient-dev

- RDS and Redis setup
  - Spin up ubuntu 16.04 LTS instance (2 Core, 7GB memory, 50GB SSD)
    - sudo apt-get update

  - Install Mysql-Server 5.7
    - sudo apt-get install mysql-server-5.7
    - put strong root password
    - comment bind address (#bind-address = 127.0.0.1) in /etc/mysql/mysql.conf.d/mysqld.cnf
    - sudo service mysql restart
    - configure firewall to access rds from home
    - create mysql user to be used from http services (django/python) do not use root
    - create mysql user to connect database externally
      - CREATE USER 'external'@'%' IDENTIFIED BY 'pass'
      - GRANT ALL PRIVILEGES ON db.* to 'external'@'%' WITH GRANT OPTION;

  - Install Redis-Server
    - sudo apt-get install build-essential tcl
    - cd
    - wget http://download.redis.io/redis-stable.tar.gz
    - tar xvzf redis-stable.tar.gz
    - cd redis-stable
    - make
    - sudo make install
    - make test
    - follow the rest of the instructions here https://redis.io/topics/quickstart)
    - django/python package for redis -> http://niwinz.github.io/django-redis/latest/

- Run Jnkins for auto deployments and cronjobs (periodic tasks)
    - follow steps here https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Ubuntu
    - open port 8001 for jenkins

- Running Gunicorn
    - used systemctl -> created new gunicorn.service under /etc/systemctl/system
    - permission to start/stop/status for jenkins user
    - trigger deployment from jenkins and sudo systemctl start gunicorn

- Geo Django Set up
  - In Django settings, add 'django.contrib.gis' to INSTALLED_APPS
  - Change mysql engine to django.contrib.gis.db.backends.mysql
  - in models.py, use "from django.contrib.gis.db import models"
  - Install GEOS
    - wget http://download.osgeo.org/geos/geos-3.6.1.tar.bz2
    - tar xjf geos-3.6.1.tar.bz2
    - cd geos-3.6.1/
    - ./configure
    - make
    - sudo make install
    - export LD_LIBRARY_PATH=/usr/local/lib
    - sudo vi /etc/environemnt and put LD_LIBRARY_PATH="/usr/local/lib"

- Switching to PostgreSQL (PostGIS) from Mysql in order to use GeoDjango Effectively
  - first install python adapter for psycopg2 -> pip install psycopg2
  - Change the engine in  database settings -> django.db.backends.postgresql
  - Set up PostgreSql server (https://www.postgresql.org/docs/9.6/static/install-short.html) (https://wiki.postgresql.org/wiki/Compile_and_Install_from_source_code)
    -  wget https://ftp.postgresql.org/pub/source/v9.6.1/postgresql-9.6.1.tar.gz
    - tar xvfz postgresql-9.6.1.tar.gz
    - cd postgresql-9.6.1
    - sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison libxml2-dev libxslt-dev libssl-dev libjson-c-dev
    - ./configure
    - make
    - sudo make install
    - sudo adduser postgres
    - sudo mkdir /usr/local/pgsql/data
    - sudo chown postgres /usr/local/pgsql/data
    - sudo su - postgres
    - /usr/local/pgsql/bin/initdb -D /usr/local/pgsql/data
    - Not suggested way to start --> /usr/local/pgsql/bin/postgres -D /usr/local/pgsql/data >logfile 2>&1 &  --> this will start the databse
    - Suggested way to start --> /usr/local/pgsql/bin/pg_ctl start -D /usr/local/pgsql/data -l postgreysql.log
    - /usr/local/pgsql/bin/createdb test
    - /usr/local/pgsql/bin/psql test
    - pg_ctl to start/stop/restart and status commands (https://www.postgresql.org/docs/9.1/static/app-pg-ctl.html)
      - /usr/local/pgsql/bin/pg_ctl restart -D /usr/local/pgsql/data -l logfile
      - /usr/local/pgsql/bin/pg_ctl status -D /usr/local/pgsql/data
    -  vi /usr/local/pgsql/data/postgresql.conf --> update the bind_address to reach from outside network. suggested to update the port number too.
    - or use ssh tunel. first connect to server and then connect to server localy

  - GEOS, PROJ.4, GDAL, GeoIp
    - Pre libs
      - sudo apt-get install binutils libproj-dev gdal-bin
      - sudo apt-get install python-gdal libgeoip1 libgeoip-dev

  - Install GEOS
    - wget http://download.osgeo.org/geos/geos-3.6.1.tar.bz2
    - tar xjf geos-3.6.1.tar.bz2
    - cd geos-3.6.1/
    - ./configure
    - make
    - sudo make install
    - sudo ldconfig

  - Install Proj4
    - wget http://download.osgeo.org/proj/proj-4.9.3.tar.gz
    - tar xzf proj-4.9.3.tar.gz
    - wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz
    - cd proj-4.9.1/nad
    - tar xzf  ../../proj-datumgrid-1.5.tar.gz
    - cd ..
    - ./configure
    - make
    - sudo make install
    - sudo ldconfig

  - Install GDAL (this installation will take time)
    - wget http://download.osgeo.org/gdal/2.1.3/gdal-2.1.3.tar.gz
    - tar xzf gdal-2.1.3.tar.gz
    - ./configure
    - make
    - sudo make install
    - sudo ldconfig

  - Install Posgris
    - wget http://download.osgeo.org/postgis/source/postgis-2.3.2.tar.gz
    - tar xvzf postgis-2.3.2.tar.gz
    - ./configure --with-pgconfig=/usr/local/pgsql/bin/pg_config
    - make
    - sudo make install
    - sudo ldconfig

  - Connected to Database
    - /usr/local/pgsql/bin/psql
    - give a password to postgrey user --> ALTER USER postgres PASSWORD '123456';
    - update config files
      - vi /usr/local/pgsql/data/postgresql.conf
        - listen_addresses = '\*'
      - vi /usr/local/pgsql/data/pg_hba.conf
        - add following line at the end of the file
        - host     db              postgres        192.168.10.1/32         password
      - restart postgressql with command below
      - /usr/local/pgsql/bin/pg_ctl restart -D /usr/local/pgsql/data -l postgreysql.log

- Sample Place data use upload_nearby script
  - first create a superuser
  - python manage.py createsuperuser
  - python upload_nearby_restaurants.py 40.6762531 -73.89776999999998 800
  - 800 meters is radius
