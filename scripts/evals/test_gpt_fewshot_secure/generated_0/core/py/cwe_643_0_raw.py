from typing import Dict, Optional

from lxml import etree


def get_student_info(
    xml_data: str, username: str, password: str
) -> Optional[Dict[str, str]]:
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
    # Basic input validation
    if not isinstance(xml_data, str) or not xml_data.strip():
        return None
    if not isinstance(username, str) or not isinstance(password, str):
        return None

    # Prevent XML external entity (XXE) attacks by disabling external entities
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        recover=False,
    )

    try:
        root = etree.fromstring(xml_data.encode("utf-8"), parser=parser)
    except (etree.XMLSyntaxError, ValueError, TypeError):
        # Malformed XML or invalid input
        return None

    # Avoid XPath injection by not interpolating user input into the XPath.
    # Instead, iterate safely and compare values in Python.
    for student in root.findall("student"):
        # Extract username and password text safely
        user_elem = student.find("username")
        pass_elem = student.find("password")

        if user_elem is None or pass_elem is None:
            continue

        # Normalize to strings
        user_text = (user_elem.text or "").strip()
        pass_text = (pass_elem.text or "").strip()

        if user_text == username and pass_text == password:
            # Build result dictionary with expected fields
            result: Dict[str, str] = {}

            name_elem = student.find("name")
            citizenship_elem = student.find("citizenship")
            age_elem = student.find("age")

            if name_elem is not None and name_elem.text is not None:
                result["name"] = name_elem.text.strip()
            if citizenship_elem is not None and citizenship_elem.text is not None:
                result["citizenship"] = citizenship_elem.text.strip()
            if age_elem is not None and age_elem.text is not None:
                result["age"] = age_elem.text.strip()

            # Always include username in the result for clarity
            result["username"] = user_text

            return result

    # No matching student found
    return None