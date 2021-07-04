import serial
import functools


def log_function_call(f): 
    @functools.wraps(f)  # wraps is a decorator that tells our function to act like f
    def log_f_as_called(*args, **kwargs):
        print(f'{f.__name__} was called with arguments={args} and kwargs={kwargs}')
        value = f(*args, **kwargs)
        print(f'{f.__name__} return value {value}')
        return value
    return log_f_as_called

@log_function_call
def get_connection_object():
    try:
        ser = serial.Serial('/dev/ttyUSB0')  # open serial port
        print(ser)
    except:
        print("Error")
    finally:
        pass
        #ser.close()
    return(True)

@log_function_call
def setup():
    conn = get_connection_object()
    #Check connection object
    return(conn)

@log_function_call
def check_safe_environment():
    rv = False
    #Check latches ect
    rv = True #For testing purposes
    return(rv)

@log_function_call
def activate_relay(conn, pin):
    try:
        #Send message to activate pin
        return(True)
    except:
        return("This is an error!")

@log_function_call
def get_data_from_conn(conn):
    data_entry = [1,4.5,4.8,5,12,6]
    return(data_entry)

@log_function_call
def log_data(data, data_entry):
    n = 0
    for key in data.keys():
        data[key].append(data_entry[n])
        n += 1
    return(data)

@log_function_call
def data_to_csv(data):
    pass

@log_function_call
def check_exit_conditions(data_entry):
    return(True)