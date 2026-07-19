import io
from pypdf import PdfReader
import docx

class FileParserService:
    @staticmethod
    def extract_text_from_pdf(file_bytes:bytes)->str:
        """
        Extract text from pdf file
        
        
        """
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PdfReader(pdf_file)
        text = []
        for page in pdf_reader.pages:
            text.append(page.extract_text() or "")
        return "\n\n".join(text)
   

    @staticmethod
    def extract_text_from_docx(file_bytes:bytes) -> str:
        """
        Extract text from docx file
        
        
        """
        
        docx_file = io.BytesIO(file_bytes)
        doc = docx.Document(docx_file)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n\n".join(text)

    @classmethod
    def extract_text(cls,filename:str,file_bytes:bytes)->str:
        """
        Determines file type by extension and extracts plain text.
        """

        filename_lower = filename.lower()
        if filename_lower.endswith(".pdf"):
            return cls.extract_text_from_pdf(file_bytes)
        elif filename_lower.endswith(".docx"):
            return cls.extract_text_from_docx(file_bytes)
        elif filename_lower.endswith(".txt"):
            return file_bytes.decode("utf-8", errors="ignore")
        else:
            raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
         
    