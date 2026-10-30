# Override the port if auto-detect picks the wrong device:
#   make deploy PORT=/dev/ttyACM0
PORT ?= auto
MPREMOTE := mpremote connect $(PORT)

SRC := $(wildcard src/*.py)

.PHONY: deploy run ls repl reset help

## Copy the project to the PicoSystem
deploy:
	$(MPREMOTE) fs cp $(SRC) :

## Run main.py from this machine without copying it
run:
	$(MPREMOTE) run src/main.py

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
