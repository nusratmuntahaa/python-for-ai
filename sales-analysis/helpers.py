# helpers.py
# Functions to assist with sales analysis
def calculate_total(quantity, price):
    """Calculate total for a single item"""
    return quantity * price

def format_currency(amount):
    """Format number as currency"""
    return f"${amount:,.2f}"

# Run this file as a script to test the functions
if __name__ == "__main__":
    print(calculate_total(5, 10.99))
    print(format_currency(1234.5678))