import socket
import argparse
import re
from datetime import datetime
import sys
class MessageLog:
    def info(msg, write_to_file=""):
        if write_to_file == False:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} INFO ] {msg}")
        else:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} INFO ] {msg}")
            with open(f"{write_to_file}", "a") as f:
                f.write(f"[ {current_time.strftime('%H:%M:%S')} INFO ] {msg}")
    
    def error(msg, write_to_file=""):
        if write_to_file == False:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} ERROR ] {msg}")
        else:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} ERROR ] {msg}")
            with open(f"{write_to_file}", "a") as f:
                f.write(f"[ {current_time.strftime('%H:%M:%S')} ERROR ] {msg}")
    
    def message(msg, write_to_file=""):
        if write_to_file == False:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} MESSAGE ] {msg}")
        else:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} MESSAGE ] {msg}")
            with open(f"{write_to_file}", "a") as f:
                f.write(f"[ {current_time.strftime('%H:%M:%S')} MESSAGE ] {msg}")
    
    def disconnected(msg, write_to_file=""):
        if write_to_file == False:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} DISCONNECTED ] {msg}")
        else:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} DISCONNECTED ] {msg}")
            with open(f"{write_to_file}", "a") as f:
                f.write(f"[ {current_time.strftime('%H:%M:%S')} DISCONNECTED ] {msg}")
    
    def connected(msg, write_to_file=""):
        if write_to_file == False:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} CONNECTED ] {msg}")
        else:
            current_time = datetime.now()
            print(f"[ {current_time.strftime('%H:%M:%S')} CONNECTED ] {msg}")
            with open(f"{write_to_file}", "a") as f:
                f.write(f"[ {current_time.strftime('%H:%M:%S')} CONNECTED ] {msg}")
