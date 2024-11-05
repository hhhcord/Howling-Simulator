import numpy as np

class WarningSystem:
    def __init__(self, slider_controller):
        self.slider_controller = slider_controller

    def check_stability(self):
        """ Check the eigenvalues of (A - gain * B * C / (1 + gain * D)) and provide feedback. """
        
        # Calculate eigenvalues of the state-space model
        eigenvalues = self.slider_controller.state_space_model.calculate_eigenvalues()

        # Check for unstable eigenvalues (real part > 0)
        unstable_eigenvalues = np.any(np.real(eigenvalues) > 0)

        # Display a warning if any unstable eigenvalues are found
        if unstable_eigenvalues:
            print("Warning: The system has unstable eigenvalues!")
        else:
            print("System is stable.")
