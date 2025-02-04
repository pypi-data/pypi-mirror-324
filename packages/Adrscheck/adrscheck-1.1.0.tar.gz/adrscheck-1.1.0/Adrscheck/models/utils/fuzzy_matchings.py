
# import pandas as pd
# from .distance import levenshtein_distance, damerau_levenshtein_distance, COMMON_WORDS

# class AddressMatcher:
#     def __init__(self, dataframe, weights=None, max_distance=3):
#         self.addresses = dataframe
#         self.weights = weights or {'AS PER FIELD': 10, 'Street': 0, 'Block': 0, 'Ward': 0}
#         self.max_distance = max_distance
#         self.addresses.columns = self.addresses.columns.str.strip()  # Strip whitespace from column names
#         self.clean_address_data()  # Clean the addresses upon initialization
#         self.word_freq = self.build_word_frequency(self.addresses)  # Build word frequency for spell checking

#     def clean_address_data(self):
#         """Clean DataFrame columns: strip whitespace and convert to lowercase."""
#         for column in self.addresses.columns:
#             if column in ['AS PER FIELD', 'Street', 'Ward', 'Block']:
#                 self.addresses[column] = self.addresses[column].str.strip().str.lower()

#     def build_word_frequency(self, dataframe):
#         """Build word frequency from the addresses in the DataFrame."""
#         word_freq = {}
#         for column in ['AS PER FIELD', 'Street', 'Ward', 'Block']:
#             for entry in dataframe[column].dropna():
#                 words = entry.split()
#                 for word in words:
#                     word_freq[word] = word_freq.get(word, 0) + 1
#         return word_freq

#     def spell_check(self, word):
#         """Suggest a corrected word based on minimum edit distance and keyboard proximity."""
#         if word in COMMON_WORDS:
#             return word

#         min_distance = float('inf')
#         best_match = None

#         # Check keyboard proximity suggestions
#         proximity_suggestions = self.keyboard_proximity_matching(word)
#         for suggestion in proximity_suggestions:
#             distance = damerau_levenshtein_distance(word, suggestion)  # Use Damerau Levenshtein
#             if distance < min_distance:
#                 min_distance = distance
#                 best_match = suggestion

#         # Check against common words
#         for known_word in COMMON_WORDS:
#             distance = damerau_levenshtein_distance(word, known_word)  # Use Damerau Levenshtein
#             if distance < min_distance:
#                 min_distance = distance
#                 best_match = known_word

#         return best_match if min_distance <= 2 else word


#     def keyboard_proximity_matching(self, input_word):
#         """Suggest words based on keyboard proximity."""
#         keyboard_layout = {
#             'q': ['w', 'a', 's'],
#             'w': ['q', 'e', 'a', 's', 'd'],
#             'e': ['w', 'r', 's', 'd'],
#             'r': ['e', 't', 'd', 'f'],
#             't': ['r', 'y', 'f', 'g'],
#             'y': ['t', 'u', 'g', 'h'],
#             'u': ['y', 'i', 'h', 'j'],
#             'i': ['u', 'o', 'j', 'k'],
#             'o': ['i', 'p', 'k'],
#             'p': ['o'],
#             'a': ['q', 's', 'z'],
#             's': ['a', 'd', 'x', 'z'],
#             'd': ['s', 'f', 'r', 'c', 'x'],
#             'f': ['d', 'g', 't', 'v', 'c'],
#             'g': ['f', 'h', 't', 'b', 'v'],
#             'h': ['g', 'j', 'y', 'n', 'b'],
#             'j': ['h', 'k', 'u', 'm', 'n'],
#             'k': ['j', 'l', 'i', 'o', 'm'],
#             'l': ['k', 'p', 'o'],
#             'z': ['a', 's'],
#             'x': ['z', 's', 'd'],
#             'c': ['x', 'd', 'f'],
#             'v': ['c', 'f', 'g'],
#             'b': ['v', 'g', 'h'],
#             'n': ['b', 'h', 'j'],
#             'm': ['n', 'j', 'k'],
#         }

#         suggestions = set()

#         for word in self.word_freq.keys():
#             if word.startswith(input_word):
#                 suggestions.add(word)

#             if input_word in keyboard_layout:
#                 for proximate_key in keyboard_layout[input_word]:
#                     if proximate_key in self.word_freq:
#                         suggestions.add(proximate_key)

#         return list(suggestions)

#     def fuzzy_validate_address(self, input_address):
#         """Validate an input address using fuzzy matching against stored addresses."""
#         if not isinstance(input_address, str) or not input_address.strip():
#             raise ValueError("Input address must be a non-empty string.")
        
#         # Spell-check the entire input address
#         corrected_address = ' '.join(self.spell_check(word) for word in input_address.split())

#         input_parts = [part.strip().lower() for part in corrected_address.split(',')]
#         input_parts = self.remove_city_and_state(input_parts)
#         matched_columns = self.match_columns(input_parts)
#         filtered_rows = self.filter_rows(corrected_address, matched_columns)
#         return filtered_rows