def main():
    parser = argparse.ArgumentParser(description="TCP Receiver; TCPRECV Version 0.1.2")
    parser.add_argument("host_port", help="Target")
    parser.add_argument("-exec",type=str, help="Execution")
    parser.add_argument("-log", type=str,help="Logging Output")
    parser.add_argument("version",action="store_true",help="TCP Receiver Version")
    args = parser.parse_args()

    file = False
    if args.host_port == "version":
        print("Rasmnout TCP Receiver; TCPRECV Version 0.1.2")
    elif args.log:
        file = args.log

    elif "@" in args.host_port:
        ip, port2 = args.host_port.split("@")
        port = int(port2)
        if args.exec:
            execution = args.exec
            repeat = False
            timeout = 1
            save_msgs = False
            max_size = 1024
            exit_on_empty = False
            commands = re.split(r",\s*", execution)

            for command in commands:
                if "repeat=" in command:
                    match = re.search(r"repeat=(true|false)", command, re.IGNORECASE)
                    if match:
                        repeat = match.group(1).lower() == "true"

                elif "timeout=" in command:
                    match = re.search(r"timeout=(\d+)", command)
                    if match:
                        timeout = int(match.group(1))

                elif "saveMSGs=" in command:
                    match = re.search(r"saveMSGs=(true|false)", command, re.IGNORECASE)
                    if match:
                        save_msgs = match.group(1).lower() == "true"

                elif "maxSize=" in command:
                    match = re.search(r"maxSize=(\d+)", command)
                    if match:
                        max_size = int(match.group(1))

                elif "exitOnEmpty=" in command:
                    match = re.search(r"exitOnEmpty=(true|false)", command, re.IGNORECASE)
                    if match:
                        exit_on_empty = match.group(1).lower() == "true"
                else:
                    nice_looking, bad_looking = command.split("=")
                    bad_command = nice_looking.upper()
                    MessageLog.error(f"{bad_command}: Unknown execution option",write_to_file=file)
                    exit(0)
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                timeout_autistic = int(timeout)
                client_socket.settimeout(timeout_autistic)
                try:
                    client_socket.connect((ip,port))
                    MessageLog.connected(f"Connected to {ip}@{port}",write_to_file=file)
                    MessageLog.info(f"Timeout: {timeout}  Socket Type: {client_socket.type}  Socket Family: {client_socket.family}  Local Port: {client_socket.getsockname()[1]}  Socket Blocking Mode: {client_socket.getblocking()}  Socket Fileno: {client_socket.fileno()}",write_to_file=file)
                    try:
                        if repeat == True:
                            try:
                                while True:
                                    data = client_socket.recv(int(max_size))
                                    if data:
                                        try:
                                            decode_data = data.decode('utf-8')
                                            if exit_on_empty == True:
                                                if decode_data == "" or b"":
                                                    MessageLog.error(f"Host: {ip}@{port} Nothing sent")
                                                    exit(0)
                                            MessageLog.message(f"{decode_data}",write_to_file=file)
                                            if save_msgs != False:
                                                MessageLog.message(f"{decode_data}",write_to_file=save_msgs)
 
                                        except UnicodeDecodeError as e:
                                            MessageLog.error(f"Decode error: {e}",write_to_file=file)
                                            MessageLog.info("Trying to decode the data.",write_to_file=file)
                                            decoded_data = data.decode('utf-8',errors="ignore")
                                            if exit_on_empty == True:
                                                if decoded_data == "" or b"":
                                                    MessageLog.error(f"Host: {ip}@{port} Nothing sent")
                                                    exit(0)
                                            MessageLog.message(f"{decoded_data}",write_to_file=file)
                                    else:
                                        MessageLog.error(f"No data received from {ip}@{port} within {timeout} seconds",write_to_file=file)
                            except KeyboardInterrupt:
                                exit(0)
                        else:
                            data = client_socket.recv(int(max_size))
                            if data:
                                try:
                                    decode_data = data.decode('utf-8')
                                    MessageLog.message(f"{decode_data}",write_to_file=file)
                                    if save_msgs != False:
                                        MessageLog.message(f"{decode_data}",write_to_file=save_msgs)
 
                                except UnicodeDecodeError as e:
                                    MessageLog.error(f"Decode error: {e}",write_to_file=file)
                                    MessageLog.info("Trying to decode the data.",write_to_file=file)
                                    decoded_data = data.decode('utf-8',errors="ignore")
                                    MessageLog.message(f"{decoded_data}",write_to_file=file)
                            else:
                                MessageLog.error(f"No data received from {ip}@{port} within {timeout} seconds",write_to_file=file)
                    except socket.timeout:
                        MessageLog.error(f"No data received within {timeout} seconds",write_to_file=file)
                except Exception as err:
                    MessageLog.error(err,write_to_file=file)
                finally:
                    client_socket.close()



        
        else:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(1)
            try:
                client_socket.connect((ip,port))
                MessageLog.connected(f"Connected to {ip}@{port}",write_to_file=file)
                MessageLog.info(f"Timeout: 1  Socket Type: {client_socket.type}  Socket Family: {client_socket.family}  Local Port: {client_socket.getsockname()[1]}  Socket Blocking Mode: {client_socket.getblocking()}  Socket Fileno: {client_socket.fileno()}",write_to_file=file)
                try:
                    data = client_socket.recv(1024)
                    if data:
                        try:
                            decode_data = data.decode('utf-8')
                            MessageLog.message(f"{decode_data}",write_to_file=file)
                        except UnicodeDecodeError as e:
                            MessageLog.error(f"Decode error: {e}",write_to_file=file)
                            MessageLog.info("Trying to decode the data.",write_to_file=file)
                            decoded_data = data.decode('utf-8',errors="ignore")
                            MessageLog.message(f"{decoded_data}",write_to_file=file)
                    else:
                        MessageLog.error(f"No data received from {ip}@{port} within 1 seconds",write_to_file=file)
                except socket.timeout:
                    MessageLog.error("No data received within 1 seconds",write_to_file=file)
            except Exception as err:
                MessageLog.error(err,write_to_file=file)
            finally:
                client_socket.close()
    else:
        parser.print_help()
