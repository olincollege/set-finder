"""
Module to contain user display functions.
"""
import math
import random
import threading
import tkinter as tk
from tkinter import filedialog, Tk
from tkinter import ttk
from tkinter.constants import TOP, BOTH
import numpy as np
import cv2
from PIL import ImageTk
from PIL import Image as ImagePL
from Card import Card
from Image import Image
from Controller import Controller


class View:
    """
    Class for displaying SET boards.

    Attributes:
        image: A cv2.Mat type image showing the full board
    """

    def __init__(self, image):
        self._controller = Controller(0)
        self.image = image
        self.submit_thread = None

        # Create an instance of tkinter frame
        top = Tk()
        top.geometry()
        self.top = top
        # Create a Label to display the image
        # Label(win, image= imgtk).pack()
        top.title("Toplevel 0")
        top.configure(highlightcolor="black")
        self._set_gui_image()
        label = tk.Label(top, image=self.img_gtk)  # Where image is inserted
        label.pack(fill=BOTH, expand=False, padx=10, pady=10, side=TOP)
        label.configure(activebackground="#f9f9f9")
        label.configure(anchor="w")
        label.configure(compound="left")

        self.label = label

        progress_bar = ttk.Progressbar(top, mode="indeterminate")
        progress_bar.pack()
        progress_bar.configure(length="540")

        self.progress = progress_bar
        t_separator = ttk.Separator(top)
        t_separator.pack()
        t_frame = ttk.Frame(top, height=75)
        t_frame.pack(fill=BOTH, expand=True)
        t_frame.configure(relief="groove")
        t_frame.configure(borderwidth="2")
        t_frame.configure(relief="groove")

        run_again = tk.Button(t_frame, command=self.start_submit_thread)

        run_again.place(relx=0.78, rely=0.266, height=33, width=73)
        run_again.configure(activebackground="beige")
        run_again.configure(borderwidth="2")
        run_again.configure(compound="left")
        run_again.configure(text="Get File")
        self.button = run_again

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
        for a_set in list_cards:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            for card in a_set:
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
        filename = filedialog.askopenfilename()
        self.image = cv2.imread(filename)
        print("Processing...")
        im = Image(self.image)
        print("finding cards")
        im.create_cards()
        print("finding sets")
        im.find_sets()
        print("drawing cards")
        self.draw_nonset_cards(im.get_cards_nonset())
        self.draw_set_cards(im.get_cards_set())
        self.image = cv2.resize(self.image, (640, 480))
        self._set_gui_image()
        self.label.config(image=self.img_gtk)
        print("Done")

    def _set_gui_image(self):
        im = ImagePL.fromarray(self._correct_color())
        self.img_gtk = ImageTk.PhotoImage(image=im)

    def _correct_color(self):
        """
        Helper function to convert image color
        """
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def show(self):
        """
        Display board state to the user.
        """
        self.top.mainloop()

    def start_submit_thread(self):
        self.button["state"] = "disabled"
        self.submit_thread = threading.Thread(target=self.new_image)
        self.submit_thread.daemon = True
        self.progress.start()
        self.submit_thread.start()
        self.top.after(20, self.check_submit_thread)

    def check_submit_thread(self):
        if self.submit_thread.is_alive():
            self.top.after(20, self.check_submit_thread)
        else:
            self.progress.stop()
            self.button["state"] = "normal"


if __name__ == "__main__":
    # Code to check if view is working
    view = View(cv2.imread("boards/1.jpg"))
    view.show()
