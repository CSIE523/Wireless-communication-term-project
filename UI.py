import numpy as np
import cv2
import random
import time
from math import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from untitled import *
import sys

height = 2500
width = 2500
img = np.zeros((height, width, 3), np.uint8)
img.fill(0)

black = (0, 0, 0)
white = (255, 255, 255)
blue = (255, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)
img = np.zeros((height, width, 3), np.uint8)
img.fill(0)
base = []
car_list = []
total_car = 0
start_global = start = time.time()
algo_time1 = 0
calling_people = 0
algo1_times = 0
threshold1 = 20
algo2_times = 0
threshold3 = 25
algo3_times = 0
algo4_times = 0
duration = 0.0
car_id = 0


def path_loss(a, b, f):
    return 87.55-20*log10(f)-20*log10(sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)*0.01)

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
    def labelupdate(self):
        self.label_7.setText(str(total_car))
        self.label_8.setText(str(calling_people))
        self.label_9.setText(str(algo1_times))
        self.label_10.setText(str(algo2_times))
        self.label_11.setText(str(algo3_times))
        self.label_12.setText(str(algo4_times))

for i in range(9):
    cv2.line(img, (0, 250+250*i), (2500, 250+250*i), (255, 255, 255), 16)
    cv2.line(img, (250+250*i, 0), (250+250*i, 2500), (255, 255, 255), 16)


for i in range(9):
    for j in range(9):
        set = random.random()
        if set >= 0.1 and set < 0.2:
            dis = random.random()
            if dis < 0.25:
                cv2.circle(img, (125 + 250*i, 125 + 250 * j - 10), radius=10, color=green, thickness=-1)
                base.append((125 + 250*i, 125 + 250 * j - 10))
            elif dis >= 0.25 and dis < 0.5:
                cv2.circle(img, (125 + 250 * i, 125 + 250 * j + 10), radius=10, color=green, thickness=-1)
                base.append((125 + 250 * i, 125 + 250 * j + 10))
            elif dis >= 0.5 and dis < 0.75:
                cv2.circle(img, (125 + 250 * i - 10, 125 + 250 * j), radius=10, color=green, thickness=-1)
                base.append((125 + 250 * i - 10, 125 + 250 * j))
            elif dis >= 0.75 and dis < 1:
                cv2.circle(img, (125 + 250 * i + 10, 125 + 250 * j), radius=10, color=green, thickness=-1)
                base.append((125 + 250 * i + 10, 125 + 250 * j))

class Car:
    def __init__(self, id):
        self.id = id
        self.alive = True
        self.call = False
        self.call_start = 0
        self.call_time = 0
        self.call_time_glob = int(np.random.normal(180, 3.2, 1))
        self.algo1_connected = -1
        self.algo2_connected = -1
        self.algo3_connected = -1
        self.algo4_connected = -1
        self.site = random.randint(0, 35)

        if int(self.site/9) == 0:
            self.x = 0
            self.y = 250*((self.site % 9)+1)
            self.dir = 0  #right
        elif int(self.site/9) == 1:
            self.x = 250*((self.site % 9)+1)
            self.y = 2500
            self.dir = 1  #up
        elif int(self.site/9) == 2:
            self.x = 2500
            self.y = 250*((self.site % 9)+1)
            self.dir = 2  #left
        else:
            self.x = 250*((self.site % 9)+1)
            self.y = 0
            self.dir = 3  #down

    def update(self):
        global total_car, call_time_glob, calling_people, algo1_times, threshold1, algo2_times, threshold3, algo3_times, algo4_times
        if self.alive == True:
            if self.x < 0 or self.y < 0 or self.x > 2500 or self.y > 2500:
                if self.call == True:
                    calling_people -= 1
                self.alive = False
                total_car -= 1

            x_dir = {0: 1, 1: 0, 2: -1, 3: 0}
            y_dir = {0: 0, 1: -1, 2: 0, 3: 1}
            rand = random.random()
            if self.x > 0 and self.x < 2500 and self.y > 0 and self.y < 2500 and self.x % 250 == 0 and self.y % 250 == 0:
                if rand < 1/2:  # foward
                    self.x += x_dir[self.dir]
                    self.y += y_dir[self.dir]
                elif rand < 1/2 + 7/32 and rand >= 1/2:  # right
                    self.dir -= 1
                    if self.dir < 0:
                        self.dir += 4
                    self.x += x_dir[self.dir]
                    self.y += y_dir[self.dir]
                elif rand < 1/2 + 7/16 and rand >= 1/2 + 7/32:  # left
                    self.dir += 1
                    if self.dir > 3:
                        self.dir -= 4
                    self.x += x_dir[self.dir]
                    self.y += y_dir[self.dir]
                elif rand < 1 and rand >= 1/2 + 7/16:  # back
                    if self.dir == 0:
                        self.dir = 2
                    elif self.dir == 1:
                        self.dir = 3
                    elif self.dir == 2:
                        self.dir = 0
                    else:
                        self.dir = 1
                    self.x += x_dir[self.dir]
                    self.y += y_dir[self.dir]
            else:
                self.x += x_dir[self.dir]
                self.y += y_dir[self.dir]

            if self.call == False and rand < 0.0003:
                self.call = True
                self.call_start = time.time()
                calling_people += 1
            if self.call == True:
                self.call_time = time.time() - self.call_start

                sig_list = []
                for b in base:
                    sig_list.append(round(path_loss((self.x, self.y), b, base.index(b)*100+100), 2))

                val = max(sig_list)
                strong = sig_list.index(val)

                if self.call_time < 0.001:
                    self.algo1_connected = strong
                    self.algo2_connected = strong
                    self.algo3_connected = strong
                    self.algo4_connected = strong


                # algorithm 1
                if sig_list[self.algo1_connected] < threshold1 and self.algo1_connected != strong:
                    self.algo1_connected = strong
                    algo1_times += 1

                # algorithm 2
                if sig_list[self.algo2_connected] < sig_list[strong]:
                    self.algo2_connected = strong
                    algo2_times += 1

                # algorithm 3
                if (sig_list[strong] - sig_list[self.algo3_connected]) > threshold3:
                    self.algo3_connected = strong
                    algo3_times += 1

                # algorithm 4
                if sig_list[self.algo4_connected] < (sum(sig_list)/len(sig_list)) and self.algo4_connected != strong:
                    self.algo4_connected = strong
                    algo4_times += 1

                if self.call_time > self.call_time_glob:
                    self.call = False
                    self.call_time = 0
                    calling_people -= 1

    def display(self):
        global car_list
        if self.alive:
            if self.call == True:
                cv2.circle(img, (self.x, self.y), 8, red, -1)
            else:
                cv2.circle(img, (self.x, self.y), 8, blue, -1)
        else:
            car_list.remove(self)
            del self

    def clear_display(self):
        if self.alive:
            cv2.circle(img, (self.x, self.y), 8, white, -1)

def create_car():
    car = Car(1)
    while True:
        car.update()
        car.display()
        cv2.imshow('img', img)
        car.clear_display()


def append_car():
    global duration, total_car, start, car_id, calling_people
    if duration > 0.005:
        car_list.append(Car(car_id))
        total_car += 1
        car_id += 1
        duration = 0.0
        start = time.time()

    duration = time.time() - start


def update_car():

    for car in car_list:
        car.update()
        car.display()
    cv2.namedWindow("img", 0)
    cv2.resizeWindow("img", 1400, 900)
    cv2.imshow('img', img)
    cv2.waitKey(1)
    for car in car_list:
        car.clear_display()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    while True:
        append_car()
        update_car()
        window.labelupdate()
    #sys.exit(app.exec_())