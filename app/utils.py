# utils.py is a module storing functions imported and used by other modules, but does nothing on its own.
# The get_item() function uses Beautiful Soup library to parse HTML tags.
def get_item(ancestor, selector, attribute=None, return_list=False):
    try:
        if return_list:
            # Return a list of strings containing every element found in an ancestor (an HTML tag) that matches the passed selector (an HTML class's value).
            # get_text() extracts text from an HTML tag.
            # strip() removes whitespace from the beginning and end of a string.
            return [item.get_text().strip() for item in ancestor.select(selector)]
        if attribute:
            # Return the value of only the first found HTML tag's attribute that matches the passed selector.
            return ancestor.select_one(selector)[attribute]
        # Return the extracted (and stripped) text of only the first found HTML tag that matches the passed selector.
        return ancestor.select_one(selector).get_text().strip()
    # If a wrong attribute value or type value was input, return nothing.
    except (AttributeError, TypeError):
        return None
