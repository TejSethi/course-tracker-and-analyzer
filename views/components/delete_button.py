from views.components.custom_button import CustomButton


class DeleteButton(CustomButton):

    def __init__(self, *args, **kwargs):
        # call Button constructor with positional and keyword args
        super().__init__(*args, **kwargs)
        # custom configuration for the button
        self.config(padx=10, bg="#dc143c", bd=1, relief="solid", cursor="hand2")
