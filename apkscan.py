#!/usr/bin/env python3

import os
import time
import urllib.request
import zipfile
import datetime
import shutil
import platform
import subprocess
import json
import argparse

# Defining global variables
is_jadx = False
is_pip = False
is_semgrep = False

# Function to print the banner
def banner():
    print(r"""
        ____ ___  _  _ ____ ____ ____ _  _ 
        |__| |__] |_/  [__  |    |__| |\ | 
        |  | |    | \_ ___] |___ |  | | \| 

                                        -- by @h1dden --
    """)


def check_requirements():
    global is_jadx, is_semgrep, is_pip
    
    # Check OS
    os_name = platform.uname().system.lower()
    if "windows" in os_name:
        print('[!] Windows not supported by the script')
        exit(1)
    elif "linux" not in os_name:
        print('[!] Only Linux is supported by this script')
        exit(1)

    # Check required tools
    jadx_path = os.path.expanduser('~/SemGrepTool/jadx/bin/jadx')
    if os.path.exists(jadx_path):
        is_jadx = True
    
    if shutil.which("semgrep"):
        is_semgrep = True
    
    if shutil.which("pip") or shutil.which("pip3"):
        is_pip = True

def install_requirements():
    global is_pip, is_semgrep, is_jadx

    if not is_pip:
        try:
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-pip'], check=True)
            is_pip = True
        except subprocess.CalledProcessError:
            print('[!] Failed to install pip')
            exit(1)

    if not is_semgrep:
        try:
            subprocess.run(['python3', '-m', 'pip', 'install', 'semgrep', '--break-system-packages'], check=True)
            is_semgrep = True
        except subprocess.CalledProcessError:
            print('[!] Failed to install semgrep')
            exit(1)

    if not is_jadx:
        tool_dir = os.path.expanduser('~/SemGrepTool')
        jadx_dir = os.path.join(tool_dir, 'jadx')
        os.makedirs(jadx_dir, exist_ok=True)

        try:
            jadx_url = "https://github.com/skylot/jadx/releases/download/v1.5.1/jadx-1.5.1.zip"
            zip_path = os.path.join(jadx_dir, "jadx.zip")
            print('[-] Downloading jadx...')
            urllib.request.urlretrieve(jadx_url, zip_path)
            
            print('[-] Extracting jadx...')
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(jadx_dir)
            
            jadx_bin = os.path.join(jadx_dir, 'bin', 'jadx')
            os.chmod(jadx_bin, 0o755)
            is_jadx = True
            os.remove(zip_path)
        except Exception as e:
            print(f'[!] Error installing jadx: {str(e)}')
            exit(1)

def generate_html_report(custom_output, output_dir):
    try:
        html_content = """
        <html>
        <head>
            <title>Semgrep Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; }
                .finding { 
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 5px;
                }
                .severity-high { border-left: 5px solid #ff4444; }
                .severity-medium { border-left: 5px solid #ffbb33; }
                .severity-low { border-left: 5px solid #00C851; }
                .section { margin-bottom: 30px; }
            </style>
        </head>
        <body>
            <h1>Semgrep Analysis Report</h1>
        """

        # Process custom rules results
        with open(custom_output) as f:
            custom_data = json.load(f)
        
        html_content += "<div class='section'><h2>Custom Rules Results</h2>"
        if custom_data.get('results'):
            for finding in custom_data['results']:
                severity = finding.get('extra', {}).get('severity', 'unknown')
                html_content += f"""
                <div class='finding severity-{severity.lower()}'>
                    <h3>{finding.get('check_id', 'Unknown Check')}</h3>
                    <p><strong>Severity:</strong> {severity}</p>
                    <p><strong>Message:</strong> {finding.get('extra', {}).get('message', 'No message available')}</p>
                    <p><strong>Path:</strong> {finding.get('path', 'Unknown path')}</p>
                    <p><strong>Line:</strong> {finding.get('start', {}).get('line', 'Unknown line')}</p>
                    <p><strong>Code:</strong> <pre>{finding.get('extra', {}).get('lines', 'No code available')}</pre></p>
                </div>
                """
        else:
            html_content += "<p>No findings from custom rules</p>"
            
        html_content += "</div></body></html>"

        # Write HTML report
        html_report = os.path.join(output_dir, 'semgrep_report.html')
        with open(html_report, 'w') as f:
            f.write(html_content)
        
        return html_report
    except Exception as e:
        print(f'\n[!] Error generating HTML report: {str(e)}')
        return None

