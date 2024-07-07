from django import template

register = template.Library()

@register.filter
def format_phone(value):
    """
    Format a phone number to the pattern `14 997468-8186`.
    """
    if len(value) == 11:  # Check if the number has 11 digits
        formatted_phone = f"{value[:2]} {value[2:7]}-{value[7:]}"
        return formatted_phone
    return value  # Return the original value if it doesn't have 11 digits
