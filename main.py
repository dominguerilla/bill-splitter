from bill_reader import BillReader
from dataclasses import dataclass

regex = r'^(?![#\n])([\w\s\+]+)+\s+\(\$(\d+(?:\.\d+)?)\):\s*((?:\w[,\s]*)+|ALL)$'

@dataclass
class Charge:
    """Represents a person and their total charge for the bill"""
    name: str
    price: float

def get_subtotals(bill_items):
    charges = []
    for item in bill_items:
        update_charges(charges,item)
    return charges

def update_charges(charges,item):
    for debtor in item.debtors:
        charge = get_charge(charges, debtor)
        if not charge:
            charge = Charge(debtor, 0)
            charges.append(charge)
        charge.price += item.price / len(item.debtors)

# TODO: Gotta be a better way to do this. Maybe by overriding some 'dunder' function for BillItem?
def get_charge(charges, name):
    for charge in charges:
        if charge.name in name:
            return charge
    return None

with BillReader("example_bill", regex) as bill:
    bill_items = bill.split()
    totals = get_subtotals(bill_items)
    for total in totals:
        print(total)

