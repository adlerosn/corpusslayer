help:
	@echo "help\t- Print this message"
	@echo "apt-deps\t- Installs package dependencies in your system"
	@echo "build\t- Build plugin data"
	@echo "depends\t- Installs python dependencies through pip"
	@echo "init\t- Creates database space, if absent"
	@echo "all\t- Build plugin data, downloads pip dependencies and init database"
	@echo "deploy-ci\t- Used by Continuous Integration worker to deploy into server"
	@echo "serve\t- Starts HTTP server listening to port 14548"

build:
	for i in plugins/* ; do if [ -f "$$i/Makefile" ]; then make -C $$i ; fi ; done;

depends:
	python3 -m pip install -r requirements.txt --upgrade

init:
	python3 manage.py migrate
	python3 manage.py createcachetable
	yes yes | python3 manage.py collectstatic


all: build depends init
	@echo ""
	@echo "Done"
	@echo ""

apt-deps:
	sudo apt-get install -y build-essential
	sudo apt-get install -y python3-setuptools
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
	sudo easy_install3 pip
	sudo make depends

test:
	-rm __init__.py
	python3 manage.py templatecheck
	python3 manage.py test
	touch __init__.py

deploy-ci:
	-sudo mkdir -p /var/www/corpusslayer
	-sudo rsync -a ./ /var/www/corpusslayer/
	sudo install ./server_deploy_config/corpusslayer.service /etc/systemd/system
	sudo install ./server_deploy_config/the-corpusslayer-com-http.conf /etc/nginx/sites-available
	sudo install ./server_deploy_config/corpusslayer-com-http.conf /etc/nginx/sites-available
	sudo systemctl daemon-reload
	sudo systemctl enable corpusslayer.service
	cd /var/www/corpusslayer; chown www-data:www-data -R .
	make -C /var/www/corpusslayer all
	make -C /var/www/corpusslayer test
	cd /var/www/corpusslayer; chown www-data:www-data -R .
	sudo systemctl restart corpusslayer.service
	sudo systemctl reload nginx.service

serve:
	uwsgi --ini uwsgi.ini
