help:
	@echo "Options available"
	@echo " - help      : Prints this message"
	@echo " - clean     : Deletes all compiled data from this directory"
	@echo " - build     : Builds required data for installation"

clean:
	@echo "!!! to be implemented !!!"

build: /usr/bin/git /usr/include/tre/tre.h /usr/share/doc/build-essential/copyright UnitexTool libunitex.so lang/Latin/LICENSE
	@echo "\n"
	@echo "=========================="
	@echo "Libs and binaries prepared"
	@echo "=========================="
	@echo ""

unitex/unitex-core/LICENSE:
	-mkdir -p unitex
	cd unitex; git clone https://github.com/UnitexGramLab/unitex-core

unitex/unitex-lingua/LICENSE:
	-mkdir -p unitex
	cd unitex; git clone https://github.com/UnitexGramLab/unitex-lingua

lang/Latin/LICENSE: unitex/unitex-lingua/LICENSE
	mkdir -p lang
	cd unitex/unitex-lingua; ./install.sh ../../lang

UnitexTool: unitex/unitex-core/bin/UnitexToolLogger
	cp unitex/unitex-core/bin/UnitexToolLogger UnitexTool

libunitex.so: unitex/unitex-core/bin/libunitex.so
	cp unitex/unitex-core/bin/libunitex.so libunitex.so

unitex/unitex-core/bin/UnitexToolLogger: unitex/unitex-core/LICENSE
	cd unitex/unitex-core/build; make DEBUG=yes UNITEXTOOLLOGGERONLY=yes

unitex/unitex-core/bin/libunitex.so: unitex/unitex-core/LICENSE
	@echo "Checking if libtre-dev package is installed..."
	dpkg-query -l libtre-dev
	-cd unitex/unitex-core/build; make 64BITS=yes LIBRARY=yes
	cd unitex/unitex-core/build; g++ *.o -Wall -W -O3 -fPIC -D_NOT_UNDER_WINDOWS -DUNITEX_LIBRARY -I"../include_tre" -Ilibtre/include -I".."  -L/usr/local/lib -ltre -lpthread -shared -o ../bin/libunitex.so

/usr/include/tre/tre.h:
	@echo ""
	@echo "Checking if libtre-dev package is installed..."
	dpkg-query -l libtre-dev

/usr/share/doc/build-essential/copyright:
	@echo ""
	@echo "Checking if build-essential package is installed..."
	dpkg-query -l build-essential

/usr/bin/git:
	@echo ""
	@echo "Checking if git package is installed..."
	dpkg-query -l git
