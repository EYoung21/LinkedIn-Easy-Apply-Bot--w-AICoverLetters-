# AI-Enhanced LinkedIn EasyApply Bot

This is a fork of the [LinkedIn Easy Apply Bot](https://github.com/lorencmiki/linkedin-easy-apply-bot) with added AI capabilities for automatic cover letter generation using GPT-4.

## New Features Added
- Automatic customized cover letter generation for each job application using GPT-4
- Dynamic PDF creation and cleanup
- Intelligent job description analysis
- Resume-aware personalization
- Automatic multi-file upload management

## Setup 

### Prerequisites
Python 3.10+ using a conda virtual environment on Linux (Ubuntu) or Windows
To run the bot, first install all requirements:

```bash
pip3 install -r requirements.txt
pip3 install openai pypdf2 fpdf python-dotenv
OpenAI API Key
Create a .env file in the root directory and add your OpenAI API key:
CopyOPENAI_API_KEY=your-api-key-here
Configuration
Enter your details into the config.yaml file:
yamlCopyusername: # Your LinkedIn email
password: # Your LinkedIn password
phone_number: # Your phone number

positions:
- software engineering intern
# Add more positions as needed

locations:
- San Diego, California
- Remote
# Add more locations as needed

salary: "60,000"  # Yearly salary requirement
rate: 25  # Hourly rate requirement

# Required for AI cover letter generation
resume_path: "PATH/TO/YOUR/RESUME.pdf"

uploads:
  Resume: "PATH/TO/YOUR/RESUME.pdf"
  Cover Letter: "PATH/TO/YOUR/COVER_LETTER.pdf"  # Optional, bot will generate custom ones

experience_level:
  - 1  # Entry level
  # - 2  # Associate
  # - 3  # Mid-Senior level
  # - 4  # Director
  # - 5  # Executive
  # - 6  # Internship
Execute
To run the AI-enhanced version:
bashCopypython3 ai_easyapplybot.py
For the original version without AI features:
bashCopypython3 easyapplybot.py
Features

All original features of the LinkedIn Easy Apply Bot
AI-powered cover letter generation
Automatic document handling
Custom answer persistence
Intelligent job filtering

License
This fork's modifications and AI enhancements are licensed under the MIT License.
The original LinkedIn Easy Apply Bot remains under its original license.
Original Work

Original Medium Write-up: https://medium.com/xplor8/how-to-apply-for-1-000-jobs-while-you-are-sleeping-da27edc3b703
Original Video Tutorial: https://www.youtube.com/watch?v=4R4E304fEAs

Acknowledgments
This project builds upon the work of the original LinkedIn Easy Apply Bot creators.
Copy
This README:
1. Clearly indicates this is a fork with new features
2. Credits the original work
3. Explains the new AI capabilities
4. Provides setup instructions for the new features
5. Maintains links to original resources
6. Includes license information
7. Provides clear instructions for both versions
