# Override the port if auto-detect picks the wrong device:
#   make deploy PORT=/dev/ttyACM0
PORT ?= auto
MPREMOTE := mpremote connect $(PORT)
TILEGEN := uvx --from git+https://github.com/bengosney/tileset.git tileset

SRC := $(wildcard src/*.py)
ASSETS := $(sort $(wildcard assets/*) assets/tileset.16bpp)

.PHONY: deploy run ls repl reset help

## Copy the project to the PicoSystem
deploy: $(ASSETS)
	$(MPREMOTE) fs cp $(SRC) $(ASSETS) :

## Copy the modules to the PicoSystem and run main.py without copying it
run:
	$(MPREMOTE) fs cp $(filter-out src/main.py,$(SRC)) : + run src/main.py

## List files on the PicoSystem
ls:
	$(MPREMOTE) fs ls

## Open a REPL on the PicoSystem
repl:
	$(MPREMOTE) repl

## Reboot the PicoSystem
reset:
	$(MPREMOTE) reset

## Show this help
help:
	@awk '/^## / { desc = substr($$0, 4); next } /^[a-z-]+:/ && desc { sub(/:.*/, ""); printf "%-8s %s\n", $$0, desc } { desc = "" }' $(MAKEFILE_LIST)

tileset/tileset.16bpp: tileset.toml
	$(TILEGEN) generate

assets/%: tileset/%
	@mkdir -p $(@D)
	cp $< $@

clean:
	rm -rf tileset
