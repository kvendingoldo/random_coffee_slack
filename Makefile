RCB_USER=ubuntu
RCB_HOST=13.48.124.39
SSH_KEY_PATH=~/.ssh/RCB.pem
TIMESTAMP=$$(date +%Y%m%d-%H%M%S)

build:
	docker build -t rcb .
	docker tag rcb rcb:${TIMESTAMP}

cleanup:
	rm -f rcb.tar
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'rm -f ~/bot/sql/* ~/bot/sql/resources/config.yml ~/bot/docker-compose.yml /tmp/rcb.tar'
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'docker rm -f bot'

upload:
	docker save rcb:${TIMESTAMP} > rcb.tar
	scp -i $(SSH_KEY_PATH) resources/migrations/V0__create_database.sql $(RCB_USER)@$(RCB_HOST):~/bot/sql/
	scp -i $(SSH_KEY_PATH) resources/migrations/V2__create_tables.sql $(RCB_USER)@$(RCB_HOST):~/bot/sql/
	scp -i $(SSH_KEY_PATH) resources/config/prod.yml $(RCB_USER)@$(RCB_HOST):~/bot/resources/config.yml
	scp -i $(SSH_KEY_PATH) rcb.tar $(RCB_USER)@$(RCB_HOST):/tmp
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'docker load < /tmp/rcb.tar'
	scp -i $(SSH_KEY_PATH) docker-compose.yml $(RCB_USER)@$(RCB_HOST):~/bot/docker-compose.yml

start:
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'BOT_VERSION=${TIMESTAMP} docker-compose up -d -f ~/bot/docker-compose.yml'

