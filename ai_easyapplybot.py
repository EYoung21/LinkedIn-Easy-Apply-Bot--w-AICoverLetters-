from easyapplybot import EasyApplyBot, log
import os
from openai import OpenAI
from fpdf import FPDF
import PyPDF2
from pathlib import Path
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv

class AIEasyApplyBot(EasyApplyBot):
    def __init__(self, *args, **kwargs):
        load_dotenv()
        # Extract AI-specific parameters
        self.resume_path = kwargs.pop('resume_path')
        self.openai_client = OpenAI()  # It will automatically look for OPENAI_API_KEY in environment
        
        # Initialize resume text
        self.resume_text = self._extract_text_from_pdf(self.resume_path)
        
        # Create directory for generated cover letters
        self.cover_letter_dir = "generated_cover_letters"
        if not os.path.exists(self.cover_letter_dir):
            os.makedirs(self.cover_letter_dir)
        
        # Initialize parent class
        super().__init__(*args, **kwargs)

    def _extract_text_from_pdf(self, pdf_path):
        """Extract text content from resume PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            log.error(f"Error extracting text from resume: {str(e)}")
            return ""

    def generate_cover_letter(self, job_title, company_name, job_description):
        """Generate a cover letter using AI based on the job details and resume"""
        try:
            prompt = f"""Based on the following resume and job details, generate a professional cover letter:
            
            Job Title: {job_title}
            Company: {company_name}
            Job Description: {job_description}
            
            Resume: {self.resume_text}
            
            The cover letter should:
            1. Be personalized for the role and company
            2. Highlight relevant experience from the resume
            3. Show enthusiasm for the position
            4. Be professional but engaging
            5. Be 3-4 paragraphs long
            6. Follow standard business letter format
            7. Not exceed one page
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            log.error(f"Error generating cover letter: {str(e)}")
            return None

    def create_pdf_cover_letter(self, content, company_name):
        """Convert the generated cover letter to PDF"""
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_margins(25.4, 25.4, 25.4)  # 1 inch margins
            
            # Add current date
            pdf.cell(0, 10, time.strftime("%B %d, %Y"), ln=True)
            pdf.ln(10)
            
            # Format and add content with proper line spacing
            lines = content.split('\n')
            for line in lines:
                # Check if line is a paragraph break
                if line.strip() == "":
                    pdf.ln(10)
                else:
                    # Add line with proper wrapping
                    pdf.multi_cell(0, 6, line.strip())
                    pdf.ln(2)
            
            # Generate filename
            safe_company_name = "".join(x for x in company_name if x.isalnum() or x in (' ', '_', '-'))
            filename = f"{self.cover_letter_dir}/cover_letter_{safe_company_name}_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
            
            pdf.output(filename)
            return filename
        except Exception as e:
            log.error(f"Error creating PDF cover letter: {str(e)}")
            return None

    def apply_to_job(self, jobID):
        """Override the original apply_to_job method to include cover letter generation"""
        try:
            # Get the job page
            self.get_job_page(jobID)
            time.sleep(1)
            
            # Get easy apply button
            button = self.get_easy_apply_button()
            
            # Check if we should proceed with application
            if not button or any(word in self.browser.title for word in self.blackListTitles):
                return super().apply_to_job(jobID)
            
            # Get job details for cover letter
            job_title = self.browser.title.split(' | ')[0].strip()
            company_name = self.browser.title.split(' | ')[1].strip()
            
            try:
                job_description = self.browser.find_element(By.CLASS_NAME, "jobs-description").text
            except Exception as e:
                log.error(f"Error getting job description: {str(e)}")
                job_description = "Position at " + company_name
            
            # Generate and save cover letter
            cover_letter_content = self.generate_cover_letter(job_title, company_name, job_description)
            if cover_letter_content:
                cover_letter_path = self.create_pdf_cover_letter(cover_letter_content, company_name)
                if cover_letter_path:
                    # Temporarily add the cover letter to uploads
                    original_uploads = self.uploads.copy()
                    self.uploads["Cover Letter"] = cover_letter_path
                    
                    # Proceed with application
                    result = super().apply_to_job(jobID)
                    
                    # Clean up
                    try:
                        os.remove(cover_letter_path)
                    except Exception as e:
                        log.error(f"Error removing temporary cover letter: {str(e)}")
                    
                    self.uploads = original_uploads
                    return result
            
            # If cover letter generation failed, proceed with normal application
            return super().apply_to_job(jobID)
            
        except Exception as e:
            log.error(f"Error in AI-enhanced application: {str(e)}")
            return False

if __name__ == '__main__':
    import yaml
    
    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    assert len(parameters['positions']) > 0
    assert len(parameters['locations']) > 0
    assert parameters['username'] is not None
    assert parameters['password'] is not None
    assert parameters['phone_number'] is not None
    assert parameters.get('resume_path') is not None

    if 'uploads' in parameters.keys() and type(parameters['uploads']) == list:
        raise Exception("uploads read from the config file appear to be in list format" +
                       " while should be dict. Try removing '-' from line containing" +
                       " filename & path")

    log.info({k: parameters[k] for k in parameters.keys() if k not in ['username', 'password']})

    output_filename = [f for f in parameters.get('output_filename', ['output.csv']) if f is not None]
    output_filename = output_filename[0] if len(output_filename) > 0 else 'output.csv'
    blacklist = parameters.get('blacklist', [])
    blackListTitles = parameters.get('blackListTitles', [])

    uploads = {} if parameters.get('uploads', {}) is None else parameters.get('uploads', {})
    for key in uploads.keys():
        assert uploads[key] is not None

    locations = [l for l in parameters['locations'] if l is not None]
    positions = [p for p in parameters['positions'] if p is not None]

    bot = AIEasyApplyBot(
        username=parameters['username'],
        password=parameters['password'],
        phone_number=parameters['phone_number'],
        resume_path=parameters['resume_path'],
        salary=parameters['salary'],
        rate=parameters['rate'],
        uploads=uploads,
        filename=output_filename,
        blacklist=blacklist,
        blackListTitles=blackListTitles,
        experience_level=parameters.get('experience_level', [])
    )
    bot.start_apply(positions, locations)