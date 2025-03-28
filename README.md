# 🛡️ APK Security Scanner

A powerful automated security analysis tool for Android APKs using Semgrep and JADX. This tool simplifies the process of identifying potential security vulnerabilities in Android applications by combining decompilation and advanced pattern matching.

## ✨ Features

- 🔍 **Automated Scanning**: Seamlessly decompiles APKs and scans for security vulnerabilities
- 📊 **Rich Reporting**: Generates both JSON and HTML reports with detailed findings
- 🚀 **Easy Installation**: One-command global installation
- 📁 **Organized Output**: Structured output with decompiled code and scan results
- 🎯 **Custom Rules**: Utilizes specialized Semgrep rules for Android security

## 🔧 Prerequisites

- Linux-based operating system
- Python 3.x
- OpenJDK 17+ (for JADX)
- Internet connection (for initial setup)

## ⚡ Quick Installation

1. **Install OpenJDK** (if not already installed):
   ```bash
   sudo apt update
   sudo apt install openjdk-17-jdk
   ```

2. **Get the tool**:
   ```bash
   git clone https://github.com/yourusername/apk-scanner.git
   cd apk-scanner
   ```

3. **Install globally**:
   ```bash
   sudo python3 apkscan.py --install
   ```

## 📝 Usage

Basic scan:
```bash
apkscan -a target.apk -o output_dir
```

Options:
```bash
apkscan --help
```

Example workflow:
```bash
cd ~/Downloads
apkscan -a suspicious.apk -o scan_results
```

## 📂 Output Structure

```
output_dir/
├── decompiled/         # Decompiled APK source
└── reports/
    ├── semgrep_results.json   # Detailed findings in JSON
    └── semgrep_report.html    # User-friendly HTML report
```

## 🛠️ Additional Options

```bash
apkscan -a <apk_file> -o <output_dir> [options]
  -s, --skip-dependencies-check    Skip dependency verification
  --install                        Install tool globally
```

## 📊 Reports

The tool generates two report formats:
- **HTML Report**: User-friendly interface with:
  - Color-coded severity indicators
  - Detailed vulnerability descriptions
  - Code snippets and locations
  - Quick navigation
- **JSON Report**: Machine-readable format for:
  - Integration with other tools
  - Custom analysis
  - Data processing

