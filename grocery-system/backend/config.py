# Import os module to access environment variables from the system
import os

# Import create_client function and Client class from Supabase library
from supabase import create_client, Client

# Import load_dotenv to load variables from .env file
from dotenv import load_dotenv


# Load all environment variables from the .env file
# Example:
# SUPABASE_URL=your_url
# SUPABASE_KEY=your_key
load_dotenv()


# Get Supabase project URL from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")

# Get Supabase API key from environment variables
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Check if URL or KEY is missing
# If missing, stop the program and show an error message
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY are missing from .env")


# Create a connection/client object for Supabase
# This object will be used to:
# - insert data
# - fetch data
# - update records
# - delete records
# from your Supabase database
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)