# 🛡️ APK Security Scanner

A powerful automated security analysis tool for Android APKs using Semgrep and JADX. This tool simplifies the process of identifying potential security vulnerabilities in Android applications by combining decompilation and advanced pattern matching.

## ✨ Features

- 🔍 **Automated Scanning**: Seamlessly decompiles APKs and scans for security vulnerabilities
- 📊 **JSON Reports**: Generates detailed findings in JSON format
- 🚀 **Simple Usage**: Just clone and run
- 📁 **Organized Output**: Timestamp-based output structure
- 🎯 **Dual Scanning**: Uses both custom and default Semgrep rules

## 🔧 Prerequisites

- Kali Linux (script is Kali-specific)
- Python 3.x
- Internet connection (for tool installation)

## ⚡ Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/apk-scanner.git
   cd apk-scanner
   ```

2. **Run the scanner**:
   ```bash
   python3 apkscan.py -a /path/to/your.apk
   ```

## 📂 Output Structure

```
repository/
├── input/
│   └── YYYYMMDD_HHMMSS/  # Timestamp folder containing input APK
└── output/
    └── YYYYMMDD_HHMMSS/  # Timestamp folder containing:
        ├── custom.json   # Results from custom rules
        ├── default.json  # Results from default Semgrep rules
        └── sources/      # Decompiled APK source code
```

## 🛠️ Command Options

```bash
python3 apkscan.py -a <apk_file> [options]
  --skip-check    Skip dependency verification
```

## ⚠️ Script Panic

If you see the "SCRIPT PANIC" ASCII art banner, it indicates a critical error, typically related to JADX decompilation. Common causes include:
- Corrupted APK file
- JADX installation issues
- Insufficient permissions
- Memory constraints

## 📝 Notes

- The script will automatically install required dependencies (JADX and Semgrep)
- Results are organized by timestamp for easy tracking
- Both custom and default Semgrep rules are applied automatically

