# Pokémon Game Infrastructure 🐍

This project deploys a simple **Pokémon Drawer Game** on AWS EC2 using **Terraform**, **Ansible**, **Docker**, and **Docker Compose**.

---

## 📁 Project Structure

.
├── terraform/ # Terraform configs (create EC2s)
├── ansible/ # Ansible playbooks
│ ├── inventory.ini
│ ├── deploy_backend.yml
│ ├── setup_game.yml
├── pokeapi_game/
│ ├── backend-api/
│ │ ├── app.py
│ │ ├── requirements.txt
│ │ └── Dockerfile
│ └── docker-compose.yml # Backend docker-compose (Flask + MongoDB)
├── docker-compose.yml # Ansible runner container config
├── Makefile # Commands to run Ansible easily
└── README.md

yaml
Copy
Edit

---

## ✅ Requirements

- **Terraform** installed
- **Docker** & **Docker Compose** installed
- Uses **Ansible** inside Docker (via `willhallonline/ansible`)
- AWS credentials configured (`~/.aws/credentials`)
- SSH private key `vockey.pem` in `~/.ssh/vockey.pem`

---

## 🚀 Deploy in One Flow

1️⃣ **Provision AWS EC2s**

```bash
cd terraform
terraform init
terraform apply
This will create 1 backend server & 1 frontend server.

Save the public IPs output at the end.

2️⃣ Update Inventory

Edit ansible/inventory.ini:

ini
Copy
Edit
[backend_servers]
<YOUR_BACKEND_IP>

[frontend_servers]
<YOUR_FRONTEND_IP>
Replace <YOUR_BACKEND_IP> and <YOUR_FRONTEND_IP>.

3️⃣ Deploy Backend

bash
Copy
Edit
make deploy_backend
Installs Docker on backend

Builds & runs backend-api Flask app + MongoDB in Docker Compose

4️⃣ Deploy Frontend

bash
Copy
Edit
make deploy_frontend
Installs Docker & clones the game repo on frontend

Sets BACKEND_API_URL with your backend IP

Auto-runs the game when you SSH in

5️⃣ SSH to Frontend

bash
Copy
Edit
ssh -i ~/.ssh/vockey.pem ubuntu@<YOUR_FRONTEND_IP>
The game should start automatically.

✅ Makefile Example
makefile
Copy
Edit
.PHONY: ansible_shell deploy_backend deploy_frontend

ansible_shell:
	docker-compose run ansible /bin/sh

deploy_backend:
	docker-compose run ansible /bin/sh -c "chmod 600 /root/.ssh/vockey.pem && ansible-playbook -i ansible/inventory.ini ansible/deploy_backend.yml --limit backend_servers"

deploy_frontend:
	docker-compose run ansible /bin/sh -c "chmod 600 /root/.ssh/vockey.pem && ansible-playbook -i ansible/inventory.ini ansible/setup_game.yml --limit frontend_servers"
✅ Example docker-compose.yml (Backend)
yaml
Copy
Edit
version: "3.8"

services:
  mongo:
    image: mongo:latest
    container_name: mongo
    restart: always
    ports:
      - "27017:27017"

  backend-api:
    build: ./backend-api
    container_name: backend-api
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_RUN_HOST=0.0.0.0
      - FLASK_RUN_PORT=5000
    depends_on:
      - mongo
✅ Example docker-compose.yml (Root)
For Ansible:

yaml
Copy
Edit
version: "3.8"

services:
  ansible:
    image: willhallonline/ansible
    container_name: ansible_runner
    working_dir: /workspace
    volumes:
      - ./:/workspace
      - ~/.ssh/vockey.pem:/root/.ssh/vockey.pem
✅ Useful Commands
SSH into backend to check containers:

bash
Copy
Edit
ssh -i ~/.ssh/vockey.pem ubuntu@<YOUR_BACKEND_IP>
docker ps
If MongoDB isn’t running:

bash
Copy
Edit
cd pokeapi_game
docker-compose up -d --build
🗑️ Destroy
bash
Copy
Edit
cd terraform
terraform destroy
📌 Tips
Always chmod 600 your SSH key.

Double-check public IPs after Terraform apply.

Credits
Pokémon API: https://pokeapi.co

Made with  using Terraform + Ansible + Docker

