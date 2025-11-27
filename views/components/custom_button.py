from tkinter import Button


class CustomButton(Button):

    def __init__(self, *args, **kwargs):
        # call Button constructor with positional and keyword args
        super().__init__(*args, **kwargs)
        # custom configuration for the button
        self.config(padx=10, bg="white", bd=1, relief="solid", cursor="hand2")
