"""
Code for NU Marine at UON:
JANICE -- Just Another Non-Intelligent Capacity Evaluation
AIMS:
 - Collect voltage data from battery cells over time
 - Use CSV data to derive model of batteries (in separate program)

PROCESS:
    - Start in startup state
    - Ensure environment safe before starting battery discharge
    - Send message to activate discharge relay on board
    - Start discharge loop
        - sample voltage data
        - logg data
        - checking for exit conditions
    - When voltage on a cell gets low enough stop the test by turning the relay off
    - Send message to activate charging relay on board (not yet implemented)
    - Start charge loop (not yet implemented)
        - sample voltage data
        - logg data
        - checking for exit conditions
    - Format the data as a CSV and export (not properly implemented, but simulated function exists)

TODO:
    - Add discharge states / data
    - Add unit tests ??
    - More interesting battery simulation
    - Investigate getting internal resistance from data?
    - Retwig simulation to have more realistic state machine speed. (State machine takes one second per function execution which is not realistic)
    - General code cleanup and formatting. It's a bit messy.
    - Remove function get_exit_condition -- no longer required.
"""
# imports
import environment as sim
import time
import logging as log
from matplotlib import pyplot as plt

# Variables
t = 0  # Time in seconds, set to start at 0 by default
dt = 1  # delta time, how long each timestep will be
tMax = 10  # Simulation runtime in Hours
# Number of cells in test. Note I'm not splitting them into batteries anywhere in code. That's assumed to have done by the users. Eg on paper.
number_of_cells = 8

time_delay_for_safe_environment = 2  # Time in seconds between
# When tried, will the discharging relay fail? True = Yes, False = No
discharging_relay_fail = False

# Function storage for state machine. NOTE: They are here in the main file, so I don't have to specifically put in code or pass extra variables, to get access to the environment object and its funcitons.


def activate_relay(rv):
    """Attempts to activate the discharging relay.
    """
    try:
        A.try_activate_relay()
    except:
        log.warning("Charging relay failed to activate!")
        rv = 10  # Emergency state
    finally:
        return(rv)


def setup_state(message):
    """The system is initilised in this state. A check is performed to check if the system is safe, and only when the systems is deemed to be safe, is the next state variable returned.
    """
    log.info("setup_state({0})".format(message))
    rv = 0
    check_safe = A.environment_safe
    if(check_safe):
        log.info("Environment safe!")
        rv = 1
        rv = activate_relay(rv)

    else:
        log.warning("Environment not safe!")
    return(rv, message)


def comms_in(message):
    """Checks for communications from the battery management system. In future versions the program may wait in this state for a communication before moving on. 
    """
    log.info("comms_in({0})".format(message))
    new_state = 2
    # In this simulation the messages need to be called from the environment.
    message = A.get_message()
    return(new_state, message)


def log_data(message):
    """Logs the data to a seperate structure for later plotting and output.

    Args:
        message (str): A string containing each cells value. This is formulated as a list for the moment.
    """
    log.info("log_data({0})".format(message))
    new_state = 3
    if(not(message == False)):
        for i in range(len(message)):
            cell_voltage = message[i]
            cell_info[i].append(cell_voltage)
        time_data.append(t)
        log.info("Cell voltage: {}".format(cell_voltage))
    return(new_state, message)


def check_exit_conditions(message):
    """Checks to see if exit conditions have been reached. I.e if some of the battery cells have reached their peak, or if a current sensor indicates the batteries are shorting.

    Args:
        message (str): A string containing each cells value. This is formulated as a list for the moment.
    """
    log.info("check_exit_conditions({0})".format(message))
    new_state = 1
    #exit_condition = A.get_exit_condition()
    exit_condition = False
    for cell in message:
        if(cell <= 1.5):
            exit_condition = True
    if(exit_condition):
        new_state = 4
        log.info("Exit perameters met!")
    return(new_state, message)


def output_data_as_csv():
    """This funciton is a placeholder, but will format and output the final CSV data.
    """
    log.info("output_data_as_csv({0})".format(message))


def emergency_state():
    """Emergency state for the test. Turns everything off, logs data and terminates.
    """
    # Log about it
    log.critical("Emergency state entered")
    print("Emergency state entered")
    # Log debug info
    # Turn everything off
    # Make safe
    # Terminate
    quit()


def battery_testing_state_maching(state_variable, message):
    """JANICE's sate machine. On each timestep the state will update. Note this is unrealistic but will be changed in future.

    Args:
        state_variable (int): An int indicating the current state of the state machine.
        message (str): A string containing each cells value. This is formulated as a list for the moment.
    """
    new_state = "No idea"
    if(state_variable == 0):
        new_state, message = setup_state(message)
    elif(state_variable == 1):
        new_state, message = comms_in(message)
    elif(state_variable == 2):
        new_state, message = log_data(message)
    elif(state_variable == 3):
        new_state, message = check_exit_conditions(message)
    elif(state_variable == 4):
        output_data_as_csv()
        return(6, 6)
    elif(state_variable == 10):
        # Emergency state
        emergency_state()
    return(new_state, message)


# Setup
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
log.basicConfig(filename="JANICE.log", level=log.INFO,
                format=LOG_FORMAT, filemode='w')
logger = log.getLogger()
log.info("Program START")

tMax *= (60 * 60)  # Convert the maximum simulation time from hours to seconds
continue_test_flag = True  # initialised to True so the test can start
# Initialised to 0, such that the state machine enters the setup state first
state_variable = 0
A = sim.environment(time_delay_for_safe_environment,
                    number_of_cells, tMax, discharging_relay_fail)
cell_info = []
time_data = []
# accidental feature, but it means that if nothing else, it'll run emergency state first.
message = 10

for i in range(number_of_cells):
    cell_info.append([])

# Main loop
while(continue_test_flag):
    A.update_environment(t)
    state_variable, message = battery_testing_state_maching(
        state_variable, message)

    # update time
    t += dt

    if(t > (tMax + 100)):
        print("Emergency cutoff")
        log.warning("Emergency cutoff!")
        continue_test_flag = False
    if(state_variable == 6):
        print("Rounds complete.")
        log.info("Program finshed")
        continue_test_flag = False
    # Output
    log.info("Current state: {0}".format(state_variable))

# Graphs because why not?
for data in cell_info:
    plt.plot(time_data, data)
plt.ylabel("Voltage (V)")
plt.xlabel("Time (S)")
plt.title("Voltage vs time for each cell")
plt.show()
