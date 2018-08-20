::Install piping and virtaulenv
  $ pip install --user pipenv

  $ export PATH="$PATH:/Users/njtwentyone/Library/Python/2.7/bin"

   $ pip install requests

   [THEN ignore steps]
	virtualenv env
	source env/bin/activate
   [Instead run]
   	$ pipenv shell

to add another package do $> pipenv install {module}
to install all in popFile do $> pipenv install

python modules:
requests
django
djangorestframework
Mock
pymongo
pymongo[gssapi,srv,tls]
  (snappy faild to build)
celery

::Install django-rest api
 followed http://www.django-rest-framework.org/tutorial/quickstart/
 running on python 2.7 mac version
 using virtualenv for python depends



:: run test
python -m unittest discover -v

:: run server
python manage.py runserver 5000

Profiling:
https://julien.danjou.info/guide-to-python-profiling-cprofile-concrete-case-carbonara/

install qcachegrind:
$brew install qcachegrind --with-graphviz

install pyprof2calltree:
sudo pip install pyprof2calltree

view profiler:
1) convert on the fly
	pyprof2calltree -k -i profile_dos.cprof.H20
2)profile_dos.cprof.H20 -o profile_dos.callgrind.H2O

:: set environment variables in pipenv shell
1) have to set variables in root directory in file '.env'
  root directory is same file as 'Pipefile'
2) with current setUp
$rootDir> cat settings/settings.conf.production >> .env

:: run production server(gunicorn)
1) $project-root> pip install gunicorn
$project-root> gunicorn --bind 0.0.0.0:5000 tutorial.wsgi:application

:: install rabbitMQ
https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html
1) brew install rabbitmq/sudo apt-get install rabbitmq-server
- installed /usr/local/sbin
 -- export PATH=$PATH:/usr/local/sbin
2) start server: $>  rabbitmq-server
3) setup up stuff:
 $> rabbitmqctl add_user user01 rabbitmq01
 $> rabbitmqctl add_vhost vhost01
 $> rabbitmqctl set_permissions -p vhost01 user01 ".*" ".*" ".*"

**

 :: start celery
 $(pipenvshell) celery -A tutorial worker -l info
