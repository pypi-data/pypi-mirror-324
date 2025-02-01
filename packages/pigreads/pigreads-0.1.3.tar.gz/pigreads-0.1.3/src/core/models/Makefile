METADATA = $(subst src/,,$(wildcard src/*.meta.yaml))
CODE = $(subst src/,,$(wildcard src/*.hpp))
MYOKIT = $(subst src/,,$(wildcard src/*.mmt))
CELLML = $(subst src/,,$(wildcard src/*.cellml))
FLOAT = $(subst src/,,$(wildcard src/*.float.yaml))
DOUBLE = $(subst src/,,$(wildcard src/*.double.yaml))
MODEL = $(subst src/,,$(wildcard src/*.model.yaml))
LINKS = $(METADATA) $(CELLML) $(MYOKIT) $(CODE) $(FLOAT) $(DOUBLE) $(MODEL)
TARGETS = $(LINKS) $(MODEL:model.yaml=float.hpp) $(MODEL:model.yaml=double.hpp) $(MODEL:model.yaml=float.yaml) $(MODEL:model.yaml=double.yaml) $(FLOAT:yaml=hpp) $(DOUBLE:yaml=hpp) $(MYOKIT:mmt=float.yaml) $(MYOKIT:mmt=double.yaml) $(CELLML:cellml=mmt) $(CELLML:cellml=float.hpp) $(CELLML:cellml=double.hpp) $(CELLML:cellml=float.yaml) $(CELLML:cellml=double.yaml)

all: $(TARGETS)

$(LINKS): %: src/%
	ln -s $< $@ || :

$(CELLML:cellml=mmt): %.mmt: %.cellml
	myokit import cellml $< $@ > /dev/null

$(MYOKIT:mmt=float.yaml) $(CELLML:cellml=float.yaml): %.float.yaml: mmt2yaml.py %.mmt %.meta.yaml
	python3 $^ float $@

$(MYOKIT:mmt=double.yaml) $(CELLML:cellml=double.yaml): %.double.yaml: mmt2yaml.py %.mmt %.meta.yaml
	python3 $^ double $@

$(MODEL:model.yaml=float.hpp) $(FLOAT:yaml=hpp) $(MYOKIT:mmt=float.hpp) $(CELLML:cellml=float.hpp): %.hpp: yaml2hpp.py %.yaml
	python3 $^ $@

$(MODEL:model.yaml=double.hpp) $(DOUBLE:yaml=hpp) $(MYOKIT:mmt=double.hpp) $(CELLML:cellml=double.hpp): %.hpp: yaml2hpp.py %.yaml
	python3 $^ $@

$(MODEL:model.yaml=double.yaml): %.double.yaml: %.model.yaml
	ln -s $< $@ || :

$(MODEL:model.yaml=float.yaml): %.float.yaml: %.model.yaml
	ln -s $< $@ || :

clean:
	$(RM) $(TARGETS)

reset:
	$(RM) *.hpp *.cellml *.mmt *.yaml
