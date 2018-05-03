help:
	@echo "help\t- Print this message"
	@echo "apt-deps\t- Installs package dependencies in your system"
	@echo "build\t- Build plugin data"
	@echo "depends\t- Installs python dependencies through pip"
	@echo "init\t- Creates database space, if absent"
	@echo "all\t- Build plugin data, downloads pip dependencies and init database"
	@echo "deploy-cd\t- Used by Continuous Delivery platform to deploy this solution into the server"
	@echo "serve\t- Starts HTTP server listening to port 14548"

virtual_env:
	virtualenv -p python3 virtual_env

build: virtual_env
	. virtual_env/bin/activate; for i in plugins/* ; do if [ -f "$$i/Makefile" ]; then make -C $$i ; fi ; done;

depends: virtual_env
	. virtual_env/bin/activate; python -m pip install -r requirements.txt --upgrade

init: virtual_env
	. virtual_env/bin/activate; python manage.py migrate
	. virtual_env/bin/activate; python manage.py createcachetable
	. virtual_env/bin/activate; yes yes | python manage.py collectstatic


all: build depends init
	@echo ""
	@echo "Done"
	@echo ""

apt-update:
	sudo apt-get update

apt-deps:
	sudo apt-get install -y systemd
	sudo apt-get install -y build-essential
	sudo apt-get install -y python3-virtualenv
	sudo apt-get install -y python3-setuptools
	sudo apt-get install -y python3-pip
	sudo apt-get install -y python3-dev
	sudo apt-get install -y gettext
	sudo apt-get install -y wget
	sudo apt-get install -y curl
	sudo apt-get install -y nginx-full
	sudo apt-get install -y libtre-dev
	sudo apt-get install -y libyaml-dev
	sudo apt-get install -y libpcre3-dev
	sudo apt-get install -y openjdk-8-jdk
	sudo apt-get install -y graphviz
	sudo apt-get install -y unzip
	sudo apt-get install -y tar
	sudo apt-get install -y git
	sudo make depends

test: virtual_env
	-rm __init__.py
	. virtual_env/bin/activate; python manage.py templatecheck
	. virtual_env/bin/activate; python manage.py test
	touch __init__.py

test-ci:
	-sudo mkdir -p /var/www/corpusslayer
	-sudo rsync -a ./ /var/www/corpusslayer/
	sudo install ./server_deploy_config/corpusslayer.service /etc/systemd/system
	sudo install ./server_deploy_config/the-corpusslayer-com-http.conf /etc/nginx/sites-available
	sudo install ./server_deploy_config/corpusslayer-com-http.conf /etc/nginx/sites-available
	#sudo systemctl daemon-reload
	#sudo systemctl enable corpusslayer.service
	cd /var/www/corpusslayer; sudo chown www-data:www-data -R .
	sudo make -C /var/www/corpusslayer all
	sudo make -C /var/www/corpusslayer test
	cd /var/www/corpusslayer; sudo chown www-data:www-data -R .
	#sudo systemctl restart corpusslayer.service
	#sudo systemctl restart nginx.service

deploy-cd:
	-sudo mkdir -p /var/www/corpusslayer
	-sudo rsync -a ./ /var/www/corpusslayer/
	sudo install ./server_deploy_config/corpusslayer.service /etc/systemd/system
	sudo install ./server_deploy_config/the-corpusslayer-com-http.conf /etc/nginx/sites-available
	sudo install ./server_deploy_config/corpusslayer-com-http.conf /etc/nginx/sites-available
	sudo systemctl daemon-reload
	sudo systemctl enable corpusslayer.service
	cd /var/www/corpusslayer; sudo chown www-data:www-data -R .
	sudo make -C /var/www/corpusslayer all
	sudo make -C /var/www/corpusslayer test
	cd /var/www/corpusslayer; sudo chown www-data:www-data -R .
	sudo systemctl restart corpusslayer.service
	sudo systemctl reload nginx.service

serve: virtual_env
	. virtual_env/bin/activate; uwsgi --http :14548 --stats :14549 --stats-http --virtualenv virtual_env --module corpusslayer.wsgi --master --enable-threads --threads 64

serve-ini: virtual_env
	. virtual_env/bin/activate; uwsgi --ini uwsgi.ini

devserver: virtual_env
	. virtual_env/bin/activate; python manage.py makemigrations
	. virtual_env/bin/activate; python manage.py migrate
	. virtual_env/bin/activate; python manage.py createcachetable
	. virtual_env/bin/activate; yes yes | python manage.py collectstatic
	. virtual_env/bin/activate; python manage.py templatecheck
	. virtual_env/bin/activate; python manage.py runserver
