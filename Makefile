TS           := $(shell /bin/date "+%Y%m%d-%H%M%S")
RCB_USER     := ubuntu
RCB_HOST     := 13.48.124.39
SSH_KEY_PATH := ~/.ssh/RCB.pem

# path to tarball on local machine
TARBALL_PATH := /tmp/rcb.tar

# path to bot home on remove machine
BOT_HOME := ~/bot

##@ General
help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Build
build: ## Build service docker image.
	docker build -t rcb .
	docker tag rcb rcb:$(TS)

##@ Deploy
upload: ## Build service docker image into production.
	docker save rcb:$(TS) > $(TARBALL_PATH)
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'mkdir -p $(BOT_HOME)/sql/ $(BOT_HOME)/resources/ $(BOT_HOME)/mysql_data/  $(BOT_HOME)/logs/'
	rsync -av -e 'ssh -i $(SSH_KEY_PATH)' admin-tools $(RCB_USER)@$(RCB_HOST):$(BOT_HOME)/
	scp -i $(SSH_KEY_PATH) resources/config/prod.yml $(RCB_USER)@$(RCB_HOST):$(BOT_HOME)/resources/config.yml
	scp -i $(SSH_KEY_PATH) $(TARBALL_PATH) $(RCB_USER)@$(RCB_HOST):/tmp
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'docker load < /tmp/rcb.tar'
	scp -i $(SSH_KEY_PATH) docker-compose.yml $(RCB_USER)@$(RCB_HOST):$(BOT_HOME)/docker-compose.yml

start: ## Start service on production
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'cd $(BOT_HOME) && BOT_HOME=$(BOT_HOME) BOT_VERSION=$(TS) docker-compose up -d --force-recreate'

cleanup: ## Delete service resources after uploading into production
	rm -f $(TARBALL_PATH) || echo "$(TARBALL_PATH) does not exist"
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'rm -f $(BOT_HOME)/sql/* $(BOT_HOME)/resources/config.yml $(BOT_HOME)/docker-compose.yml /tmp/rcb.tar'
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'docker rm -f bot || echo "Bot container does not exist"'

cleanup_data: ## Clean up service MySQL data from production
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'rm -f $(BOT_HOME)/mysql_data/*'

##@ Test
lint: ## Run Python linter
	pylint src/
