import socket
import argparse
import time
import random
import threading
import ssl

# Verze skriptu
VERSION = "0.1.1"

def log(level, message, log_file=None, log_level="info"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    if log_level in ["info", "debug"] or (log_level == "error" and level == "error"):
        log_message = f"[{level.upper()} {timestamp}] {message}"
        print(log_message)
        if log_file:
            with open(log_file, "a") as f:
                f.write(log_message + "\n")

def handle_client(client_socket, address, options):
    log("info", f"New connection from {address}", options["log_file"], options["log_level"])
    client_socket.settimeout(options["timeout"])
    
    try:
        data = client_socket.recv(options["buffer_size"])
        if options["hex_dump"]:
            log("info", f"Received hex dump: {data.hex()}", options["log_file"], options["log_level"])
        else:
            try:
                decoded_data = data.decode(options["encoding"])
                log("info", f"Received data: {decoded_data}", options["log_file"], options["log_level"])
            except UnicodeDecodeError:
                log("info", f"Received raw bytes: {data}", options["log_file"], options["log_level"])
                
        if options["save_data"]:
            with open(options["save_data"], "ab") as f:
                f.write(data)
                log("info", f"Saved received data to {options['save_data']}", options["log_file"], options["log_level"])
        
        if options["response"]:
            client_socket.sendall(options["response"].encode(options["encoding"]))
            log("info", f"Sent response: {options['response']}", options["log_file"], options["log_level"])
    except socket.timeout:
        log("error", "Client connection timed out", options["log_file"], options["log_level"])
    except Exception as e:
        log("error", f"Error handling client: {e}", options["log_file"], options["log_level"])
    finally:
        client_socket.close()
        log("info", "Connection closed.", options["log_file"], options["log_level"])

def start_server(ip, port, options):
    sock_type = socket.AF_INET6 if options["ipv6"] else socket.AF_INET
    server = socket.socket(sock_type, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(options["max_clients"])
    
    log("info", f"Server listening on {ip}:{port}", options["log_file"], options["log_level"])
    
    while True:
        client_socket, address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address, options))
        client_thread.start()

def main():
    parser = argparse.ArgumentParser(description="Rasmnout TCP Server; TCPSERV Version 0.1.0")
    parser.add_argument("listen", nargs="?", help="Listen address in format <IP>@<PORT>")
    parser.add_argument("-exec", help="Execution")
    parser.add_argument("-version", action="store_true", help="Show version information")
    
    args = parser.parse_args()
    
    if args.version:
        log("info", f"Rasmnout TCP Server; TCPSERV Version {VERSION}")
        return
    
    if not args.listen:
        log("error", "Listen address is required. Use <IP>@<PORT> format.")
        return
    
    ip, port = args.listen.split('@')
    port = int(port)
    
    options = {
        "timeout": 5,
        "buffer_size": 1024,
        "max_clients": 5,
        "verbose": False,
        "log_file": None,
        "log_level": "info",
        "ipv6": False,
        "hex_dump": False,
        "encoding": "utf-8",
        "save_data": None,
        "response": None,
    }
    
    if args.exec:
        exec_options = args.exec.split(',')
        for option in exec_options:
            key, value = option.split('=') if '=' in option else (option, "True")
            key = key.strip()
            value = value.strip("'")
            
            if key in ["timeout", "buffer_size", "max_clients"]:
                options[key] = int(value)
            elif key in ["verbose", "ipv6", "hex_dump"]:
                options[key] = value.lower() == 'true'
            elif key in ["log_file", "log_level", "encoding", "save_data", "response"]:
                options[key] = value
    
    start_server(ip, port, options)


