# Configuration file for Sciris

# This file gets sourced by the Python code to extract parameters for setting 
# which directories the web application uses, which Redis database gets used, 
# and whether new registered accounts are automatically activated or not.

# NOTE: For the _DIR parameters, you can use full absolute paths also.  If 
# you use a relative path, it is interpreted as being with respect to the 
# root path of the main repository.

# Last update: 2018apr21

import os

# A secret key value used by Python Flask.
SECRET_KEY = 'Pick something unique for your site here'

# Grab the directory up one level from where we are (/bin).
ROOT_DIR = os.path.abspath(os.pardir) + os.sep

# Directory containing the client code.
CLIENT_DIR = ROOT_DIR + 'vueinterface'

# Directory containing the model code.  This is the primary Python code that 
# the web app will rely on related to the actual model.
MODEL_DIR = ROOT_DIR + 'scirismodel'

# Directory containing Python code specific to the web app.  sessionmanager 
# (the directory this config file is in) contains general Python functionality 
# that the web app directory code makes use of. 
WEBAPP_DIR = ROOT_DIR + 'webapp'

# Directory where uploaded files will be saved, as well as files saved to be 
# downloadable to user machines.
UPLOADS_DIR = ROOT_DIR + 'uploads'

# Directory where files may be saved that the web app should be able to 
# access.
FILESAVEROOT_DIR = ROOT_DIR + 'savedfiles'

# URL for the Redis database that the web app will use to manage 
# persistence.  Note that the /N/ number at the end should match the 
# database number you want to use.  (N=0 is the default Redis database.)
REDIS_URL = 'redis://localhost:6379/4/'

# Flag for setting whether registration of a new account automatically 
# spawns a new active account.  If this is set False, then an admin user has 
# to manually activate the account for the user.
REGISTER_AUTOACTIVATE = True