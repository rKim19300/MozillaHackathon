import requests
from bs4 import BeautifulSoup
import re
from PyPDF2 import PdfReader
from io import BytesIO

def parse_webpage(url: str) -> dict[str, str]:
    """
    Parses a terms of service webpage through the url.

    :param url: The url of the terms of service page

    :Returns the dict<section-title, section-content>
    """

    url = "https://www.facebook.com/terms.php"

    # Fetch the page content
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all sections
        sections = {}
        for heading in soup.find_all(['h2', 'h3']): # NOTE some websites may use finer details than h3
            section_title = heading.get_text(strip=True)

            # Find the content under the heading
            content = []
            sibling = heading.find_next_sibling()
            while sibling and sibling.name not in ['h2', 'h3']:
                if sibling.name in ['p', 'div']:
                    content.append(sibling.get_text(strip=True))
                sibling = sibling.find_next_sibling()

            # Store the section title and its content
            sections[section_title] = ' '.join(content)

        return sections
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")


def extract_pdf_sections(pdf_byte_stream) -> dict[str, str]:
    """
    Extracts the section of the pdf, which contains the TOS

    :param pdf_byte_stream: A pdf file represented as a byte stream.
    """
    
    # Initialize a dictionary to store sections
    terms_of_service = {}

    # Read the PDF
    reader = PdfReader(pdf_byte_stream)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # Use a regular expression to identify headings
    heading_pattern = re.compile(r'^\d+\.\s+[A-Za-z ]+', re.MULTILINE)  # Example: "1. Section Title"
    sections = heading_pattern.split(full_text)
    headings = heading_pattern.findall(full_text)

    # Combine headings and content into a dictionary
    for i, heading in enumerate(headings):
        content = sections[i + 1] if i + 1 < len(sections) else ""
        terms_of_service[heading.strip()] = content.strip()

    return terms_of_service



