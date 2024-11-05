import tkinter as tk

class InvertController:
    def __init__(self, state_space_model, update_callback):
        """
        Initialize the invert controller with the given state-space model and 
        update callback function.
        """
        self.state_space_model = state_space_model
        self.update_callback = update_callback

        self.invert_window = None
        self.init_invert_window()

    def init_invert_window(self):
        """
        Create a separate window with an Invert switch to control the sign of 
        the gain value in the output feedback.
        """
        self.invert_window = tk.Toplevel()
        self.invert_window.title("Gain Invert Control")

        # Create an invert switch for the gain
        self.sign_var = tk.IntVar(value=0)  # 0: positive, 1: inverted
        invert_switch = tk.Checkbutton(
            self.invert_window,
            text="Invert Gain Sign",
            variable=self.sign_var,
            command=self.toggle_gain_sign
        )
        invert_switch.pack(padx=10, pady=10)

    def toggle_gain_sign(self):
        """
        Toggle the sign of the gain value based on the Invert switch.
        """
        # If the switch is checked, make the gain negative; otherwise, make it positive
        if self.sign_var.get() == 1:
            self.state_space_model.gain = -abs(self.state_space_model.gain)
        else:
            self.state_space_model.gain = abs(self.state_space_model.gain)

        # Call the update callback function to refresh the eigenvalue plot
        self.update_callback()
