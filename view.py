"""
Module to contain user display functions for the GUI.
"""
import threading
import tkinter as tk
from tkinter import filedialog, Tk
from tkinter import ttk
from tkinter.constants import BOTH, CENTER
from PIL import ImageTk
from PIL import Image as ImagePL
from controller import Controller


class View:
    """
    Class for displaying SET boards.

    Attributes:
        controller: A Controller instance shared among all View instances.
        _top: A tkinter.Tk instance representing the window root.
        _label: A tkinter.Label instance representing the GUI element for the
            image to be put into.
        _progress: A ttk.Progressbar instance representing a indeterminate
            progress bar.
        _button: A tkinter.Button instance representing the file selection
            button.
        _submit_thread: A threading.Thread instance representing the processing
            thread, separate from the GUI thread.
        _img_gtk: A PIL.ImageTk instance representing the GUI version of the
            image.
        _img_ref: A reference to the original cv2 version of the image, to
            prevent garbage collection by Tkinter.
    """

    controller = Controller()

    def __init__(self):
        """
        Create an instance of the View class.
        """
        self._submit_thread = None

        # Create an instance of tkinter frame
        self._top = Tk()
        self._top.geometry()
        self._top.title("SET Finder")
        self._top.configure(highlightcolor="black")
        self._set_gui_image(self.controller.get_image())
        self._label = tk.Label(
            self._top, image=self._img_gui
        )  # Where image is inserted
        self._label.pack(
            fill=BOTH, expand=False, padx=10, pady=10, anchor=CENTER
        )
        self._label.configure(activebackground="#f9f9f9")

        self._progress = ttk.Progressbar(self._top, mode="indeterminate")
        self._progress.pack()
        self._progress.configure(length="540")

        t_separator = ttk.Separator(self._top)
        t_separator.pack()
        t_frame = ttk.Frame(self._top, height=75)
        t_frame.pack(fill=BOTH, expand=True)
        t_frame.configure(relief="groove")
        t_frame.configure(borderwidth="2")
        t_frame.configure(relief="groove")

        self._button = tk.Button(t_frame, command=self.start_submit_thread)

        self._button.place(relx=0.78, rely=0.266, height=33, width=73)
        self._button.configure(activebackground="beige")
        self._button.configure(borderwidth="2")
        self._button.configure(compound="left")
        self._button.configure(text="Get File")

    def run(self):
        """'
        Run program again to capture image.
        """
        try:
            filename = filedialog.askopenfilename(
                filetypes=[
                    (
                        "Images",
                        ".bpm .jpg .jpeg .png .tiff .tif .pic .exr .webp",
                    )
                ]
            )
            self.controller.read_image(filename)
        except TypeError:
            return
        self.controller.generate_image_overlay()
        self._set_gui_image(self.controller.get_image())
        self._label.config(image=self._img_gui)
        print("Done")

    def _set_gui_image(self, image_cv2):
        """
        Set the GUI version of the image.
        """
        self._im_ref = ImagePL.fromarray(image_cv2)
        self._img_gui = ImageTk.PhotoImage(image=self._im_ref)

    def show(self):
        """
        Display board state to the user.
        """
        self._top.mainloop()

    def start_submit_thread(self):
        """
        Start the processing thread.
        """
        self._button["state"] = "disabled"
        self._submit_thread = threading.Thread(target=self.run)
        self._submit_thread.daemon = True
        self._progress.start()
        self._submit_thread.start()
        self._top.after(20, self.check_submit_thread)

    def check_submit_thread(self):
        """
        Check if the processing thread has finished.
        """
        if self._submit_thread.is_alive():
            self._top.after(20, self.check_submit_thread)
        else:
            self._progress.stop()
            self._button["state"] = "normal"


if __name__ == "__main__":
    # Code to check if view is working
    view = View()
    view.show()
