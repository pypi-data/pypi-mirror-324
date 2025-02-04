# import pandas as pd
# from ..utils.fuzzy_matching import fuzzy_match

# class BangaloreHandler:
#     def __init__(self):
#         # Load Bangalore address data
#         self.df = pd.read_csv('C:/VSCODE PROJECTS/Adrscheck/data/Karnataka/bangaloreaddress.csv')

#     def correct_address(self, input_address):
#         matches = self.fuzzy_validate_address(input_address)
#         if matches:
#             return matches
#         return "No matching addresses found."

#     def fuzzy_validate_address(self, input_address):
#         # Simple fuzzy matching on the address fields
#         for _, row in self.df.iterrows():
#             if fuzzy_match(input_address, row['Street']):
#                 return {
#                     "Street": row['Street'],
#                     "Ward": row['Ward'],
#                     "Block": row['Block'],
#                     "AS PER FIELD": row['AS PER FIELD']
#                 }
#         return None
