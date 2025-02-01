EXT = $(shell python3-config --extension-suffix)
TARGETS = pigreads/_core$(EXT) pigreads/_core_double$(EXT)

all: $(TARGETS)
	$(MAKE) -C core $@
	$(MAKE) -C core_double PRECISION=double $@

source:
	$(MAKE) -C core $@
	$(MAKE) -C core_double PRECISION=double $@

core/_core$(EXT):
	$(MAKE) -C core _core$(EXT)

core_double/_core$(EXT):
	$(MAKE) -C core_double PRECISION=double _core$(EXT)

pigreads/_core$(EXT): core/_core$(EXT)
	ln -s $(shell readlink -f $<) $@

pigreads/_core_double$(EXT): core_double/_core$(EXT)
	ln -s $(shell readlink -f $<) $@

clean:
	$(MAKE) -C core clean
	$(MAKE) -C core_double clean
	$(RM) $(TARGETS)
