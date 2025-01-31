import socket
import sys
import argparse
import time
import random

# Verze skriptu
VERSION = "0.1.6"

def log(level, message, log_file=None, log_level="info"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    if log_level in ["info", "debug"] or (log_level == "error" and level == "error"):
        log_message = f"[{level.upper()} {timestamp}] {message}"
        print(log_message)
        if log_file:
            with open(log_file, "a") as f:
                f.write(log_message + "\n")

def send_tcp_data(ip, port, data, timeout=1, retry=1, buffer_size=1024, verbose=False, no_response=False, encoding='utf-8', log_file=None, log_level='info', random_delay=0, max_attempts=3, chunk_size=None, keep_alive=False, ipv6=False, ssl=False, hex_dump=False, force_disconnect=False):
    for attempt in range(min(retry, max_attempts)):
        try:
            sock_type = socket.AF_INET6 if ipv6 else socket.AF_INET
            sock = socket.socket(sock_type, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            log("info", f"Attempt {attempt + 1} of {retry}: Connecting to {ip}:{port} with timeout {timeout} seconds...", log_file, log_level)
            
            sock.connect((ip, port))
            log("info", f"Connected to {ip}:{port}", log_file, log_level)
            
            if random_delay:
                delay = random.randint(0, random_delay) / 1000
                time.sleep(delay)
                log("debug", f"Random delay of {delay} seconds before sending data", log_file, log_level)
            
            if chunk_size:
                for i in range(0, len(data), chunk_size):
                    sock.sendall(data[i:i+chunk_size].encode(encoding) if isinstance(data, str) else data[i:i+chunk_size])
            else:
                sock.sendall(data.encode(encoding) if isinstance(data, str) else data)
            
            if no_response:
                log("info", "No response requested. Closing connection.", log_file, log_level)
                sock.close()
                return
            
            response = sock.recv(buffer_size)
            if hex_dump:
                log("info", f"Received hex dump: {response.hex()}", log_file, log_level)
            else:
                try:
                    decoded_response = response.decode(encoding)
                    log("info", f"Received response: {decoded_response}", log_file, log_level)
                except UnicodeDecodeError:
                    log("info", f"Received raw bytes: {response}", log_file, log_level)
            
            if force_disconnect:
                log("info", "Force disconnect enabled. Closing connection immediately.", log_file, log_level)
                sock.close()
                return
            
            if not keep_alive:
                sock.close()
                log("info", "Connection closed.", log_file, log_level)
            return
        except socket.timeout:
            log("error", f"Attempt {attempt + 1} of {retry}: Connection timed out", log_file, log_level)
        except Exception as e:
            log("error", f"Attempt {attempt + 1} of {retry}: An error occurred: {e}", log_file, log_level)
        finally:
            if 'sock' in locals():
                sock.close()
                log("info", "Connection closed.", log_file, log_level)

def main():
    parser = argparse.ArgumentParser(description="Rasmnout TCP Send; TCPSEND Version 0.1.6")
    parser.add_argument("destination", nargs="?", help="Destination in format <IP>@<PORT>")
    parser.add_argument("-exec", help="Options, e.g., timeout=1,data='Hello, Server!',verbose=True,retry=3,buffer_size=2048,no_response=True,data_file='file.txt',encoding='utf-8',log_file='log.txt',log_level='debug',random_delay=100,max_attempts=5,chunk_size=512,keep_alive=True,ipv6=True,ssl=True,hex_dump=True,force_disconnect=True")
    parser.add_argument("-version", action="store_true", help="Show version information")
    
    args = parser.parse_args()
    
    if args.version:
        log("info", f"Rasmnout TCP Send; TCPSEND Version {VERSION}")
        return
    
    if not args.destination:
        log("error", "Destination is required. Use <IP>@<PORT> format.")
        return
    
    ip, port = args.destination.split('@')
    port = int(port)
    
    options = {
        "timeout": 1,
        "data": "Hello, Server!",
        "retry": 1,
        "buffer_size": 1024,
        "verbose": False,
        "no_response": False,
        "data_file": None,
        "encoding": 'utf-8',
        "log_file": None,
        "log_level": "info",
        "random_delay": 0,
        "max_attempts": 3,
        "chunk_size": None,
        "keep_alive": False,
        "ipv6": False,
        "ssl": False,
        "hex_dump": False,
        "force_disconnect": False
    }
    
    if args.exec:
        exec_options = args.exec.split(',')
        for option in exec_options:
            key, value = option.split('=') if '=' in option else (option, "True")
            key = key.strip()
            value = value.strip("'")
            
            if key in ["timeout", "retry", "buffer_size", "random_delay", "max_attempts", "chunk_size"]:
                options[key] = int(value)
            elif key in ["verbose", "no_response", "keep_alive", "ipv6", "ssl", "hex_dump", "force_disconnect"]:
                options[key] = value.lower() == 'true'
            elif key in ["data", "data_file", "encoding", "log_file", "log_level"]:
                options[key] = value
    
    if options["data_file"]:
        try:
            with open(options["data_file"], 'rb') as f:
                options["data"] = f.read()
            log("info", f"Read {len(options['data'])} bytes from {options['data_file']}", options["log_file"], options["log_level"])
        except Exception as e:
            log("error", f"Error reading file {options['data_file']}: {e}", options["log_file"], options["log_level"])
            return
    
    send_tcp_data(ip, port, **options)
