help:
	@echo "help\t- Print this message"
	@echo "build\t- Downloads all 3rd party assets needed"

build: mxpost treetagger brill
	@echo ""
	@echo "Done"
	@echo ""

mxpost: MACMORPHO_mxpost.zip
	unzip MACMORPHO_mxpost.zip
	mv MAC-MORPHO80-20 mxpost
	touch mxpost

treetagger: MACMORPHO_treetagger.zip
	unzip MACMORPHO_treetagger.zip
	-mkdir -p treetagger
	mv Trained80 treetagger/Trained80
	touch treetagger

brill: MACMORPHO_brill.zip
	unzip MACMORPHO_brill.zip
	touch brill

MACMORPHO_mxpost.zip:
	wget http://www.nilc.icmc.usp.br/nilc/download/mxpost-files_macmorpho.zip -O MACMORPHO_mxpost.zip

MACMORPHO_treetagger.zip:
	wget http://www.nilc.icmc.usp.br/nilc/download/treetagger-files_macmorpho.zip -O MACMORPHO_treetagger.zip

MACMORPHO_brill.zip:
	wget http://www.nilc.icmc.usp.br/nilc/download/brill-files_macmorpho.zip -O MACMORPHO_brill.zip
