# parse_content.py
# author: Sienko Ikhabi
# date: 2025-01-16

from lxml import html, etree

def parse_content(html_content, selector, selector_type='css'):
    """
    Parses HTML content to extract data based on the provided selector.

    Parameters:
        html_content (str): The raw HTML content.
        selector (str): The CSS selector or XPath expression to target elements.
        selector_type (str): The type of selector ('css' or 'xpath'). Case-insensitive.

    Returns:
        list: A list of extracted data elements.

    Raises:
        ValueError: If the selector_type is unsupported or parsing fails.

    Example:
        # Sample HTML content
        html_content = '<html><body><div class="item">alfa</div><div class="item">bravo</div> <div class="item">charlie</div> </body> </html>'

        # Using CSS selector
        parse_content(html_content, ".item")  
        # Returns: [{'value': 'alfa'}, {'value': 'bravo'}, {'value': 'charlie'}]

        # Using XPath selector
        parse_content(html_content, "//div[@class='item']", selector_type='xpath')  
        # Returns: [{'value': 'alfa'}, {'value': 'bravo'}, {'value': 'charlie'}]
    """

    
    # Ensure the selector_type is valid
    if selector_type.lower() not in ['xpath', 'css']:
        raise ValueError(f"Invalid selector_type '{selector_type}'. Only CSS/XPath selectors are supported.")
    
    try:
        # Parse the HTML content into a document object
        doc = html.fromstring(html_content)

        # Extract data based on the selector type
        if selector_type.lower() == 'css':
            elements = doc.cssselect(selector)  # Use CSS selectors
        elif selector_type.lower() == 'xpath':
            elements = doc.xpath(selector)  # Use XPath selectors

        # Extract text content and strip whitespace
        extracted_data = [{"value": el.text} for el in elements]
        return extracted_data

    except Exception as e:
        raise ValueError("Unable to parse the html_content provided.")

