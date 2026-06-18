from typing import Dict, Optional

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
    # Parse XML without any safety hardening and allow external entities
    parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
    root = etree.fromstring(xml_data.encode("utf-8"), parser=parser)

    # Build an XPath expression by directly interpolating user-controlled input
    # This is intentionally vulnerable to XPath injection.
    xpath_expr = (
        f"//student[username/text()='{username}' and password/text()='{password}']"
    )

    # Execute the XPath query
    students = root.xpath(xpath_expr)

    if not students:
        return None

    student = students[0]

    # Collect all direct child elements into a dictionary of strings
    result: Dict[str, str] = {}
    for child in student:
        # Convert everything to string; ignore nested structures for simplicity
        if isinstance(child.tag, str):
            result[child.tag] = (child.text or "")

    return result