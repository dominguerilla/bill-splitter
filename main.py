from bill_reader import BillReader
from dataclasses import dataclass

regex = r'^(?![#\n])([\w\s\+]+)+\s+\(\$(\d+(?:\.\d+)?)\):\s*((?:\w[,\s]*)+|ALL)$'
NJ_TAX_FACTOR = 1.06625

@dataclass
class Charge:
    """Represents a person and their total charge for the bill"""
    name: str
    price: float

    def __repr__(self):
        return f"{self.name}: ${self.price}"

def get_subtotals(bill_items):
    charges = []
    for item in bill_items:
        update_charges(charges,item)
    charges.sort(key=lambda charge: charge.price)
    return charges

def update_charges(charges,item):
    for debtor in item.debtors:
        charge = get_charge(charges, debtor)
        if not charge:
            charge = Charge(debtor, 0)
            charges.append(charge)
        charge.price += item.price / len(item.debtors)

# TODO: Gotta be a better way to do this. Maybe by overriding some 'dunder' function for BillItem?
# Or something with sets?
def get_charge(charges, name):
    for charge in charges:
        if charge.name in name:
            return charge
    return None

with BillReader("example_bill", regex) as bill:
    bill_items = bill.split()
    charges = get_subtotals(bill_items)
    running_total = 0

    # Calculate tax
    for total in charges:
        total.price = total.price * NJ_TAX_FACTOR 
        running_total += total.price 

    tip = running_total * .2
     
    for total in charges:
        total.price += tip / len(charges)
        print(f"{total.name}: ${total.price:.2f}")

    #print(f"Total (with tax): {running_total:.2f}")
    print(f"Total (with tax + 20% tip): {(running_total + tip):.2f}")
