import os
from dotenv import load_dotenv
load_dotenv()

HOST = os.getenv('HOST')
LOGIN = os.getenv('LOGIN')
PASS = os.getenv('PASS')
SIGNIN_PAGE = os.getenv('SIGNINPAGE')
