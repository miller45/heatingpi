import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class OLED:
    DC = 23

    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.disp.begin()
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.font = ImageFont.load_default()

    def ping(self):
        print("ping from oled")

    def sayHello(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        x = 0
        self.draw.text((x, self.top),"Hello World", font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()
