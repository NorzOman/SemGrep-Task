# 🛡️ APK Security Scanner with Semgrep

A Python tool that automates APK security analysis using Semgrep and JADX. This tool helps security researchers and developers identify potential vulnerabilities in Android applications.

## 🚀 Features
- **Automated Setup**: Automatically installs and configures required tools (JADX, Semgrep)
- **APK Decompilation**: Uses JADX to decompile APK files for analysis
- **Security Scanning**: Leverages Semgrep's auto-detection to find security issues
- **Cross-Platform**: Works on Linux distributions with APT or DNF package managers
- **User-Friendly**: Interactive prompts and colored output for better usability

## 🔧 Requirements
- Linux-based operating system (Kali Linux recommended)
- Python 3.x
- APT or DNF package manager
- Internet connection for tool installation

## 🛠️ Installation
1. Clone this repository
2. Run the script: `python3 main.py`
3. Follow the interactive prompts to install required tools

## 📝 Usage
1. Launch the tool: `python3 main.py`
2. The script will check and install required dependencies
3. Enter the path to your APK file when prompted
4. Wait for the analysis to complete
