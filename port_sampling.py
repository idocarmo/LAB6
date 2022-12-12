import pigpio
import numpy as np
import time

GPIO = 27

N_BITS = 16*100
N_TIME_CAPTURES = N_BITS + 2 + 1
MEASURE = True
capture_array = np.array((N_TIME_CAPTURES, 2))
i=0

def array_write(gpio, level, tick):
    capture_array[i] = tick, level
    i += 1

sart_time = time.time()

# Connect to local Pi
pi = pigpio.pi() 

# Check if Pi is Connected
if not pi.connected:
    print("ERROR: Pi is not connected")    
    exit(0)

# Defining Pi's input
pi.set_mode(GPIO, pigpio.INPUT)
# Set it to down, i.e., 0 
pi.set_pull_up_down(GPIO, pigpio.PUD_DOWN)

# Define the callback that will 
cb = pi.callback(GPIO, pigpio.RISING_EDGE, array_write)


while MEASURE:
    try:
        if i == (N_TIME_CAPTURES - 1):
            MEDIR = False
    except KeyboardInterrupt:
        cb.cancel()
        np.savetxt(capture_array, "logfile_" + str(start_time) + ".csv", delimiter=",")
        break
        
        
cb.cancel() 

end_time = time.time()

np.savetxt(capture_array, "logfile_" + str(start_time) + ".csv", delimiter=",")



pi.stop()

