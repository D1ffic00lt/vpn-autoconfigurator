# import os
# import subprocess
#
# # Paths
# wg_config_path = "/path/to/your/container/config/wg0.conf"  # Path to the WireGuard server config in the other container
# peer_config_dir = "/path/to/your/container/config/peers"    # Directory to store peer config files
#
# # Peer details
# peer_name = "new_peer"
# peer_ip = "10.13.13.4"  # Assign a new IP from the VPN subnet
# server_public_key = "your_server_public_key"  # Get this from your server config
# server_endpoint = "your_server_ip_or_domain:51820"
#
# # Step 1: Generate key pair for the new peer
# def generate_keys():
#     private_key = subprocess.check_output("wg genkey", shell=True).decode('utf-8').strip()
#     public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).decode('utf-8').strip()
#     return private_key, public_key
#
# # Step 2: Add the peer to the WireGuard server configuration
# def add_peer_to_server_config(peer_public_key):
#     peer_config = f"""
# [Peer]
# PublicKey = {peer_public_key}
# AllowedIPs = {peer_ip}/32
# """
#     # Append to the server's WireGuard configuration file
#     with open(wg_config_path, 'a') as config_file:
#         config_file.write(peer_config)
#
# # Step 3: Create the peer's configuration file
# def create_peer_config(private_key):
#     peer_config = f"""
# [Interface]
# PrivateKey = {private_key}
# Address = {peer_ip}/32
# DNS = 1.1.1.1  # Adjust DNS as necessary
#
# [Peer]
# PublicKey = {server_public_key}
# Endpoint = {server_endpoint}
# AllowedIPs = 0.0.0.0/0, ::/0
# PersistentKeepalive = 25
# """
#     peer_config_path = os.path.join(peer_config_dir, f"{peer_name}.conf")
#     with open(peer_config_path, 'w') as peer_file:
#         peer_file.write(peer_config)
#     return peer_config_path
#
# # Step 4: Restart the WireGuard container (or reload configuration)
# def restart_wireguard_container():
#     # Adjust this command to restart the specific container running WireGuard
#     os.system("docker restart wireguard-container-name")
#
# # Main function
# def main():
#     # Generate keys for the new peer
#     private_key, public_key = generate_keys()
#
#     # Add the peer's public key to the server configuration
#     add_peer_to_server_config(public_key)
#
#     # Create the peer configuration file
#     peer_config_path = create_peer_config(private_key)
#     print(f"Peer configuration file created at: {peer_config_path}")
#
#     # Restart the WireGuard container to apply changes
#     restart_wireguard_container()
#     print("WireGuard container restarted.")
#
# if __name__ == "__main__":
#     main()
import sys

