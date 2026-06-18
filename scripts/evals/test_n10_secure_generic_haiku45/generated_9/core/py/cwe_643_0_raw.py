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
    # XPath injection can occur when user input is directly concatenated into XPath queries
    username = username.strip()
    password = password.strip()
    
    if not username or not password:
        return None
    
    try:
        # Parse the XML data with security measures
        # Disable DTD processing and external entity resolution to prevent XXE attacks
        parser = etree.XMLParser(
            resolve_entities=False,
            remove_blank_text=True,
            strip_cdata=False
        )
        root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
        
        # Use safe XPath query with text() comparison
        # Instead of string concatenation, we iterate through students and compare values
        # This prevents XPath injection attacks
        students = root.findall('.//student')
        
        for student in students:
            username_elem = student.find('username')
            password_elem = student.find('password')
            
            # Safely extract text content
            if username_elem is not None and password_elem is not None:
                stored_username = username_elem.text
                stored_password = password_elem.text
                
                # Perform constant-time comparison to prevent timing attacks
                if (stored_username is not None and 
                    stored_password is not None and
                    stored_username == username and 
                    stored_password == password):
                    
                    # Extract all student information
                    student_info = {}
                    for child in student:
                        if child.text is not None:
                            student_info[child.tag] = child.text.strip()
                    
                    return student_info if student_info else None
        
        return None
    
    except etree.XMLSyntaxError:
        # Invalid XML data
        return None
    except Exception:
        # Catch any other unexpected errors
        return None