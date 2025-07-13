# Pokémon Game Infrastructure 🐍

This project deploys a simple **Pokémon Drawer Game** on AWS EC2 using **Terraform**, **Ansible**, **Docker**, and **Docker Compose**.
Here is a diagram of this infrastrucure 

<img width="599" height="528" alt="image" src="https://github.com/user-attachments/assets/b92247e8-55a2-4a0c-ac6c-ae529ce6b753" />

---

## Requirements

- **Terraform** installed
- **Docker** & **Docker Compose** installed
- Uses **Ansible** inside Docker (via `willhallonline/ansible`)
- AWS credentials configured (`~/.aws/credentials`)
- SSH private key `vockey.pem` in `~/.ssh/vockey.pem`

---

##  Deploy in 3 simple steps Fow

**Provision AWS EC2s**

1. Terraform steps
cd pokemonpart3
terraform init
terraform apply
This will create 1 backend server & 1 frontend server.

Save the public IPs output at the end.

---

2. Update Inventory

Edit ansible/inventory.ini:

[backend_servers]
<YOUR_BACKEND_IP>

[frontend_servers]
<YOUR_FRONTEND_IP>
Replace <YOUR_BACKEND_IP> and <YOUR_FRONTEND_IP>.

---

3. Deploy Backend

make deploy_backend
Installs Docker on backend

Builds & runs backend-api Flask app + MongoDB in Docker Compose

---

4. Deploy Frontend

make deploy_frontend
Installs Docker & clones the game repo on frontend

Sets BACKEND_API_URL with your backend IP

Auto-runs the game when you SSH in

---

**SSH to Frontend**

When you ssh to frontend IP, The game should start automatically.

---

**Makefile**
the commands are stored in the make file
ansible_shell
deploy_backend
deploy_frontend

---

**Destroy**

cd pokemonpart3
terraform destroy

---

**Tips**
The ssh key name is vockey, therefore make sure you are saving your key in the .ssh folder wih "vockey" name

---

**Credits**
Pokémon API: https://pokeapi.co

Made by using Terraform + Ansible + Docker

