help:
	@echo "help\t- Print this message"
	@echo "build\t- Downloads all 3rd party assets needed"

build: mxpost
	@echo '#!/usr/bin/env bash' > mxterminator.sh
	@echo 'export CLASSPATH=$(shell pwd)/mxpost/mxpost.jar' >> mxterminator.sh
	@echo 'java -mx100m eos.TestEOS $$1' >> mxterminator.sh
	@chmod +x mxterminator.sh
	
	@echo '#!/usr/bin/env bash' > mxpost.sh
	@echo 'export CLASSPATH=$(shell pwd)/mxpost/mxpost.jar' >> mxpost.sh
	@echo 'java -mx100m tagger.TestTagger $$1' >> mxpost.sh
	@chmod +x mxpost.sh
	
	@echo ""
	@echo "Ready"
	@echo ""

mxpost: jmx.tar.gz
	-mkdir -p mxpost
	cd mxpost
	cd mxpost; tar -xf ../jmx.tar.gz

jmx.tar.gz:
	wget ftp://ftp.cis.upenn.edu/pub/adwait/jmx/jmx.tar.gz -O jmx.tar.gz
