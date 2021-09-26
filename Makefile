#
# Common variables
#
TS           := $(shell /bin/date "+%Y%m%d-%H%M%S")
RCB_USER     := ubuntu
RCB_HOST     := 13.48.124.39
SSH_KEY_PATH := ~/.ssh/RCB.pem

# path to tarball on local machine
TARBALL_PATH := /tmp/rcb.tar

# path to bot home on remove machine
BOT_HOME := ~/bot

info:
	@echo "The current version of image is '$(TS)'"

build:
	docker build -t rcb .
	docker tag rcb rcb:$(TS)

upload:
	docker save rcb:$(TS) > $(TARBALL_PATH)
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'mkdir -p $(BOT_HOME)/sql/ $(BOT_HOME)/resources/ $(BOT_HOME)/mysql_data/'
	scp -i $(SSH_KEY_PATH) resources/config/prod.yml $(RCB_USER)@$(RCB_HOST):$(BOT_HOME)/resources/config.yml
	scp -i $(SSH_KEY_PATH) $(TARBALL_PATH) $(RCB_USER)@$(RCB_HOST):/tmp
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'docker load < /tmp/rcb.tar'
	scp -i $(SSH_KEY_PATH) docker-compose.yml $(RCB_USER)@$(RCB_HOST):$(BOT_HOME)/docker-compose.yml

start:
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'cd $(BOT_HOME) && BOT_HOME=$(BOT_HOME) BOT_VERSION=$(TS) docker-compose up -d --force-recreate'

cleanup:
	rm -f $(TARBALL_PATH) || echo "$(TARBALL_PATH) does not exist"
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'rm -f $(BOT_HOME)/sql/* $(BOT_HOME)/resources/config.yml $(BOT_HOME)/docker-compose.yml /tmp/rcb.tar'
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'docker rm -f bot || echo "Bot container does not exist"'

cleanup_data:
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'rm -f $(BOT_HOME)/mysql_data/*'
