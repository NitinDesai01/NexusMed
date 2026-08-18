import pytesseract
from PIL import Image
import PyPDF2
import os
import logging

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff']
        
    def process_file(self, file_path):
        """Process file and extract text using OCR"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.pdf':
                return self._process_pdf(file_path)
            elif file_ext in ['.jpg', '.jpeg', '.png', '.tiff']:
                return self._process_image(file_path)
            else:
                return None
        except Exception as e:
            logger.error(f"OCR processing error: {e}")
            return None
    
    def _process_pdf(self, file_path):
        """Extract text from PDF"""
        try:
            text = ''
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
            return text
        except Exception as e:
            logger.error(f"PDF processing error: {e}")
            return None
    
    def _process_image(self, file_path):
        """Extract text from image using Tesseract"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            logger.error(f"Image OCR error: {e}")
            return None
    
    def extract_key_info(self, text):
        """Extract key medical information from text"""
        if not text:
            return None
        
        info = {
            'patient_name': self._extract_field(text, ['Patient:', 'Patient Name:', 'Name:']),
            'date': self._extract_field(text, ['Date:', 'Report Date:', 'Test Date:']),
            'doctor': self._extract_field(text, ['Doctor:', 'Physician:', 'Referring Doctor:']),
            'test_type': self._extract_field(text, ['Test:', 'Report Type:', 'Examination:']),
            'findings': self._extract_section(text, 'Findings'),
            'conclusion': self._extract_section(text, 'Conclusion'),
            'recommendations': self._extract_section(text, 'Recommendations')
        }
        
        return info
    
    def _extract_field(self, text, patterns):
        """Extract a field using multiple patterns"""
        for pattern in patterns:
            lines = text.split('\n')
            for line in lines:
                if pattern in line:
                    return line.split(pattern)[1].strip()
        return None
    
    def _extract_section(self, text, section_name):
        """Extract a section from the text"""
        lines = text.split('\n')
        section_lines = []
        found = False
        
        for i, line in enumerate(lines):
            if section_name.lower() in line.lower():
                found = True
                continue
            if found and line.strip():
                # Check if next section starts
                if any(s in line.lower() for s in ['conclusion', 'recommendations', 'signature']):
                    break
                section_lines.append(line.strip())
        
        return '\n'.join(section_lines) if section_lines else None