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
    if not xml_data or not isinstance(xml_data, str):
        return None
    
    if not username or not isinstance(username, str):
        return None
    
    if not password or not isinstance(password, str):
        return None
    
    try:
        # Parse XML data securely - disable entity resolution to prevent XXE attacks
        parser = etree.XMLParser(
            resolve_entities=False,
            no_network=True,
            dtd_validation=False,
            load_dtd=False
        )
        root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
        
        # Iterate through all student elements to find matching credentials
        # SECURITY: Do NOT use user input directly in XPath queries to prevent XPath injection
        # Instead, iterate through elements and compare values programmatically
        for student in root.findall('.//student'):
            username_elem = student.find('username')
            password_elem = student.find('password')
            
            if username_elem is None or password_elem is None:
                continue
            
            # Compare username and password
            if username_elem.text == username and password_elem.text == password:
                # Extract student information
                student_info = {}
                
                # Define sensitive fields that should NOT be included in the response
                sensitive_fields = {'username', 'password'}
                
                for child in student:
                    # Only include non-sensitive fields in the response
                    if child.text and child.tag not in sensitive_fields:
                        student_info[child.tag] = child.text
                
                # Return the student information if we have valid data
                if student_info:
                    return student_info
        
        # No matching student found
        return None
        
    except etree.XMLSyntaxError:
        # Invalid XML data
        return None
    except Exception:
        # Handle any other parsing errors
        return None