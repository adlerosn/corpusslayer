help:
	@echo "help\t- Print this message"
	@echo "build\t- Downloads all 3rd party assets needed"

build: treetagger
	@echo ""
	@echo "Ready"
	@echo ""

treetagger: tree-tagger-linux.tar.gz
	-mkdir -p treetagger
	cd treetagger
	cd treetagger; tar -xf ../tree-tagger-linux.tar.gz

tree-tagger-linux.tar.gz:
	wget "http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.1.tar.gz" -O tree-tagger-linux.tar.gz
