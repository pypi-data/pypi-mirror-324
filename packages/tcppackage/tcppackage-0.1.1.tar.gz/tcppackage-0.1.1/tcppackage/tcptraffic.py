import argparse
import re
import random
import socket
import threading
from datetime import datetime
from scapy.all import sniff, TCP, IP, Raw

class MessageLog:
    @staticmethod
    def info(msg):
        current_time = datetime.now()
        log_msg = f"[ {current_time.strftime('%H:%M:%S')} INFO ] {msg}"
        print(log_msg)
    
    @staticmethod
    def error(msg):
        current_time = datetime.now()
        log_msg = f"[ {current_time.strftime('%H:%M:%S')} ERROR ] {msg}"
        print(log_msg)

def action(dst=None, src=None, target=None, listen_ip=None, listen_port=None):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_ip, int(listen_port)))
    server_socket.listen(5)
    MessageLog.info(f"Server is running on {listen_ip}@{listen_port}")
    clients = []

    def broadcast(message):
        for client in clients:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

    def packet_callback(packet, src=None, dst=None, target=None):
        if packet.haslayer(IP) and packet.haslayer(TCP):
            ip_layer = packet[IP]
            tcp_layer = packet[TCP]

            if src and ip_layer.src != src:
                return
            if dst and ip_layer.dst != dst:
                return
            if target and ip_layer.src != target and ip_layer.dst != target:
                return

            if packet.haslayer(Raw):
                data = packet[Raw].load
                broadcast(f"{ip_layer.src}@{tcp_layer.sport} > {ip_layer.dst}@{tcp_layer.dport}: {data.decode('utf-8', errors='ignore')}\n")
            else:
                broadcast(f"{ip_layer.src}@{tcp_layer.sport} > {ip_layer.dst}@{tcp_layer.dport}: (No raw data)\n")

    def sniff_traffic():
        MessageLog.info("Starting to sniff packets...")
        filter_str = "tcp"
        if src:
            filter_str += f" and src host {src}"
        if dst:
            filter_str += f" and dst host {dst}"
        if target:
            filter_str += f" and host {target}"
        sniff(filter=filter_str, prn=lambda pkt: packet_callback(pkt, src, dst, target), store=0)

    def handle_client(client_socket, client_address):
        MessageLog.info(f"New client connected: {client_address}")
        clients.append(client_socket)
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                broadcast(message)
            except:
                break
        clients.remove(client_socket)
        client_socket.close()

    # Start sniffing in a separate thread
    sniff_thread = threading.Thread(target=sniff_traffic)
    sniff_thread.daemon = True
    sniff_thread.start()

    # Server waits for client connections
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except KeyboardInterrupt:
            MessageLog.info("Server shutting down due to keyboard interrupt...")
            break

def find_random_free_port():
    while True:
        port = random.randint(1024, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                continue

def parse_and_execute_commands(commands):
    close_call_target = False
    close_call_listen = False
    target = None
    src = None
    dst = None
    listen_ip = None
    listen_port = None

    for command in commands:
        if "target=" in command:
            if close_call_target:
                MessageLog.error("You cannot specify 'target' and 'src'/'dst' together.")
                exit(1)
            match = re.search(r"target=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", command)
            if match:
                target = match.group(1)
                close_call_target = True

        elif "src=" in command:
            if close_call_target:
                MessageLog.error("You cannot specify 'src' when 'target' is already set.")
                exit(1)
            match = re.search(r"src=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", command)
            if match:
                src = match.group(1)
                MessageLog.info(f"Source: {src}")

        elif "dst=" in command:
            if close_call_target:
                MessageLog.error("You cannot specify 'dst' when 'target' is already set.")
                exit(1)
            match = re.search(r"dst=([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", command)
            if match:
                dst = match.group(1)

        elif "listen=" in command:
            match = re.search(r"listen=([^@]+)@(\d+)", command)
            if match:
                listen_ip = match.group(1)
                listen_port = int(match.group(2))
                close_call_listen = True
            else:
                MessageLog.error("Invalid listen format. Expected listen=ip@port.")
                exit(1)
        else:
            MessageLog.error("Invalid command. Expected target=, src=, dst=, or listen=.")
            exit(1)

    if not close_call_listen:
        listen_port = find_random_free_port()
        listen_ip = "127.0.0.1"
        MessageLog.info(f"Using random port: 127.0.0.1@{listen_port}")

    action(src=src, dst=dst, target=target, listen_ip=listen_ip, listen_port=listen_port)

def main():
    parser = argparse.ArgumentParser(description="TCP Traffic; TCPTRAFFIC Version 0.1.0")
    parser.add_argument("-version", action="store_true", help="TCP Traffic Version")
    parser.add_argument("-exec", type=str, help="Execution")
    args = parser.parse_args()

    if args.version:
        MessageLog.info("Rasmnout TCP Traffic; TCPTRAFFIC Version 0.1.0")

    elif args.exec:
        execution = args.exec
        commands = re.split(r",\s*", execution)
        parse_and_execute_commands(commands)
    else:
        parser.print_help()
