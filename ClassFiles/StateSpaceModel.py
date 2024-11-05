import numpy as np
import scipy.linalg

class StateSpaceModel:
    def __init__(self, system_matrix, input_matrix, output_matrix, feedthrough_matrix, gain=1.0, sampling_period=44.1e3):
        """
        Initialize the state-space model with system matrix A, input matrix B, 
        output matrix C, feedthrough matrix D, gain, and sampling period.
        """
        self.system_matrix = system_matrix  # A matrix
        self.input_matrix = input_matrix  # B matrix
        self.output_matrix = output_matrix  # C matrix
        self.feedthrough_matrix = feedthrough_matrix  # D matrix
        self.gain = gain  # Gain for output feedback
        self.sampling_period = sampling_period  # Sampling period

    def update_gain(self, new_gain):
        """
        Update the feedback gain and recalculate the closed-loop system.
        """
        self.gain = new_gain

    def get_discrete_A_cl(self):
        """
        Calculate the discrete-time closed-loop system matrix for output feedback (A - gain * B * C / (1 + gain * D)).
        """
        denominator = 1 + self.gain * self.feedthrough_matrix
        if denominator == 0:
            raise ValueError("The denominator 1 + gain * D cannot be zero for stability.")
        
        # A - (gain * B * C) / (1 + gain * D)
        A_cl = self.system_matrix - (self.gain * self.input_matrix @ self.output_matrix) / denominator
        return A_cl

    def get_continuous_A_cl(self):
        """
        Convert the discrete-time matrix A_cl to a continuous-time matrix.
        """
        discrete_A_cl = self.get_discrete_A_cl()
        dt = self.calculate_control_period(self.sampling_period)

        # Calculate the continuous-time matrix using the matrix logarithm
        continuous_A_cl = scipy.linalg.logm(discrete_A_cl) / dt
        return continuous_A_cl

    def calculate_eigenvalues(self):
        """
        Calculate the eigenvalues of the continuous-time closed-loop matrix A_cl.
        """
        continuous_A_cl = self.get_continuous_A_cl()
        eigenvalues = np.linalg.eigvals(continuous_A_cl)
        return eigenvalues

    def calculate_control_period(self, sampling_frequency):
        """
        Calculate the control period (sampling period) from the sampling frequency (in Hz).
        """
        return 1.0 / sampling_frequency