#     def remove_city_and_state(self, input_parts):
#         """Remove the last two parts assuming they are city and state."""
#         return input_parts[:-2] if len(input_parts) > 2 else input_parts

#     def match_columns(self, input_parts):
#         """Match input parts with DataFrame columns and return matched values."""
#         matched_columns = {column: set() for column in self.weights.keys()}

#         # Create a list of tuples (column_name, row_value) for faster access
#         address_data = [
#             {col: str(row[col]).lower() if pd.notna(row[col]) else '' for col in matched_columns.keys()}
#             for _, row in self.addresses.iterrows()
#         ]

#         for part in input_parts:
#             for column in matched_columns.keys():
#                 for row_data in address_data:
#                     column_value = row_data[column]

#                     # Pre-filter by substring presence
#                     if part in column_value:
#                         matched_columns[column].add(column_value)
#                     else:
#                         distance = levenshtein_distance(part, column_value)
#                         if distance <= self.max_distance:
#                             matched_columns[column].add(column_value)

#         # Convert sets back to lists
#         for column in matched_columns.keys():
#             matched_columns[column] = list(matched_columns[column])

#         return matched_columns


#     def filter_rows(self, input_address, matched_columns):
#         """Filter rows based on matches and calculate scores for potential matches."""
#         filtered_rows = []
#         input_address = input_address.strip().lower()

#         for index, row in self.addresses.iterrows():
#             score = 0
#             row_data = {
#                 "AS PER FIELD": str(row.get('AS PER FIELD', '')).lower() if pd.notna(row.get('AS PER FIELD')) else '',
#                 "Street": str(row.get('Street', '')).lower() if pd.notna(row.get('Street')) else '',
#                 "Ward": str(row.get('Ward', '')).lower() if pd.notna(row.get('Ward')) else '',
#                 "Block": str(row.get('Block', '')).lower() if pd.notna(row.get('Block')) else '',
#             }

#             # Calculate score based on matches
#             matched = False  # Flag to check if there's a match in the row
#             for column, matches in matched_columns.items():
#                 for match in matches:
#                     if match in row_data[column]:
#                         score += self.weights[column]  # Use the specified weight for this column
#                         matched = True  # Set the matched flag
#                     else:
#                         distance = levenshtein_distance(match, row_data[column])
#                         if distance <= self.max_distance:
#                             score += (self.max_distance - distance) * self.weights[column]  # Reward closer matches

#             # Create a complete address string only if there is a match
#             if matched and score > 0:
#                 complete_address = ', '.join(filter(None, [row_data['AS PER FIELD'], row_data['Street'], row_data['Ward'], row_data['Block']]))
#                 filtered_rows.append((complete_address, score))

#         # Sort filtered rows by score (higher score first)
#         filtered_rows.sort(key=lambda x: x[1], reverse=True)

#         # Now find the closest match to the input address using Levenshtein distance
#         closest_match = self.find_closest_match(input_address, filtered_rows)

#         if closest_match is None:
#             print(f"No matches found for '{input_address}'.")
#             return None
#         else:
#             print(f"Closest match to '{input_address}': '{closest_match[0]}' with a score of {closest_match[1]}")
#             return closest_match[0]


#     def find_closest_match(self, input_address, filtered_rows):
#         """Find the closest match to the input address from the filtered rows."""
#         closest_match = None
#         closest_distance = float('inf')

#         for address, score in filtered_rows:
#             distance = levenshtein_distance(input_address, address)
#             if distance < closest_distance:
#                 closest_distance = distance
#                 closest_match = (address, score)

#         return closest_match















# Refactored AddressMatcher class without pandas
from .distance import levenshtein_distance, damerau_levenshtein_distance, COMMON_WORDS

