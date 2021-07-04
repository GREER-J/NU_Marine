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
    - Add unit tests ?? Have to mock functions. Will replace environment.py
    - More interesting battery simulation
    - Investigate getting internal resistance from data?
    - Retwig simulation to have more realistic state machine speed. (State machine takes one second per function execution which is not realistic)
    - General code cleanup and formatting. It's a bit messy.
    - Remove function get_exit_condition -- no longer required.
    - Implement logging with decorators instead of inside the individual functions.
    - Move JANICE to it's own class? Adv better data transfer Dis less readability for engineers
    - Write dummy function with Pyserial to connect and test a connection
    - Employ function annotations for better documentation ect
"""


# imports
import time
import logging as log
from matplotlib import pyplot as plt
from JANICE import *

# Variables
e_stop = True
e_stop_val = 1000
e = 0
state = 0
charge = 10 #Representing a pin number or something
discharge = 11 # A/A Pin number

#Start logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
log.basicConfig(filename="JANICE.log", level=log.INFO,
                format=LOG_FORMAT, filemode='w')
logger = log.getLogger()
logger.info("Program START")


cells = 5
data = {'time':[]}

for i in range(cells):
    data['vol_{}'.format(i)] = []


while(True):
    if(e_stop):
        e += 1
    if(state == 0):
        #START HERE Get connection object
        conn = setup()
        state = 1

    elif(state == 1):
        #Check environment safe
        safe = check_safe_environment()
        if(safe):
            state = 2
    elif(state == 2):
        #Activate board relay
        activate_relay(conn,charge)
        state = 3
    
    #Loop 1
    elif(state == 3):
        #Sample voltage
        data_entry = get_data_from_conn(conn)
        state = 4
    elif(state == 4):
        #Log data
        data = log_data(data, data_entry)
        state = 5
    elif(state == 5):
        #Check exit conditions
        if(check_exit_conditions(data_entry)):
            state = 6
        else:
            state = 3
    
    elif(state == 6):
        #Activate charging relay
        activate_relay(conn,discharge)
        state = 7
    
    #Loop 2
    elif(state == 7):
        #Sample voltage
        data_entry = get_data_from_conn(conn)
        state = 8
    elif(state == 8):
        #Log data
        data = log_data(data, data_entry)
        state = 9
    elif(state == 9):
        #Check exit conditions
        if(check_exit_conditions(data_entry)):
            state = 10
        else:
            state = 7
    
    elif(state == 10):
        #Make safe
        state = 11
    elif(state == 11):
        #Format CSV data
        data_to_csv(data)
        state = 12


    elif(state == 12):
        #END HERE
        pass
    
    elif(state == 13):
        #Emergency state
        pass
    
    if(e_stop):
        if(e >= e_stop_val):
            print("E stop hit!")
            break
print(data)
