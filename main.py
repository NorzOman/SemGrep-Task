import os
import time
import urllib.request
import zipfile
import datetime
import shutil
import platform
import subprocess
import json

# Defining global variables
is_jadx = False
is_pip = False
is_semgrep = False

# Function to print the banner
def banner():
    print("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                         SEMGREP ANALYSIS TOOL                            ║
    ║                                                                          ║
    ║       ███████╗███████╗███╗   ███╗ ██████╗ ██████╗ ███████╗██████╗        ║
    ║       ██╔════╝██╔════╝████╗ ████║██╔════╝ ██╔══██╗██╔════╝██╔══██╗       ║
    ║       ███████╗█████╗  ██╔████╔██║██║  ███╗██████╔╝█████╗  ██████╔╝       ║
    ║       ╚════██║██╔══╝  ██║╚██╔╝██║██║   ██║██╔══██╗██╔══╝  ██╔═══╝        ║
    ║       ███████║███████╗██║ ╚═╝ ██║╚██████╔╝██║  ██║███████╗██║            ║
    ║       ╚══════╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝            ║
    ║                                                                          ║
    ║                        Android Security Analysis                         ║
    ║                                                     -Tushar H1dden       ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """)

def check_requirements():
    global is_jadx, is_semgrep, is_pip
    
    # Check OS
    os_name = platform.uname().system.lower()
    if "windows" in os_name:
        print('\n[!] Windows not supported by the script, check supported platforms on the github repo')
        exit(1)
    elif "linux" not in os_name:
        print('\n[!] Only Linux is supported by this script')
        exit(1)

    # Check required tools
    jadx_path = os.path.expanduser('~/SemGrepTool/jadx/bin/jadx')
    if os.path.exists(jadx_path):
        is_jadx = True
        print('\n[-] Found jadx in ~/SemGrepTool/jadx...')
        time.sleep(0.5)
    else:
        print('\n[!] Required tool jadx was not found in the system...')
        time.sleep(0.5)

    if shutil.which("semgrep"):
        print('\n[-] Required tool semgrep is installed...')
        is_semgrep = True
        time.sleep(0.5)
    else:
        print('\n[!] Required tool semgrep was not found in the system...')

    if shutil.which("pip") or shutil.which("pip3"):
        print('\n[-] Required tool pip is installed...')
        is_pip = True
        time.sleep(0.5)
    else:
        print('\n[!] Required tool pip was not found in the system...')

def install_requirements():
    global is_pip, is_semgrep, is_jadx

    # Setting up pip
    if not is_pip:
        print('\n[?] pip is not installed. Would you like to install it? [Y/n]: ')
        pip_choice = input().lower()
        if pip_choice == '' or pip_choice == 'y':
            print('\n[!] Installing pip...')
            time.sleep(0.5)
            try:
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'python3-pip'], check=True)
                is_pip = True
            except subprocess.CalledProcessError:
                print('\n[!] Failed to install pip. Please install it manually.')
                exit(1)
        else:
            print('\n[!] pip installation rejected. Cannot proceed without pip. Exiting...')
            exit(1)

    # Setting up semgrep
    if not is_semgrep:
        print('\n[?] semgrep is not installed. Would you like to install it? [Y/n]: ')
        semgrep_choice = input().lower()
        if semgrep_choice == '' or semgrep_choice == 'y':
            print('\n[!] Installing semgrep...')
            time.sleep(0.5)
            try:
                subprocess.run(['python3', '-m', 'pip', 'install', 'semgrep', '--break-system-packages'], check=True)
                is_semgrep = True
            except subprocess.CalledProcessError:
                print('\n[!] Failed to install semgrep')
                exit(1)
        else:
            print('\n[!] semgrep installation rejected. Cannot proceed without semgrep. Exiting...')
            exit(1)
    
    # Setting up jadx
    if not is_jadx:
        print('\n[?] jadx is not installed. Would you like to install it? [Y/n]: ')
        jadx_choice = input().lower()
        if jadx_choice == '' or jadx_choice == 'y':
            print('\n[!] Installing jadx...')
            time.sleep(0.5)
            tool_dir = os.path.expanduser('~/SemGrepTool')
            jadx_dir = os.path.join(tool_dir, 'jadx')
            if not os.path.exists(jadx_dir):
                os.makedirs(jadx_dir)

            try:
                # Download jadx
                jadx_url = "https://github.com/skylot/jadx/releases/download/v1.5.1/jadx-1.5.1.zip"
                zip_path = os.path.join(jadx_dir, "jadx.zip")
                print('\n[-] Pulling jadx...This may take a while depending on your internet speed...Please be patient...')
                urllib.request.urlretrieve(jadx_url, zip_path)
                
                # Extract zip
                print('\n[-] Extracting jadx...')
                time.sleep(0.5)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(jadx_dir)
                
                # Make jadx executable
                jadx_bin = os.path.join(jadx_dir, 'bin', 'jadx')
                print('\n[-] Making jadx executable...')
                time.sleep(0.5)
                os.chmod(jadx_bin, 0o755)
                is_jadx = True

                # Cleanup
                os.remove(zip_path)
                print('\n[-] jadx installed successfully')
            except Exception as e:
                print(f'\n[!] Error installing jadx: {str(e)}')
                exit(1)
        else:
            print('\n[!] jadx installation rejected. Cannot proceed without jadx. Exiting...')
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

def main():
    tool_dir = os.path.expanduser('~/SemGrepTool')
    if not os.path.exists(tool_dir):
        os.makedirs(tool_dir)
        print('\n[-] Created working directory at ' + tool_dir)
        time.sleep(0.5)
    else:
        print('\n[-] Working directory already exists at ' + tool_dir)
        time.sleep(0.5)

    # Move our custom rules to the tool directory
    git_cloned_rule = os.path.join(os.getcwd(), 'rules')
    custom_rules_path = os.path.join(tool_dir, 'rules')

    if os.path.exists(custom_rules_path):
        print('\n[-] Custom rules already exist in tool directory')
        time.sleep(0.5)
        is_custom_rules = True
    else:
        if os.path.exists(git_cloned_rule):
            shutil.copytree(git_cloned_rule, custom_rules_path)
            print('\n[-] Copied rules from cloned repo to tool directory')
            time.sleep(0.5)
            is_custom_rules = True
        else:
            print('\n[!] Rules folder not found in current directory. Please ensure you cloned the repo correctly')
            time.sleep(0.5)
            is_custom_rules = False

    banner()
    print("\n[-] Initializing the tool...")
    time.sleep(0.5)
    check_requirements()

    if not is_jadx or not is_semgrep:
        print('\n[!] Required tools are not installed, installing them...')
        install_requirements()
    else:
        print('\n[-] All required tools are installed...')

    print('\n[-] Enter the path to the APK file: ')
    apk_path = input().strip()
    
    if not os.path.exists(apk_path):
        print('\n[!] APK file not found!')
        exit(1)
        
    # Create analysis directory
    apk_name = os.path.basename(apk_path).replace('.apk', '')
    current_date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    analysis_dir = os.path.expanduser(f'~/SemGrepTool/{apk_name}_{current_date}')
    if not os.path.exists(analysis_dir):
        os.makedirs(analysis_dir)
        
    # Create output directory
    output_dir = os.path.join(analysis_dir, 'output')
    os.makedirs(output_dir)
        
    # Copy APK to analysis directory
    new_apk_path = os.path.join(analysis_dir, os.path.basename(apk_path))
    shutil.copy2(apk_path, new_apk_path)
    
    # Decompile APK
    decompiled_dir = os.path.join(analysis_dir, 'decompiledapk')
    print('\n[-] Decompiling APK...')
    try:
        subprocess.run([os.path.expanduser('~/SemGrepTool/jadx/bin/jadx'), '-d', decompiled_dir, new_apk_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f'\n[!] Error decompiling APK: {str(e)}')
        exit(1)
    
    # Run semgrep with custom rules only
    print('\n[-] Running semgrep analysis using custom rules...')
    rules_path = custom_rules_path if is_custom_rules else git_cloned_rule
    custom_output = os.path.join(output_dir, 'custom_rules_results.json')
    try:
        subprocess.run([
            'semgrep', 'scan',
            '--config', rules_path,
            '--output', custom_output,
            '--json',
            decompiled_dir
        ], check=True)
        
        # Generate HTML report
        html_report = generate_html_report(custom_output, output_dir)
        
        if html_report:
            print(f'\n[-] Analysis complete! Results are stored in: {output_dir}')
            print('\n[-] You can find the following reports:')
            print(f'    - Custom rules report: {custom_output}')
            print(f'    - HTML report: {html_report}')
        else:
            print('\n[!] Failed to generate HTML report')
            
    except subprocess.CalledProcessError as e:
        print(f'\n[!] Error running semgrep analysis with custom rules: {str(e)}')
        exit(1)

if __name__ == '__main__':
    main()