from dataclasses import dataclass
import re

@dataclass
class BillItem:
    """Represents one item on a bill, along with its debtors"""
    name: str
    price: float
    debtors: list[str]

class BillReader(object):
    """Given an input filename and regex expression, creates a list of BillItems.""" 
    def __init__(self, filename, regex):
        self.filename = filename
        self.regex = regex
        self.bill = None
        self._is_open = False
    
    def is_open(self):
        return self.bill and self._is_open

    def __enter__(self, *args):
        self.bill = open(self.filename)
        self._is_open = True
        return self

    def __exit__(self, *args):
        if self.bill:
            self.bill.close()
            self._is_open = False

    def print_first_line(self):
        if self.is_open():
           print(self.bill.readline())

    def split(self):
        if not self.is_open():
            raise Exception("Bill not open.")

        def tokenize_line_to_item(line):
            groups = re.findall(self.regex, line)
            if not groups:
                return None
            item = groups[0] 
            name = item[0]
            price = float(item[1])
            debtors = [debtor.strip() for debtor in item[2].split(',')]
            return BillItem(name, price, debtors)

        matches = list(map(tokenize_line_to_item, self.bill.readlines())) 
        return filter(None, matches) 
    

