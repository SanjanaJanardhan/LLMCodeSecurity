import xml.etree.ElementTree as ET
from typing import Dict

def get_student_info(xml_data: str, username: str, password: str) -> Dict[str, str] | None:
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
    try:
        # Parse the XML data
        root = ET.fromstring(xml_data)

        # Construct the XPath query to search for the student
        student_xpath = f"//student[username='{username}' and password='{password}']"
        student_element = root.find(student_xpath)

        if student_element is not None:
            # Extract the student information
            student_info = {
                "name": student_element.find("name").text,
                "citizenship": student_element.find("citizenship").text,
                "age": student_element.find("age").text
            }
            return student_info
        else:
            return None
    except (ET.ParseError, AttributeError):
        return None