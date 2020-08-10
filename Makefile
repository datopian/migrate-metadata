# Makefile for migrate-metadata
PACKAGE_NAME := migrate-metadata
PACKAGE_DIRS := migrate_metadata
TESTS_DIR := tests

SHELL := bash
PYTHON := python
PYTEST := pytest
PIP := pip
PIP_COMPILE := pip-compile

SENTINELS := .make-cache

default: help

dev-requirements.txt: dev-requirements.in
	$(PIP_COMPILE) --no-index dev-requirements.in -o $@

requirements.txt: requirements.in
	$(PIP_COMPILE) --no-index requirements.in -o $@

## Update requirements files for the current Python version
requirements: $(SENTINELS)/requirements
.PHONY: requirements

## Run all tests
test:
	$(PYTEST) $(PACKAGE_DIRS) $(TESTS_DIR)
.PHONY: test

# --- Private Targets ---

$(SENTINELS):
	mkdir $@

$(SENTINELS)/requirements: requirements.txt dev-requirements.txt | $(SENTINELS)
	@touch $@

# --- Help related variables and targets --

GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM := 20

## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
	  helpMessage = match(lastLine, /^## (.*)/); \
	  if (helpMessage) { \
	    helpCommand = substr($$1, 0, index($$1, ":")-1); \
	    helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
	    printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
	  } \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
