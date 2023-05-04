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

    def __init__(self):
        self._controller = Controller()
        self.submit_thread = None

        # Create an instance of tkinter frame
        top = Tk()
        top.geometry()
        self.top = top
        # Create a Label to display the image
        # Label(win, image= imgtk).pack()
        top.title("Toplevel 0")
        top.configure(highlightcolor="black")
        self._set_gui_image(self._controller.get_image())
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

    
    def run(self):
        """'
        Run program again to capture image.
        """
        try:
            filename = filedialog.askopenfilename(filetypes=[("JPEG images","*.jpg"),("PNG images","*.png")])
            self._controller.read_image(filename)
        except:
            return
        self._controller.generate_image_overlay()
        self._set_gui_image(self._controller.get_image())
        self.label.config(image=self.img_gtk)
        print("Done")

    def _set_gui_image(self,image_cv2):
        self.im_ref = ImagePL.fromarray(image_cv2)
        self.img_gtk = ImageTk.PhotoImage(image=self.im_ref)

    def show(self):
        """
        Display board state to the user.
        """
        self.top.mainloop()

    def start_submit_thread(self):
        self.button["state"] = "disabled"
        self.submit_thread = threading.Thread(target=self.run)
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
    view = View()
    view.show()
