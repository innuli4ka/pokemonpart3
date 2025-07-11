.PHONY: deploy_all terraform apply_backend apply_frontend

deploy_all: terraform backend frontend

terraform:
	terraform init
	terraform apply -auto-approve

backend:
	ssh -i ~/.ssh/vockey.pem ubuntu@$(terraform output -raw backend_ip) \
	"cd ~/pokeapi_game && docker-compose up -d --build"

frontend:
	docker-compose run ansible /bin/sh -c "chmod 600 /root/.ssh/vockey.pem && ansible-playbook -i ansible/inventory.ini ansible/setup_game.yml --limit frontend_servers"
