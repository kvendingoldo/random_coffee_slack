RCB_USER=ubuntu
RCB_HOST=13.48.124.39
SSH_KEY_PATH=~/.ssh/RCB.pem
TIMESTAMP=$$(date +%Y%m%d-%H%M%S)

build:
	docker build -t rbc .

upload:
	ssh -i $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'rm -f ~/bot/sql/*'
	scp -i $(SSH_KEY_PATH) resources/migrations/* $(RCB_USER)@$(RCB_HOST):~/bot/sql/
	docker save rcb > rcb.tar
	scp -i $(SSH_KEY_PATH) rcb.tar $(RCB_USER)@$(RCB_HOST):/tmp
	ssh -it $(SSH_KEY_PATH) $(RCB_USER)@$(RCB_HOST) 'docker load < /tmp/rcb.tar && rm /tmp/rcb.tar'
