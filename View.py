"""
Module to contain user display functions.
"""
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from Card import Card
from Image import Image
from Controller import Controller
import random
from tkinter import Tk, Label
from PIL import ImageTk
from PIL import Image as ImagePL
import time

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

class View:
    """
    Class for displaying SET boards.

    Attributes:
        image: A cv2.Mat type image showing the full board
    """

    def __init__(self, image):
        self._controller = Controller(4)
        self.image = image
        
        #Create an instance of tkinter frame
        top = Tk()
        top.geometry()
        self.top = top
        #Create a Label to display the image
        #Label(win, image= imgtk).pack()
        top.title("Toplevel 0")
        top.configure(highlightcolor="black")
        self._get_gui_image()
        Label1 = tk.Label(top,image=self.img_gtk) # Where image is inserted
        Label1.pack(fill=BOTH, expand=False,padx=10,pady=10,side=TOP)
        Label1.configure(activebackground="#f9f9f9")
        Label1.configure(anchor='w')
        Label1.configure(compound='left')

        self.label = Label1

        TProgressbar1 = ttk.Progressbar(top)
        TProgressbar1.pack()
        TProgressbar1.configure(length="540")
        
        self.progress = TProgressbar1
        TSeparator1 = ttk.Separator(top)
        TSeparator1.pack()
        TFrame1 = ttk.Frame(top,height=75)
        TFrame1.pack(fill=BOTH,expand=True)
        TFrame1.configure(relief='groove')
        TFrame1.configure(borderwidth="2")
        TFrame1.configure(relief="groove")
        IncreaseContrast = tk.Button(TFrame1)
        IncreaseContrast.place(relx=0.048, rely=0.266, height=33, width=111)

        IncreaseContrast.configure(activebackground="beige")
        IncreaseContrast.configure(borderwidth="2")
        IncreaseContrast.configure(compound='left')
        IncreaseContrast.configure(text='''+ Contrast''')
        DecreaseContrast = tk.Button(TFrame1)
        DecreaseContrast.place(relx=0.26, rely=0.266, height=33, width=112)
        DecreaseContrast.configure(activebackground="beige")
        DecreaseContrast.configure(borderwidth="2")
        DecreaseContrast.configure(compound='left')
        DecreaseContrast.configure(text='''- Contrast''')
        RunAgain = tk.Button(TFrame1,command=self.new_image) # Make new image
        RunAgain.place(relx=0.78, rely=0.266, height=33, width=73)
        RunAgain.configure(activebackground="beige")
        RunAgain.configure(borderwidth="2")
        RunAgain.configure(compound='left')
        RunAgain.configure(text='''New''')


    def draw_nonset_cards(self, list_cards):
        """
        Draws cards on the image in black.

        Args:
            list_cards: A list of Card objects representing the non-SET cards.
        """
        for card in list_cards:
            self._draw_rectangle(card, (255, 255, 255), 3)

    def draw_set_cards(self, list_cards):
        """
        Draws cards on the image in green.

        Args:
            list_cards: A list of list of Card objects representing the SET
            cards.
        """
        card_counter = {}
        for set in list_cards:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for card in set:
                self._draw_rectangle(card, color, card_counter.get(card, 0))
                card_counter[card] = card_counter.get(card, 0) + 1

    def _draw_rectangle(self, card: Card, color, ring_count):
        """
        Draws a contour on the image, offset to not overlap other contours.

        Args:
            card: A Card object.
            color: A tuple of the color to draw the rectangle.
        """
        contour_scale = (
            (size := self.image.shape)[0] * size[1]
        ) / cv2.contourArea(card.contour)
        thickness = int(math.sqrt(size[0] * size[1]) / 50)
        dilation_factor = 0.1 * ring_count * contour_scale / 30
        x_com, y_com = np.average(card.contour, axis=0)[0]
        trans = np.array([[1, 0, -x_com], [0, 1, -y_com], [0, 0, 1]])
        untrans = np.array([[1, 0, x_com], [0, 1, y_com], [0, 0, 1]])
        dilate = np.array(
            [
                [1 + dilation_factor, 0, 1],
                [0, 1 + dilation_factor, 1],
                [0, 0, 1],
            ]
        )
        contour = np.r_[
            np.transpose(np.reshape(np.array(card.contour), (4, 2), order="C")),
            [[1, 1, 1, 1]],
        ]
        translated = np.matmul(trans, contour)
        dilated = np.matmul(dilate, translated)
        reverse_trans = np.matmul(untrans, dilated)
        reshaped = np.reshape(
            np.transpose(np.delete(reverse_trans, 2, axis=0)),
            (4, 1, 2),
            order="C",
        ).astype(int)
        cv2.drawContours(self.image, [reshaped], 0, color, thickness)
    
    def new_image(self):
        """'
        Run program again to capture image.
        """
        self.progress['value']=0
        self.image = self._controller.get_image()
        print("Processing...")
        self.progress['value']=25
        # im = Image(self.image)
        time.sleep(3)
        print("finding cards")
        self.progress['value']=50
        # im.create_cards()
        time.sleep(3)
        print("finding sets")
        self.progress['value']=75
        # im.find_sets()
        time.sleep(3)
        print("drawing cards")
        self.progress['value']=100
        time.sleep(3)
        # self.draw_set_cards(im.get_cards_set())
        self._get_gui_image()
        self.label.config(image=self.img_gtk)
        print("Done")
        self.progress['value']=0

    def _get_gui_image(self):
        im = ImagePL.fromarray(self._correct_color())
        self.img_gtk = ImageTk.PhotoImage(image=im)
    
    def _correct_color(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def show(self):
        """
        Display board state to the user.
        """
        self.top.mainloop()

if __name__ == "__main__":
    # Code to check if view is working
    view = View(cv2.imread("boards/1.jpg"))
    view.show()
