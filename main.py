from ClassFiles.AudioLoader import AudioLoader  # Import the AudioLoader class
from ClassFiles.ControlSystemSimulation import ControlSystemSimulation
from ClassFiles.StateFeedbackControllerSimulation import StateFeedbackController
from ClassFiles.MainController import MainController

def main():
    # Create an instance of AudioLoader
    print("Creating AudioLoader instance...")
    al = AudioLoader()

    # Specify the duration in seconds to read
    time_test = 20  # Time duration for input/output audio data

    # Load the input audio signal for a specified time period
    print("\nPlease select the .wav file for the input audio signal")
    input_data, sampling_rate = al.load_audio(time_test)
    print("Input audio signal loaded.")

    # Load the output audio signal for the same time period
    print("\nPlease select the .wav file for the output audio signal")
    output_data, _ = al.load_audio(time_test)
    print("Output audio signal loaded.")

    # Specify the order of the system for simulation
    system_order = 149
    # system_order = 2

    # Set up the control system simulation
    print("Setting up the control system simulation...")
    simulation = ControlSystemSimulation(n=system_order, t_end=time_test, num_points=len(input_data))

    # Identify the system using SRIM method
    print("Identifying system using SRIM method...")
    SRIM_plant_system = simulation.identify_system_SRIM(input_data, output_data)
    print("System identification completed.")

    # Set up the State Feedback Controller
    print("Setting up State Feedback Controller...")
    SFC = StateFeedbackController(
        n=system_order, 
        plant_system=SRIM_plant_system, 
        ideal_system=None, 
        input_signal=input_data, 
        test_signal=None, 
        sampling_rate=sampling_rate, 
        F_ini=None, 
        F_ast=None
    )

    # Simulate the system and get the output signals
    print("Running the State Feedback Controller simulation...")
    SFC.optimal_equalization()
    print("Simulation completed.")

    # Specify the CSV file path for the discrete system matrices
    input_file = './output/plant_system_discrete_matrices.csv'

    # Create an instance of MainController
    main_controller = MainController(input_file)

    # Start the slider control
    main_controller.slider_controller.start()

if __name__ == '__main__':
    main()
