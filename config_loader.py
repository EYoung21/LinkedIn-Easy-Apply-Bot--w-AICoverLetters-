import os
from dotenv import load_dotenv
import yaml

# Load environment variables from .env file
load_dotenv()

def load_config():
    with open('config.yaml', 'r') as file:
        # Load the YAML template
        template = file.read()
        
        # Manually substitute environment variables
        template = template.replace('${USERNAME}', os.getenv('USERNAME', ''))
        template = template.replace('${PASSWORD}', os.getenv('PASSWORD', ''))
        template = template.replace('${PHONE_NUMBER}', os.getenv('PHONE_NUMBER', ''))
        template = template.replace('${RESUME_PATH}', os.getenv('RESUME_PATH', ''))
        template = template.replace('${CV_PATH}', os.getenv('CV_PATH', ''))
        
        # Load YAML after substitution
        config = yaml.safe_load(template)
        
        # Clean up positions (remove extra quotes and split properly)
        if isinstance(config['positions'][0], str):
            config['positions'] = [pos.strip() for pos in config['positions'][0].split(',')]
        
        return config

# Usage
config = load_config()