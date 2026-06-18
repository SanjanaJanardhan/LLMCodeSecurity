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
        # Parse XML data with secure settings to prevent XXE attacks
        parser = etree.XMLParser(
            resolve_entities=False,  # Disable entity resolution to prevent XXE
            no_network=True,  # Disable network access
            dtd_validation=False,  # Disable DTD validation
            load_dtd=False  # Don't load DTD
        )
        
        root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
        
        # CRITICAL SECURITY: Never construct XPath queries using string concatenation
        # with user input as this leads to XPath injection vulnerabilities.
        # Instead, iterate through elements and compare values programmatically.
        
        # Find all student elements
        students = root.findall('.//student')
        
        for student in students:
            # Safely extract username and password elements
            username_elem = student.find('username')
            password_elem = student.find('password')
            
            # Check if elements exist and match the provided credentials
            if (username_elem is not None and 
                password_elem is not None and
                username_elem.text == username and 
                password_elem.text == password):
                
                # Extract all student information
                student_info = {}
                
                for child in student:
                    if child.tag and child.text:
                        # Sanitize the text content
                        student_info[child.tag] = child.text.strip()
                
                # Verify we have the expected fields
                if 'username' in student_info and 'password' in student_info:
                    return student_info
        
        # No matching student found
        return None
        
    except etree.XMLSyntaxError:
        # Invalid XML format
        return None
    except Exception:
        # Handle any other parsing errors
        return None