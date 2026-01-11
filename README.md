<h1 align="center">
    <img src="/cmd_ui/assets/KeyShell_logo.png">
</h1>

<p align="center">
KeyShell is a robust CLI password manager designed to secure credentials locally using AES encryption and strict root access control. 
</p>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#demonstration">Demonstration</a>
</p>

<br>

## Description

**KeyShell** is a robust, modular, and security-focused Python CLI tool designed to securely manage passwords and sensitive credentials in a local environment.

Its goal is to provide a safe offline vault that ensures total privacy and control, utilizing industrial-standard AES-128 encryption and strict root access authentication to protect your data against unauthorized access.

Originally created as a learning project to explore cryptography and secure software engineering, KeyShell now serves as a solid base for anyone who wants to:

- Understand how modern encryption (AES, PBKDF2, Salting) is implemented in Python
- Manage passwords without relying on third-party cloud services
- Practice building secure CLI applications with defenses against common vulnerabilities (like Path Traversal)
<br>
<br>

## Features

✅ **Current capabilities**:
- Robust Cryptography: Uses AES-128 encryption (Fernet) combined with PBKDF2HMAC (SHA256) key derivation and unique salts.
- Secure Local Storage: Fully offline architecture storing encrypted secrets in isolated .bin files.
- Root Access Control: Single-user "Root" system with strict Master Password policy enforcement (length, complexity).
- Security-First UX: Implements "Double Check" authentication (requires Master Password confirmation before revealing secrets).
- Smart CLI Interface: Interactive terminal UI powered by rich, featuring colored alerts, tables, and ID-based selection.
- Defensive Engineering: Built-in protection against Path Traversal attacks and file injection attempts.
- Full CRUD Management: Easily Add, List, Retrieve, and Securely Delete credentials.


🛠️ **Work in progress**:
- Multi-User environment support with SQLite
- Asymetric encryption with RSA
- Clipboard integration (auto-copy passwords)
- Graphical User Interface (GUI) wrapper

<br>

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/RikoRiken/KeyShell.git
cd KeyShell
```

2. **Install dependencies: (Required for encryption and the UI)**
```bash
pip install -r requirements.txt
# OR manually:
pip install rich cryptography pytest
```
3. **Run the tool:**

***On Windows**, use the included batch file. It automatically handles the virtual environment and execution.*
```bash
.\KeyShell.bat
``` 

***On Linux**, run directly with Python 3.*
```bash
python3 main.py
``` 
<br>

## Demonstration

1. Secure authentication (Root Access)

Upon launch, the user is greeted by the secure banner and must authenticate to decrypt the vault.

Command *(On Windows)* = `.\KeyShell.bat`

Command *(On Linux)* = `python3 main.py`

<img src="/cmd_ui/assets/KeyShell_login.png">

2. Adding and Getting secrets (Interactive Mode)

The tool prompts for details and automatically enforces password policies before encrypting the data.

<img src="/cmd_ui/assets/KeyShell_add-get.png">


3. 🛡️ Security in Action: Vuln. Detected

KeyShell actively monitors for malicious inputs. Here, a Path Traversal attack (../hack) is detected and blocked instantly.

<img src="/cmd_ui/assets/KeyShell_path-traversal.png">
