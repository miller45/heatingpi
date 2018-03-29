import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class OLED:
    DC = 23
    fontHeight = 8
    robotoFontLineHeight=18

    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
        self.disp.begin()
        self.width = self.disp.width
        self.height = self.disp.height
        # self.image = Image.open('heatingpi.ppm').convert('1')
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        self.font = ImageFont.load_default()
        self.robotoFont = ImageFont.truetype("Roboto-Black.ttf", self.robotoFontLineHeight)

    def ping(self):
        print("ping from oled")

    def showSplashScreen(self):
        # self.image = Image.open('happycat_oled_32.ppm').convert('1')

        # self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        x = 0
        y = self.top;
        self.draw.text((x, y), "Welcome to...", font=self.font, fill=255)
        y += self.fontHeight
        self.draw.text((x, y), "Heating PI", font=self.robotoFont, fill=255)
        y += self.robotoFontLineHeight
        # self.draw.text((x, self.top + self.LINEHEIGHT * 1),"w "+str(self.width)+" h "+str(self.height), font=self.uniFont, fill=255)
        self.disp.image(self.image)
        self.disp.display()
    def showTemperatures(self,t1,t2):
        x=0
        y=0
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.draw.text((x, self.top),"IN "+format(t1,".1f")+" OUT "+format(t2,'.1f'), font=self.font, fill=255)
        y+=self.fontHeight
        self.draw.text((x, y), "DIFF " + format(t2-t1,".1f") , font=self.robotoFont, fill=255)
        #y+=self.robotoFontLineHeight
        #self.draw.text((x, y), "T2 " + str(t2) , font=self.robotoFont, fill=255)
        self.disp.image(self.image)
        self.disp.display()

