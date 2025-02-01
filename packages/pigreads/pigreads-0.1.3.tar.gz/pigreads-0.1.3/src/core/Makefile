FLAGS = -O3 -Wall -shared -std=c++20 -fPIC -lOpenCL $(shell python3 -m pybind11 --includes)
EXT = $(shell python3-config --extension-suffix)
SOURCE = models.hpp kernels.h
TARGETS = _core$(EXT) $(SOURCE)
PRECISION ?= float

all: $(TARGETS)

source: $(SOURCE)

_core$(EXT): %$(EXT): main.cpp geometry.h kernels.h opencl.hpp models.hpp states.h types.h
	g++ $(FLAGS) -o $@ $<

kernels.h: kernels.h.sh types.h states.h geometry.h models.hpp
	sh $< > $@

models.hpp: models.hpp.sh models $(wildcard models/*.py) $(wildcard models/*.hpp) $(wildcard models/src/*)
	make -C models
	PRECISION="${PRECISION}" sh $< > $@

clean:
	$(MAKE) -C models clean
	$(RM) $(TARGETS)
	$(RM) -r __pycache__
