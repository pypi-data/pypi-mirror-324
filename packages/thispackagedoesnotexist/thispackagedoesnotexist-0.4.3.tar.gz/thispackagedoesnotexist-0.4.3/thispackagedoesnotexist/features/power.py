import os
import time

def power(client, data, converter):
    try:
        command = data["power"]

        if command not in ["restart", "shutdown", "lock"]:
            client.emit('message', converter.encode({"power_logger": f"From Client: {command} not recognized"}))
            return
        
        client.emit('message', converter.encode({"power": f"From Client: {command} executed"}))
        
        time.sleep(2)

        if command == "restart":
            os.system("shutdown /r /t 0")
        elif command == "shutdown":
            os.system("shutdown /s /t 0")
        elif command == "lock":
            os.system("rundll32.exe user32.dll,LockWorkStation")

    except Exception as e:
        client.emit('message', converter.encode({"power_logger": str(e)}))
