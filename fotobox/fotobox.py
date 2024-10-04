import time
import logging
import os
from subprocess import check_call
from gpiozero import OutputDevice, Button
from picamera2 import Picamera2, Preview
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class Fotobox:
    def generate_static_overlay(self, text):
        try:
            img = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", self.fontsize)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((self.width - text_width) // 2, (self.height - text_height) // 2)
            draw.text(position, text, font=font, fill=(255, 255, 255, 255))
            overlay_img = np.array(img)
            return overlay_img
        except Exception as e:
            logging.error(f"Error while generating static overlay: {e}")
            return None

    def capture(self):
        if self.ready:
            self.ready = False
            self.flash_switch.on()
            for text in self.countdown:
                self.camera.set_overlay(text)
                time.sleep(1)
            filename = time.strftime("/fotobox/%Y%m%d-%H%M%S.jpg")
            self.camera.capture_file(filename)
            self.camera.set_overlay(self.welcometext)
            self.flash_switch.off()
            self.ready = True
            logging.info(f"Captured image: {filename}")

    def poweroff(self):
        logging.info("Shutting down...")
        check_call(["systemctl", "poweroff", "-i"])

    def __init__(self, width, height, fontsize, welcometext, countdown):
        self.width = int(width)
        self.height = int(height)
        self.fontsize = int(fontsize)
        self.welcometext = self.generate_static_overlay(str(welcometext))
        self.ready = False
        self.camera = None
        self.countdown = [self.generate_static_overlay(str(text)) for text in list(countdown)]
        self.capture_button = Button(16, bounce_time=0.1)
        self.capture_button.when_pressed = self.capture
        self.poweroff_button = Button(17, bounce_time=0.1)
        self.poweroff_button.when_pressed = self.poweroff
        self.flash_switch = OutputDevice(18, active_high=True, initial_value=False)
        if not os.path.exists("/fotobox"):
            os.makedirs("/fotobox")
            logging.info("Folder '/fotobox' created.")
        else:
            logging.info("Folder '/fotobox' already exists.")
        try:
            self.camera = Picamera2()
            self.camera.configure(self.camera.create_preview_configuration(main={"size": (self.width, self.height)}))
            self.camera.start_preview(Preview.DRM, width=self.width, height=self.height)
            self.camera.start()
        except Exception as e:
            logging.error(f"Failed to initialize the camera: {e}")
            exit(1)
        time.sleep(1)
        self.camera.set_overlay(self.welcometext)
        self.ready = True
        logging.info("Fotobox is ready")

    def close(self):
        logging.info("Closing Fotobox and releasing the camera and gpio pins.")
        self.shutdown = True
        if self.camera:
            self.camera.stop_preview()
            self.camera.stop()
        try:
            self.capture_button.close()
            self.poweroff_button.close()
            self.flash_switch.close()
        except AttributeError:
            logging.warning("GPIO pins already cleaned up or not initialized.")
