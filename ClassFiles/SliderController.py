import tkinter as tk
import numpy as np

class SliderController:
    def __init__(self, state_space_model, update_callback):
        """
        Initialize the slider controller with the given state-space model and 
        update callback function.
        """
        self.MAX = 36  # Maximum slider range in dB
        self.state_space_model = state_space_model
        self.update_callback = update_callback

        self.init_slider()

    def init_slider(self):
        """
        Initialize a single slider to control the gain for output feedback.
        """
        self.root = tk.Tk()
        self.root.title("Output Feedback Gain Control")

        # Create slider for gain with logarithmic scaling (in dB)
        self.gain_slider = tk.Scale(
            self.root,
            from_=-self.MAX, to=self.MAX,  # dB range from -36 to 36
            resolution=0.1,                # Set slider resolution
            orient='horizontal',
            length=300,
            label='Output Feedback Gain (dB)',
            command=self.update_gain
        )
        self.gain_slider.set(0)  # Set initial gain to 0 dB (corresponding to gain=1.0)
        self.gain_slider.pack(padx=10, pady=10)

    def update_gain(self, db_value):
        """
        Update the gain value in the state-space model based on slider input.
        """
        # Convert dB value to linear scale
        linear_gain = 10 ** (float(db_value) / 20)

        # Update the gain in the state-space model
        self.state_space_model.update_gain(linear_gain)

        # Call the update callback function to refresh the eigenvalue plot
        self.update_callback()

    def start(self):
        """
        Start the Tkinter main loop to display the GUI.
        """
        self.root.mainloop()
