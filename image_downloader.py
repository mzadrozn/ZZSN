import random
import requests
import re
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import os
import sys


class DataRetriever:

    def __init__(self):
        URL = f"https://www.webcamgalore.com/complete-{str(sys.argv[1])}.html"
        response = str(requests.get(URL).content)
        camera_numbers = re.findall('[0-9]+\.html\"><b>', response, re.DOTALL)
        random.shuffle(camera_numbers)
        self.camera_numbers = [n.replace(".html\"><b>", "") for n in camera_numbers]
        self.winter = True
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('key_press_event', self.onnextphoto)
        self.current = None
        self.img_winter = None
        self.img_summer = None
        self.existing_files = [filename.replace(".jpg", "") for filename in os.listdir("winter")]
        if not os.path.exists("winter"):
            os.mkdir("winter")
        if not os.path.exists("summer"):
            os.mkdir("summer")
        plt.show()

    def onenter(self):
        if self.img_summer and self.img_winter:
            self.img_winter.save(f"winter/{self.current}.jpg")
            self.img_summer.save(f"summer/{self.current}.jpg")
            self.reset()
        elif self.img_winter:
            self.winter = False
        if self.winter:
            self.next()
        self.show_photo()

    def onnextphoto(self, event):
        if event.key == 'enter':
            self.onenter()
        elif event.key == 'r':
            self.show_photo()
        elif event.key == 'escape':
            self.reset()
            self.onenter()

    def reset(self):
        self.img_summer = None
        self.img_winter = None
        self.winter = True
        plt.cla()
        plt.clf()

    def show_photo(self):
        def get_next_img():
            if self.winter:
                date = f"0{random.randint(1,2)}-{random.randint(10,28)}"
            else:
                date = f"0{random.randint(5,9)}-{random.randint(10,30)}"
            img_url = f"https://images.webcamgalore.com/oneyear/{date}/{self.current}.jpg"
            data = requests.get(img_url).content
            return Image.open(BytesIO(data))
        img = get_next_img()
        counter = 0
        while img.getextrema()[0] == (255, 255):
            if counter > 2:
                self.next()
                self.reset()
                counter = 0
            counter += 1
            img = get_next_img()
        if self.winter:
            self.img_winter = img
        else:
            self.img_summer = img
        plt.imshow(img)
        plt.show()

    def next(self):
        self.current = self.camera_numbers.pop()
        while self.current in self.existing_files:
            self.current = self.camera_numbers.pop()


DataRetriever()