.PHONY: ansible_shell deploy_backend deploy_frontend

create_ec2s:
	terraform -chdir=terraform init && \
	terraform -chdir=terraform plan && \
	terraform -chdir=terraform apply -auto-approve

ansible_shell:
	docker-compose run ansible /bin/sh

gen_inventory:
	cd terraform && terraform output -json instance_public_ips > ../ansible/ips.json
	python3 ansible/generate_inventory.py

deploy_backend:
	docker-compose run ansible /bin/sh -c "chmod 400 /root/.ssh/vockey.pem && ansible-playbook -i ansible/inventory.ini ansible/deploy_backend.yml --limit backend_servers"

deploy_frontend:
	docker-compose run ansible /bin/sh -c "chmod 400 /root/.ssh/vockey.pem && ansible-playbook -i ansible/inventory.ini ansible/setup_game.yml --limit frontend_servers"