def install_globally():
    if os.geteuid() != 0:
        print("[!] This installation requires root privileges. Please run with sudo.")
        exit(1)
    
    try:
        # Get the absolute path of the current script
        script_path = os.path.abspath(__file__)
        install_path = "/usr/local/bin/apkscan"
        
        # Copy the script to /usr/local/bin
        shutil.copy2(script_path, install_path)
        
        # Make it executable
        os.chmod(install_path, 0o755)
        
        print("[-] Successfully installed! You can now use 'apkscan' command globally.")
        print("    Example usage:")
        print("    apkscan -a app.apk -o output_dir")
        exit(0)
    except Exception as e:
        print(f"[!] Installation failed: {str(e)}")
        exit(1)

def main():
    # Show banner first
    banner()
    
    parser = argparse.ArgumentParser(
        description='''
Semgrep Analysis Tool for Android APKs
-------------------------------------
A tool for automated security analysis of Android APK files using Semgrep.
Decompiles APK files and scans for security vulnerabilities using custom rules.

Example usage:
  apkscan -a app.apk -o output_dir
  apkscan --apk app.apk --output output_dir --skip-dependencies-check
  sudo apkscan --install    # To install globally
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--install',
                      action='store_true',
                      help='Install the script globally as "apkscan" command')
    
    parser.add_argument('-a', '--apk', 
                      help='Path to the APK file to analyze')
    
    parser.add_argument('-o', '--output',
                      help='Output directory for analysis results')
    
    parser.add_argument('-s', '--skip-dependencies-check',
                      action='store_true',
                      help='Skip checking and installing dependencies')

    args = parser.parse_args()

    # Handle installation if --install is specified
    if args.install:
        install_globally()
        return  # Exit after installation

    # Validate required arguments for normal operation
    if not args.apk or not args.output:
        parser.error("Both --apk and --output are required unless --install is specified")

    if not args.skip_dependencies_check:
        print("[-] Checking requirements...")
        check_requirements()
        if not all([is_jadx, is_semgrep, is_pip]):
            print('[-] Installing missing requirements...')
            install_requirements()

    if not os.path.exists(args.apk):
        print('[!] APK file not found!')
        exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Create analysis subdirectories
    decompiled_dir = os.path.join(args.output, 'decompiled')
    reports_dir = os.path.join(args.output, 'reports')
    os.makedirs(decompiled_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # Decompile APK
    print('[-] Decompiling APK...')
    try:
        subprocess.run([os.path.expanduser('~/SemGrepTool/jadx/bin/jadx'), 
                       '-d', decompiled_dir, args.apk], check=True)
    except subprocess.CalledProcessError as e:
        print(f'[!] Error decompiling APK: {str(e)}')
        exit(1)

    # Run semgrep analysis
    print('[-] Running semgrep analysis...')
    custom_rules_path = os.path.join(os.getcwd(), 'rules')
    custom_output = os.path.join(reports_dir, 'semgrep_results.json')
    
    try:
        subprocess.run([
            'semgrep', 'scan',
            '--config', custom_rules_path,
            '--output', custom_output,
            '--json',
            decompiled_dir
        ], check=True)
        
        html_report = generate_html_report(custom_output, reports_dir)
        if html_report:
            print(f'[-] Analysis complete! Results are stored in: {args.output}')
            print('[-] Generated reports:')
            print(f'    - JSON report: {custom_output}')
            print(f'    - HTML report: {html_report}')
        
    except subprocess.CalledProcessError as e:
        print(f'[!] Error running semgrep analysis: {str(e)}')
        exit(1)

if __name__ == '__main__':
    main()