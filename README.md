# 🛡️ APK Security Scanner with Semgrep

A Python tool that automates APK security analysis using Semgrep and JADX. This tool helps security researchers and developers identify potential vulnerabilities in Android applications by scanning decompiled APK code.

## 🚀 Features
- **Automated Analysis**: Decompiles APKs and scans for security vulnerabilities using custom Semgrep rules
- **Detailed Reports**: Generates both JSON and HTML reports with findings
- **Easy Setup**: Automatically installs and configures all required tools
- **Organized Output**: Creates a structured output directory with decompiled code and scan results

## 🔧 Prerequisites
- Linux-based operating system
- Python 3.x
- OpenJDK 17 or higher (required for JADX)
- Internet connection for tool installation

## 🛠️ Installation & Setup
1. Install OpenJDK 17 if not already installed:
   ```bash
   sudo apt update
   sudo apt install openjdk-17-jdk
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/apk-security-scanner.git
   cd apk-security-scanner
   ```

3. Run the tool:
   ```bash
   python3 main.py
   ```

4. When prompted, type 'Y' to install any missing dependencies (pip, Semgrep, JADX)

## 📝 Usage
1. Place your APK file anywhere accessible
2. Run the tool: `python3 main.py`
3. When prompted, enter the full path to your APK file
4. Wait for the analysis to complete

## 📂 Output Structure
The tool creates a workspace at `~/SemGrepTool/` containing:
- `jadx/`: JADX decompiler installation
- `rules/`: Custom Semgrep rules
- `{apk_name}_{timestamp}/`: Analysis directory for each scan
  - `decompiledapk/`: Decompiled APK source code
  - `output/`: Analysis results
    - `custom_rules_results.json`: Detailed JSON report
    - `semgrep_report.html`: User-friendly HTML report

## 📊 Understanding Results
- The HTML report provides a clean interface to review findings
- Results are color-coded by severity (High, Medium, Low)
- Each finding includes:
  - Vulnerability type
  - Affected file and line number
  - Code snippet
  - Detailed description


Demo:

https://github.com/user-attachments/assets/e4385c12-5d75-4c23-9671-0e4b6b37f7d7

