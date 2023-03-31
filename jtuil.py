# Some useful utility functions

import platform
import glob
import serial
import os

def is_int(a_string):
    try:
        int(a_string)
        return True
    except ValueError:
        return False



# Get a list of .wav files from the given directory.
# By default use the Samples directory within the current working directory.
def get_sample_list(a_directory=None):
    if a_directory is None:
        a_directory = os.path.join(os.getcwd(), "Samples/")
    # return os.listdir(a_directory)
    return glob.glob(a_directory + '*.wav')
