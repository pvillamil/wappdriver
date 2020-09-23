'''This module local.py provides access to local data. It can read and write local data
---
This module also provides functions to  make the data files dynamic.
The values of the selectors are updated from the internet, first time when the user runs wappdriver
---
Updates can be performed manually by calling `update_vars()`
'''

from . import remote
import os
import yaml
from datetime import datetime
from .. import __version__


wapp_dir = os.path.expanduser('~/.wappdriver')

log_file = os.path.join(wapp_dir, 'log_file.txt')
cdp_file = os.path.join(wapp_dir, 'cdp.txt')
var_file = os.path.join(wapp_dir, 'var.yml')

version_file = os.path.join(wapp_dir, 'ver.txt')

sessions_dir = os.path.join(wapp_dir,'sessions')

def set_chrome_driver_path(path=''):
    '''
    Writes the absolute path of installation of Chrome Driver Executable
    in `chrome_driver_path.txt` file in `.wappdriver` directory 
    which exists at the home directory of the user
    ---

    - if the argument `path` is provided, sets the value to path
    - otherwise prompts for user input
    ---

    Validation of `path` and whether correct version is installed or not 
    are done by `test_browser` module of the `tests` package
    '''

    while path == '':
        path = input('''
        -------------------------------------------------------------
        Paste the absolute path of the installation of Chrome Driver
        You have to enter this only once
        -------------------------------------------------------------
        ''').strip()

    with open(cdp_file, 'w+') as f:
        f.write(path)


def get_chrome_driver_path():
    '''Returns the chrome driver path
    first line from `chrome_driver_path.txt` file in `.wappdriver` directory 
    which exists at the home directory of the user.
    ---
    If error arises, calls `set_chrome_driver_path()`
    '''
    try:
        with open(cdp_file, 'r') as f:
            path = f.readline().strip()
            return path
    except Exception as e:
        print('Could not Read Chrome Driver Path')
        print(f'Some Error Occured {e}')
        set_chrome_driver_path()


def set_local_vars(vars):
    '''
    Takes a string and writes that into `var.yml` inside `.wappdriver` 
    '''
    with open(var_file, 'w+') as f:
        f.write(vars)


def get_local_vars():
    ''' 
    Returns the vars dictionary
    '''
    with open(var_file, 'r') as f:
        return yaml.full_load(f)


def set_local_ver(ver):
    '''
    Takes a string and writes that into `ver.txt` inside `.wappdriver` 
    '''
    with open(version_file, 'w+') as f:
        f.write(ver)


def get_local_ver():
    ''' 
    Returns the value of version of `var.yml` inside `.wappdriver`, as a float
    '''
    with open(version_file, 'r') as f:
        return float(f.readline())


def update_vars():
    ''' Checks for updates in var.yml, if availaible, updates the local data
    Usually takes a few seconds to run, calling this function 
    at the beginning of your script ensures that the values of xpath and css selectors used 
    for automation are up to date with the latest version of WhatsApp Web.

    Returns True on success
    If failed
    - returns False
    - raises and catches WappDriver Error, and prints it. 

    '''

    local_version = get_local_ver()
    remote_version = remote.version()

    try:
        if remote_version > local_version:
            set_local_vars(remote.fetch_vars())
            set_local_ver(str(remote_version))

        return True

    except Exception as e:
        f'Could not update data from Internet. Check your internet connection \n {e}'


def ensure():
    '''
    Executed whenever local is imported, please run `ensure()` to ensure the required local files exists.
    If those files do not exist, ensures the creation of them with proper initial values.
    '''

    if not os.path.exists(wapp_dir):
        os.mkdir(wapp_dir)

    if not os.path.exists(log_file):
        with open(log_file, 'w+') as f:
            f.write(f'''
            --------------------------
            Log File Created
            {datetime.now()}
            wappdriver : {__version__}
            ---------------------------\n
            ''')

    if not os.path.exists(cdp_file):
        set_chrome_driver_path()

    if not os.path.exists(version_file):
        set_local_ver('0')

    if not os.path.exists(var_file):
        update_vars()

    if not os.path.exists(sessions_dir):
        os.mkdir(sessions_dir)
