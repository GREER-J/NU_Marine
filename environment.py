import random


class cell:
    """
    A class representing each cell of the battery.
    """

    def __init__(self, cell_name, cell_max_voltage, cell_min_voltage, cell_discharge_time):
        """The init function for a battery cell object.

        Args:
            cell_name (int): The cell number, e.g 1, 2... this is supposed to represent the cell number within the battery.
            cell_max_voltage (int): The maximum voltage the cell can charge to.
            cell_min_voltage (int): The minimum voltage the cell can charge to.
            cell_discharge_time (int): The amount of time in seconds that it will take the cell to discharge (from this a gradient is calculated).
        """
        self.cell_name = cell_name
        self.cell_max_voltage = cell_max_voltage
        self.cell_min_voltage = cell_min_voltage
        self.gradient = (cell_min_voltage - cell_max_voltage) / \
            cell_discharge_time


class environment:
    """
    A class representing the environment of the battery testing machine.
    """

    def __init__(self, safe_after_time_delay, number_of_cells, t_max, discharging_relay_fail):
        """Initilisation function for the environment.

        Args:
            safe_after_time_delay (int): The amount of time in seconds, between system startup and the simulated environment being made safe.
            number_of_cells (int): The number of cells to be tested in the system.
            t_max (int): The maximum amount of time the simulation will run in seconds.
            discharging_relay_fail (bool): Will the charging relay fail to activate? 
        """
        self.safe_time_delay = safe_after_time_delay
        self.t_max = t_max
        self.environment_safe = False
        self.exit_condition = False
        self.message = False
        self.discharging_relay_fail = discharging_relay_fail
        self.cells = []
        for i in range(number_of_cells):
            discharge_time = (4 * 60 * 60) + (random.random() * (2 * 60 * 60))
            cell_obj = cell(i, 3.3, 1.5, discharge_time)
            self.cells.append(cell_obj)

    def check_safe(self, t):
        """Checks if the simulated environment has been made safe.

        Args:
            t (int): The time since the system has been turned on in seconds.
        """
        if(t >= self.safe_time_delay):
            self.environment_safe = True

    def get_message(self):
        """Retrieves messages from the environment and returns the message. The message perameter will be "False" if no message is present.
        """
        rv = self.message
        return(rv)

    def get_exit_condition(self):
        """Retreives and returns the current exit condition of the system. The exit condition variables indicates whether the batteries are fully discharged. 
        """
        rv = self.exit_condition
        return(rv)

    def update_exit_condition(self, t):
        """Checks to see if the exit conditions of the simulation have been met. In this instance the funciton only checks whether the current system time exceeds a given maximum simulation time.

        Args:
            t (int): The time since the system has been turned on in seconds. 
        """
        if(t > self.t_max):
            self.exit_condition = True

    def sense_voltages(self, t):
        """Polls each cell in the system and uses a linear equation to calculate the current voltage.

        Args:
            t (int): The time since the system has been turned on in seconds.
        """
        for cell in self.cells:
            # These values just make the simulated data more interesting.
            noise = 0  # random.random() * .1
            cell.voltage = cell.cell_max_voltage + \
                (cell.gradient * t) + noise

    def send_message(self):
        """Simulates a message being passed from the embeded system to the main proram. In this case this is simulated by a string, containing each cell's current voltage.
        """
        val = []
        for cell in self.cells:
            val.append(cell.voltage)
        self.message = val

    def try_activate_relay(self):
        """Simulate activating the charging relay. If the simulate is setup for this to fail it will throw an error.
        """
        if(self.discharging_relay_fail):
            raise RuntimeError
        return(True)

    def update_environment(self, t):
        """Runs a collection of function that, on each time-step update the perameters of the system.

        Args:
            t (int): The time since the system has been turned on in seconds.
        """
        self.check_safe(t)
        self.sense_voltages(t)
        self.send_message()
        self.update_exit_condition(t)