class AddressMatcher:
    def __init__(self, addresses, weights=None, max_distance=3):
        self.addresses = addresses
        self.weights = weights or {'AS PER FIELD': 1000, 'Street': 0, 'Block': 0, 'Ward': 0}
        self.max_distance = max_distance
        self.word_freq = self.build_word_frequency()  # Build word frequency for spell checking

    def build_word_frequency(self):
        """Build word frequency from the addresses."""
        word_freq = {}
        for row in self.addresses:
            for column in ['AS PER FIELD', 'Street', 'Ward', 'Block']:
                entry = row.get(column, '')
                words = entry.split()
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
        return word_freq

    def spell_check(self, word):
        """Suggest a corrected word based on minimum edit distance and keyboard proximity."""
        if word in COMMON_WORDS:
            return word

        min_distance = float('inf')
        best_match = None

        # Check keyboard proximity suggestions
        proximity_suggestions = self.keyboard_proximity_matching(word)
        for suggestion in proximity_suggestions:
            distance = damerau_levenshtein_distance(word, suggestion)  # Use Damerau Levenshtein
            if distance < min_distance:
                min_distance = distance
                best_match = suggestion

        # Check against common words
        for known_word in COMMON_WORDS:
            distance = damerau_levenshtein_distance(word, known_word)  # Use Damerau Levenshtein
            if distance < min_distance:
                min_distance = distance
                best_match = known_word

        return best_match if min_distance <= 2 else word

    def keyboard_proximity_matching(self, input_word):
        """Suggest words based on keyboard proximity."""
        keyboard_layout = {
            'q': ['w', 'a', 's'], 'w': ['q', 'e', 'a', 's', 'd'], 'e': ['w', 'r', 's', 'd'], 'r': ['e', 't', 'd', 'f'],
            't': ['r', 'y', 'f', 'g'], 'y': ['t', 'u', 'g', 'h'], 'u': ['y', 'i', 'h', 'j'], 'i': ['u', 'o', 'j', 'k'],
            'o': ['i', 'p', 'k'], 'p': ['o'], 'a': ['q', 's', 'z'], 's': ['a', 'd', 'x', 'z'], 'd': ['s', 'f', 'r', 'c', 'x'],
            'f': ['d', 'g', 't', 'v', 'c'], 'g': ['f', 'h', 't', 'b', 'v'], 'h': ['g', 'j', 'y', 'n', 'b'], 'j': ['h', 'k', 'u', 'm', 'n'],
            'k': ['j', 'l', 'i', 'o', 'm'], 'l': ['k', 'p', 'o'], 'z': ['a', 's'], 'x': ['z', 's', 'd'], 'c': ['x', 'd', 'f'],
            'v': ['c', 'f', 'g'], 'b': ['v', 'g', 'h'], 'n': ['b', 'h', 'j'], 'm': ['n', 'j', 'k']
        }

        suggestions = set()
        for word in self.word_freq.keys():
            if word.startswith(input_word):
                suggestions.add(word)

            if input_word in keyboard_layout:
                for proximate_key in keyboard_layout[input_word]:
                    if proximate_key in self.word_freq:
                        suggestions.add(proximate_key)

        return list(suggestions)

    def fuzzy_validate_address(self, input_address):
        """Validate an input address using fuzzy matching against stored addresses."""
        if not isinstance(input_address, str) or not input_address.strip():
            raise ValueError("Input address must be a non-empty string.")

        # Spell-check the entire input address
        corrected_address = ' '.join(self.spell_check(word) for word in input_address.split())

        input_parts = [part.strip().lower() for part in corrected_address.split(',')]
        input_parts = self.remove_city_and_state(input_parts)
        matched_columns = self.match_columns(input_parts)

        filtered_rows = self.filter_rows(corrected_address, matched_columns)

        return filtered_rows

    def remove_city_and_state(self, input_parts):
        """Remove the last two parts assuming they are city and state."""
        return input_parts[:-2] if len(input_parts) > 2 else input_parts

    def match_columns(self, input_parts):
        """Match input parts with the addresses and return matched values."""
        matched_columns = {column: set() for column in self.weights.keys()}

        for part in input_parts:
            for row in self.addresses:
                for column, value in row.items():
                    if part in value:
                        matched_columns[column].add(value)
                    else:
                        distance = levenshtein_distance(part, value)
                        if distance <= self.max_distance:
                            matched_columns[column].add(value)

        for column in matched_columns.keys():
            matched_columns[column] = list(matched_columns[column])

        return matched_columns

    def filter_rows(self, input_address, matched_columns):
        """Filter rows based on matches and calculate scores for potential matches."""
        filtered_rows = []
        input_address = input_address.strip().lower()

        for row in self.addresses:
            score = 0
            matched = False
            for column, matches in matched_columns.items():
                for match in matches:
                    if match in row[column]:
                        score += self.weights[column]
                        matched = True
                    else:
                        distance = levenshtein_distance(match, row[column])
                        if distance <= self.max_distance:
                            score += (self.max_distance - distance) * self.weights[column]

                if matched and score > 0:
                    complete_address = ', '.join(filter(None, [row['AS PER FIELD'], row['Street'], row['Ward'], row['Block']]))
                    print(complete_address)
                    filtered_rows.append((complete_address, score))

        filtered_rows.sort(key=lambda x: x[1], reverse=True)
        closest_match = self.find_closest_match(input_address, filtered_rows)

        if closest_match is None:
            print(f"No matches found for '{input_address}'.")
            return None
        else:
            print(f"Closest match to '{input_address}': '{closest_match[0]}' with a score of {closest_match[1]}")
            return closest_match[0]

    def find_closest_match(self, input_address, filtered_rows):
        """Find the closest match to the input address from the filtered rows."""
        closest_match = None
        closest_distance = float('inf')

        for address, score in filtered_rows:
            distance = levenshtein_distance(input_address, address)
            if distance < closest_distance:
                closest_distance = distance
                closest_match = (address, score)

        return closest_match