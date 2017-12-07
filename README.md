# Corpus Slayer

This is a modular and multilingual corpus processing tool built on top of DJango and Python 3.

This tool doesn't aim to be good for all purposes right out of the box, but to be extensible enough to receive a plug-in that satisfies your cravings.

You could say that this is a collection of ad-hoc command-line tools glued together with Python and JSON, and put together in an event-based architecture that produces web pages as result.

An usage scenario would be an university that offers such platform for its researchers to investigate the Literature for different construction patterns in many authors, to build better voice command devices that recognizes the user intention better than in past iterations, to build better speech-to-text converters that are shipped in smartphones that adds punctuation automatically, among many other possibilities that a better understanding of the language we use can bring.

## How to run

First run `sudo make apt-deps` to download dependencies from distribution's repository into your system.

Then run `sudo make depends` to download required python modules from PyPI repository into your system.

Then run `make all` to make migrations to the database and download extra data for the plug-ins.

Finally run `make serve`. You may now be able to access the application through the port 14548.

## License

Trying to give people as much freedom to do whatever they want to the code, the license chosen was the MIT.

Notice that the MIT license only applies to the base platform and plug-ins received as is. When running `make all`, `make build` or `make deploy-ci`, it's expected that you will download MXPOST (proprietary license), TreeTagger (proprietary license), Unitex/GramLab (GNU LGPL v2.1) and Mac-Morpho (CC-BY-4.0); where some of those are incompatible with MIT license and may impose restrictions on how you will use or redistribute the platform - you are welcomed to contribute by writing a plug-in to replace those proprietary parts.

## Translations

The software comes preloaded with two translations: Brazilian Portuguese and American English.

### Adding a language

Run `python3 manage.py makemessages -l LL_CC`, where `LL_CC` is your locale name according [DJango's documentation](https://docs.djangoproject.com/en/1.11/topics/i18n/).

### Editing language strings

- Visit the `/rosetta` endpoint in your browser
- Click a language
- Start translating

PS: This is how you edit the content of the pages “Help”, “Privacy” and “Terms”.

### Syncing with whole project

After you edit a template, it'll be required that you re-sync language strings from templates

- Run `python3 manage.py makemessages -a`
- Visit the `/rosetta` endpoint in your browser
- Translate new strings

## Server

The recommended configuration is NGINX reverse-proxying a uWSGI server powered by Python 3, this last one kept alive by systemd.

### SystemD

Just copy the file `server_deploy_config/corpusslayer.service` into `/etc/systemd/system` and adapt it to suit your needs.

Points worth your attention:
- platform absolute path (default: `/var/www/corpusslayer`)

### uWSGI

Just run `make serve` and the web server will be available in the port `14548`. Check how to automate this command at server startup in the topic immediately above.

### NGINX

Just copy the file `server_deploy_config/corpusslayer-com-http.conf` into `/etc/nginx/sites-available` and adapt it to suit your needs.

Points worth your attention:
- ACME snippet for successfully acquiring X.509 certificates from CertBot (default: `/etc/nginx/snippets/acme.conf`)
- TLS and GZIP snippet (default: `/etc/nginx/snippets/tlsgzip.conf`)
- Proxied server location (default: `the.corpusslayer.com:14548`)
- Static files location (default: `/var/www/corpusslayer/static`)
- Media files location (default: `/var/www/corpusslayer/media`)
- Server name (default: `the.corpusslayer.com`)

### Apache

It's known that Apache Web Server (2.4.18) with mod-wsgi-py3 (4.3.0) on its default configuration only handles ASCII. There's a fix in [DJango's documentation](https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/modwsgi/) ("Fixing UnicodeEncodeError for file uploads"), but we chose uWSGI because it works out of the box without any additional configuration.

The server configuration is up to you.

### Python 2.x

TL;DR: Won't run.

Python 2 wasn't targeted during the development. This is because Python 3 series is said to be the present and future of the Python language by its [official wiki](https://wiki.python.org/moin/Python2orPython3).

## Some actions

### Changing site name

Edit file at `secrets/SITE.txt` and restart the WSGI server
<br>
Default: `Corpus Slayer`

### Changing site domain

Edit file at `secrets/SITE.tld` and restart the WSGI server
<br>
Default: `the.corpusslayer.com`

### Logging everyone out

Delete file `secrets/SECRET_KEY.bin` and restart the WSGI server

### Deleting all users and all associated data

Delete file `db.sqlite3`, run `make init` and then restart the WSGI server
