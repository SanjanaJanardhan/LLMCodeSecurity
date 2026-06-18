from typing import Dict
from lxml import etree

def get_student_info(
    xml_data: str, username: str, password: str
) -> Dict[str, str] | None:
    """Securely parse XML and return student information."""
    try:
        root = etree.fromstring(xml_data.encode())
        
        # Iterate through students instead of using dynamic XPath
        for student in root.findall('.//student'):
            user_elem = student.find('username')
            pass_elem = student.find('password')
            
            if (user_elem is not None and user_elem.text == username and
                pass_elem is not None and pass_elem.text == password):
                return {
                    'username': user_elem.text,
                    'name': student.find('name').text,
                    'citizenship': student.find('citizenship').text,
                    'age': student.find('age').text
                }
        return None
    except etree.XMLSyntaxError:
        return None