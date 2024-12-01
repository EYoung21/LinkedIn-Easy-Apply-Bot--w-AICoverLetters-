import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

def load_config():
    with open('config.yaml', 'r') as file:
        # Load the YAML template
        config = yaml.safe_load(file)
        
        # Replace environment variables
        config['username'] = os.getenv('USERNAME')
        config['password'] = os.getenv('PASSWORD')
        config['phone_number'] = os.getenv('PHONE_NUMBER')
        
        # Update file paths
        config['uploads']['Resume'] = os.getenv('RESUME_PATH')
        config['uploads']['Cover Letter'] = os.getenv('CV_PATH')
        config['resume_path'] = os.getenv('RESUME_PATH')
        
        return config

# Usage
config = load_config()