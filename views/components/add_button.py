from views.components.custom_button import CustomButton


class AddButton(CustomButton):

    def __init__(self, *args, **kwargs):
        # call Button constructor with positional and keyword args
        super().__init__(*args, **kwargs)
        # custom configuration for the button
        self.config(padx=10, bg="lightblue", bd=1, relief="solid", cursor="hand2")
