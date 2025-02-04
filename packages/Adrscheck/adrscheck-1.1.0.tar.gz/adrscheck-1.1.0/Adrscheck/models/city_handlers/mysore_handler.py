# import pandas as pd
# from Adrscheck.models.utils.fuzzy_matchings import AddressMatcher

# class MysoreHandler:
#     def __init__(self):
#         self.addresses = self.load_addresses()
#         self.matcher = AddressMatcher(self.addresses)  # Initialize the matcher with the addresses
       


#     def load_addresses(self):
#         # Load addresses from the CSV file for Mysore
#         return pd.read_csv(r'c:\VSCODE PROJECTS\Adrscheck\data\Karnataka\mysoreaddress.csv')

#     def fuzzy_validate_address(self, input_address):
#         # Use the matcher to validate the address
#         return self.matcher.fuzzy_validate_address(input_address)
        






# # THE BELOW CODE DOES NOT USES ANY BUILT IN CSV READER OF EXTERNAL CSV DEPENDENCIES
import csv
from Adrscheck.models.utils.fuzzy_matchings import AddressMatcher

class MysoreHandler:
    def __init__(self):
        self.addresses = self.load_addresses()
        self.matcher = AddressMatcher(self.addresses)  # Initialize the matcher with the addresses

    def load_addresses(self):
        """Load addresses from the CSV file for Mysore without using pandas."""
        addresses = []
        with open(r'c:\VSCODE PROJECTS\Adrscheck\data\Karnataka\mysoreaddress.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Strip whitespace and convert to lowercase for specified columns
                addresses.append({
                    "AS PER FIELD": row.get("AS PER FIELD", "").strip().lower(),
                    "Street": row.get("Street", "").strip().lower(),
                    "Ward": row.get("Ward", "").strip().lower(),
                    "Block": row.get("Block", "").strip().lower()
                })
        return addresses

    def fuzzy_validate_address(self, input_address):
        # Use the matcher to validate the address
        return self.matcher.fuzzy_validate_address(input_address)