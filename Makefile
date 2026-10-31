# Override the port if auto-detect picks the wrong device:
#   make deploy PORT=/dev/ttyACM0
PORT ?= auto
MPREMOTE := mpremote connect $(PORT)
TILEGEN := uvx --from git+https://github.com/bengosney/tileset.git tileset

SRC := $(wildcard src/*.py)
ASSETS := $(sort $(wildcard assets/*) assets/tileset.16bpp)
DEPLOY_LOG := deploy.log

.PHONY: deploy redeploy run ls repl reset help

## Copy files changed since the last deploy to the PicoSystem
deploy: $(DEPLOY_LOG)

## Copy the whole project, for a new or wiped PicoSystem
redeploy:
	rm -f $(DEPLOY_LOG)
	$(MAKE) deploy

# The log's modified time is how make knows which files have changed
$(DEPLOY_LOG): $(SRC) $(ASSETS)
	$(MPREMOTE) fs cp $? :
	@for file in $?; do echo "$$(date '+%F %T') $$file" >> $@; done

## Deploy changed files and run main.py
run: deploy
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

tileset/tileset.16bpp: tileset.toml
	$(TILEGEN) generate

assets/%: tileset/%
	@mkdir -p $(@D)
	cp $< $@

clean:
	rm -rf tileset
