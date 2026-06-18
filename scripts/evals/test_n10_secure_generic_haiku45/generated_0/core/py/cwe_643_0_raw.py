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
    # Use XPath string literals to safely handle special characters
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
            remove_comments=True
        )
        root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)
        
        # Use XPath with proper string literal handling to prevent XPath injection
        # Instead of string concatenation, use XPath predicates with text() comparison
        students = root.xpath(
            "//student[username/text()=$username and password/text()=$password]",
            username=username,
            password=password
        )
        
        if not students:
            return None
        
        # Get the first matching student
        student = students[0]
        
        # Extract student information safely
        student_info = {}
        
        # Define allowed fields to extract
        allowed_fields = ['username', 'password', 'name', 'citizenship', 'age']
        
        for field in allowed_fields:
            elements = student.xpath(f"{field}/text()")
            if elements:
                # Get the first text content and ensure it's a string
                value = elements[0]
                if isinstance(value, str):
                    student_info[field] = value.strip()
        
        # Verify we found the expected fields
        if 'username' in student_info and 'password' in student_info:
            return student_info if student_info else None
        
        return None
        
    except etree.XMLSyntaxError:
        # Invalid XML format
        return None
    except etree.XPathError:
        # XPath evaluation error
        return None
    except Exception:
        # Catch any other unexpected errors
        return None