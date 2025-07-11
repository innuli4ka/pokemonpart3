.PHONY: ansible_shell deploy_backend deploy_frontend

ansible_shell:
	docker-compose run ansible /bin/sh

deploy_backend:
	docker-compose run ansible /bin/sh -c "chmod 600 /root/.ssh/vockey.pem && ansible-playbook -i ansible/inventory.ini ansible/deploy_backend.yml --limit backend_servers"

deploy_frontend:
	docker-compose run ansible /bin/sh -c "chmod 600 /root/.ssh/vockey.pem && ansible-playbook -i ansible/inventory.ini ansible/setup_game.yml --limit frontend_servers"