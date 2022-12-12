import pigpio
import numpy as np

import sys
import time
import logging

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(levelname)s:%(message)s'
    )

logging.info('Loading Variables...')

GPIO = 27

N_BITS = 16*100
N_TIME_CAPTURES = N_BITS + 2 + 1
MEASURE = True

capture_array = np.array((N_TIME_CAPTURES, 2))
i=0

def array_write(gpio, level, tick):
    logging.debug(f'Function callback {i}. Meassure {MEASURE}')
    capture_array[i] = tick, level
    i += 1
    if i == (N_TIME_CAPTURES - 1):
            cb.cancel()
            MEASURE = False

start_time = time.time()

logging.info('Setting Pi connection...')
# Connect to local Pi
pi = pigpio.pi() 

# Check if Pi is Connected
if not pi.connected:
    logging.error('Could not identify Pi connection.')    
    sys.exit()

logging.info('Configuring input and sampling...')
# Define Pi's input
pi.set_mode(GPIO, pigpio.INPUT)
# Set it to down, i.e., 0 
pi.set_pull_up_down(GPIO, pigpio.PUD_DOWN)

# Define the callback that will execute the sampling
cb = pi.callback(GPIO, pigpio.RISING_EDGE, array_write)
logging.info('Configuring input and sampling...')

logging.info(f'Sampling the gpio {GPIO}. It may take a while...')
while MEASURE:
    try:
        logging.debug(f'Executing sampling.')
    except KeyboardInterrupt:
        logging.warning(f'Sampling interrupted by keyboard action.')
        break
                
 

end_time = time.time()

logging.info(f'Finished sampling.')
logging.info(f'Execution time: {end_time - start_time}')

logging.info(f'Saving the sampling values file...')
np.savetxt(capture_array, "peaksfile_" + str(start_time) + ".csv", delimiter=",")

logging.info(f'All done.')

pi.stop()

