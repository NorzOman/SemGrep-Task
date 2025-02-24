import os
import time
import urllib.request
import zipfile
import datetime
import shutil

# Defining global variables
is_apt = False
is_dnf = False
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
    global is_apt, is_dnf, is_jadx, is_semgrep, is_pip
    
    # Check OS
    os_name = platform.uname().system.lower()
    if "windows" in os_name:
        print('\n[!] Windows not supported by the script, check supported platforms on the github repo')
        exit(1)

    # Check package managers
    if shutil.which("apt"):
        is_apt = True
        print('\n[-] APT package manager found')
        time.sleep(0.5)
    elif shutil.which("dnf"):
        is_dnf = True
        print('\n[-] DNF package manager found')
        time.sleep(0.5)
    else:
        print('\n[?] Neither APT nor DNF found')
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
    global is_apt, is_dnf, is_pip, is_semgrep, is_jadx

    # Setting up pip
    if not is_pip:
        print('\n[?] pip is not installed. Would you like to install it? [Y/n]: ')
        pip_choice = input().lower()
        if pip_choice == '' or pip_choice == 'y':
            print('\n[!] Installing pip...')
            time.sleep(0.5)
            if is_apt:
                os.system('sudo apt install python3-pip')
            elif is_dnf:
                os.system('sudo dnf install python3-pip')
            is_pip = True
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
                if os.system('pip install semgrep --break-system-packages') != 0:
                    if os.system('pip3 install semgrep --break-system-packages') != 0:
                        raise Exception("Failed to install semgrep")
                is_semgrep = True
            except Exception as e:
                print('\n[!] Error installing semgrep: {str(e)}')
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
                print('\n[!] Error installing jadx: {str(e)}')
                exit(1)
        else:
            print('\n[!] jadx installation rejected. Cannot proceed without jadx. Exiting...')
            exit(1)

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
        
    # Copy APK to analysis directory
    new_apk_path = os.path.join(analysis_dir, os.path.basename(apk_path))
    shutil.copy2(apk_path, new_apk_path)
    
    # Decompile APK
    decompiled_dir = os.path.join(analysis_dir, 'decompiledapk')
    print('\n[-] Decompiling APK...')
    try:
        os.system(f'~/SemGrepTool/jadx/bin/jadx -d {decompiled_dir} {new_apk_path}')
    except Exception as e:
        print('\n[!] Error decompiling APK: {str(e)}')
        exit(1)
    
    # Run semgrep
    print('\n[-] Running semgrep analysis using custom rules...')
    rules_path = os.path.join(os.getcwd(), 'rules')
    try:
        os.system(f'semgrep scan --config={rules_path} {decompiled_dir}')
    except Exception as e:
        print('\n[!] Error running semgrep analysis: {str(e)}')
        exit(1)
    
    print('\n[-] Running semgrep analysis using default rules...')
    try:
        os.system(f'semgrep scan --config=auto {decompiled_dir}')
    except Exception as e:
        print('\n[!] Error running semgrep analysis: {str(e)}')
        exit(1)
        

if __name__ == '__main__':
    main()
