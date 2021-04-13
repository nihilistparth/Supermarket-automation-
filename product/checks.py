from .models import Product

def quantity_check(id, total_quantity):
    p = Product.objects.get(pk=id)

    if p.quantity>=total_quantity:
        return True
    else:
        return False

# Checks if the product exists in the database...
def product_exist(name):
    p_list = Product.objects.filter(name__exact = name)
    if len(p_list)==0:
        return False
    return True

# Check for the dates as strings
def date_correct(start_date, end_date):
    if len(start_date) != 0 and len(end_date) != 0:
        return 1
    elif len(start_date) != 0 and len(end_date) == 0:
        return 2
    return 0