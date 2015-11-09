import os
import sys

def check_key(key_name_param):
    sys.stdout.write("Checking key %s ... " % key_name_param)
    try:
        # noinspection PyStatementEffect
        os.environ[key_name_param]
        print("OK")
    except KeyError:
        print "Missing!"

def check_virtual_env():
    sys.stdout.write("Checking virtual env ...")
    if hasattr(sys, 'real_prefix'):
        print("OK")
    else:
        print("Not running in virtual environment!")

def check_python():
    sys.stdout.write("Checking Python version ...")
    if sys.version_info > (2, 7, 10):
        print("OK ({0},{1},{2})".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    else:
        print("Problematic.")

key_names = [
    "TRELLO_API_KEY",
    "TRELLO_API_SECRET",
    "TRELLO_TOKEN",
    "TRELLO_TOKEN_SECRET",
    "SLACK_TOKEN"
]

for key_name in key_names:
    check_key(key_name)

check_virtual_env()
check_python()
