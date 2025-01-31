def main():
    print("\nTCP Packages by Rasmnout ( https://rasmnout.github.io/tcp-packages )")
    print("Your one-stop solution for working with TCP packages.\n")
    
    tools = {
        'tcprecv': {
            'version': '0.1.2',
            'description': 'Capture TCP messages from a server',
            'exec_options': [
                'repeat=<True/False>', 
                'timeout=<int>', 
                'saveMSGs="<path>"', 
                'maxSize=<int>', 
                'exitOnEmpty=<True/False>'
            ]
        },
        'tcpsend': {
            'version': '0.1.6',
            'description': 'Send TCP messages to a server',
            'exec_options': [
                'timeout=<int>', 
                'data="<message>"', 
                'retry=<int>', 
                'buffer_size=<int>', 
                'verbose=<True/False>', 
                'no_response=<True/False>', 
                'data_file="<path>"', 
                'encoding="<utf-8/latin1/raw>"', 
                'log_file="<path>"', 
                'log_level="info/debug/error"', 
                'random_delay=<int>', 
                'max_attempts=<int>', 
                'chunk_size=<int>', 
                'keep_alive=<True/False>', 
                'ipv6=<True/False>', 
                'ssl=<True/False>', 
                'hex_dump=<True/False>', 
                'force_disconnect=<True/False>'
            ]
        },
        'tcpserv': {
            'version': '0.1.0',
            'description': 'Create a TCP server',
            'exec_options': [
                'timeout=<int>', 
                'buffer_size=<int>', 
                'max_clients=<int>', 
                'verbose=<True/False>', 
                'log_file="<file>"', 
                'ipv6=<True/False>', 
                'hex_dump=<True/False>', 
                'save_data="<path>"', 
                'response="<message>"'
            ]
        },
        'tcptraffic': {
            'version': '0.1.0',
            'description': 'Capture TCP traffic from the network',
            'exec_options': [
                'target=<ip>', 
                'src=<ip>', 
                'dst=<ip>', 
                'listen=<ip>@<port>'
            ]
        }
    }
    
    for tool, info in tools.items():
        print(f"\nTool: {tool} (v{info['version']})")
        print(f"  Description: {info['description']}")
        print("  Options:")
        print(f"    -h / --help: Display Help")
        print(f"    -version: Display version")
        print(f"    -exec=\"<EXECUTION OPTION>\": Execution options include:")
        for option in info['exec_options']:
            print(f"      - {option}")
    
    print("\nExecution options allow you to customize the behavior of each tool, such as setting timeouts, buffers, and response messages.")


