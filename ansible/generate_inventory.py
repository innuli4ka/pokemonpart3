import json

# Load IPs from exported JSON
with open("ansible/ips.json") as f:
    ips = json.load(f)

if not isinstance(ips, list) or len(ips) != 2:
    raise ValueError(f"Expected 2 IP addresses, got: {len(ips)}")

backend_ip = ips[0]
frontend_ip = ips[1]

with open("ansible/inventory.ini", "w") as f:
    f.write(f"""[backend_servers]
{backend_ip} ansible_user=ubuntu ansible_ssh_private_key_file=/root/.ssh/vockey.pem ansible_ssh_common_args='-o StrictHostKeyChecking=no'

[frontend_servers]
{frontend_ip} ansible_user=ubuntu ansible_ssh_private_key_file=/root/.ssh/vockey.pem ansible_ssh_common_args='-o StrictHostKeyChecking=no' backend_ip={backend_ip}
""")
print("✅ Inventory file generated!")
