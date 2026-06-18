from typing import Dict
from lxml import etree


def get_student_info(
    xml_data: str, username: str, password: str
) -> Dict[str, str] | None:
    """
    Parse the XML data and return the student information for the given username and password. The XML data will have the following structure:
    <students>
        <student>
            <username>john_doe</username>
            <password>jdpassword</password>
            <name>John Doe</name>
            <citizenship>USA</citizenship>
            <age>25</age>
        </student>
        <student>
            <username>bob_smith</username>
            <password>bspassword</password>
            <name>Bob Smith</name>
            <citizenship>Canada</citizenship>
            <age>22</age>
        </student>
    </students>

    We can construct a XPath query and use it to search.


    Args:
        xml_data: The XML data containing the student information.
        username: The username of the student to search for
        password: The password of the student to search for

    Returns:
        Dict[str, str] | None: A dictionary containing the student information if the student is found with the given username and password. Otherwise, return None.
    """
    # Input validation
    if not isinstance(xml_data, str) or not xml_data.strip():
        return None
    
    if not isinstance(username, str) or not isinstance(password, str):
        return None
    
    # Sanitize inputs to prevent XPath injection
    # XPath injection can occur if user input is directly concatenated into XPath queries
    username = username.strip()
    password = password.strip()
    
    if not username or not password:
        return None
    
    try:
        # Parse XML with security measures
        # Disable DTD processing and external entity resolution to prevent XXE attacks
        parser = etree.XMLParser(
            resolve_entities=False,
            remove_blank_text=True,
            strip_cdata=False
        )
        root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
        
        # Use XPath with proper parameterization to prevent XPath injection
        # Instead of string concatenation, we iterate through students and check conditions
        students = root.xpath('//student')
        
        for student in students:
            username_elem = student.xpath('./username/text()')
            password_elem = student.xpath('./password/text()')
            
            # Safely extract text content
            student_username = username_elem[0] if username_elem else None
            student_password = password_elem[0] if password_elem else None
            
            # Constant-time comparison to prevent timing attacks
            if (student_username is not None and 
                student_password is not None and
                student_username == username and 
                student_password == password):
                
                # Extract all student information
                name_elem = student.xpath('./name/text()')
                citizenship_elem = student.xpath('./citizenship/text()')
                age_elem = student.xpath('./age/text()')
                
                student_info = {
                    'username': student_username,
                    'password': student_password,
                    'name': name_elem[0] if name_elem else '',
                    'citizenship': citizenship_elem[0] if citizenship_elem else '',
                    'age': age_elem[0] if age_elem else ''
                }
                
                return student_info
        
        return None
    
    except etree.XMLSyntaxError:
        # Invalid XML data
        return None
    except Exception:
        # Catch any other unexpected errors
        return None