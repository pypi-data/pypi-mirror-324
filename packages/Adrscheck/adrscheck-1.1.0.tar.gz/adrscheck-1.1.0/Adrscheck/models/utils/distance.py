
import re
import importlib

from Adrscheck import *
# Set of common words for spell checking
COMMON_WORDS = {
    'mysore', 'bangalore', 'mumbai', 'pune', 'karnataka', 'maharashtra',
    'road', 'cross', 'main', 'block', 'ward', 'stage', 'second', 
    'first', 'third', 'fourth', 'fifth'
}

def levenshtein_distance(s1, s2):
    """Compute the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def damerau_levenshtein_distance(s1, s2):
    """Compute the Damerau-Levenshtein distance."""
    d = {}
    for i in range(-1, len(s1) + 1):
        d[i, -1] = i + 1
    for j in range(-1, len(s2) + 1):
        d[-1, j] = j + 1

    for i in range(len(s1)):
        for j in range(len(s2)):
            cost = 0 if s1[i] == s2[j] else 1
            d[i, j] = min(
                d[i - 1, j] + 1,    # Deletion
                d[i, j - 1] + 1,    # Insertion
                d[i - 1, j - 1] + cost  # Substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[i, j] = min(d[i, j], d[i - 2, j - 2] + cost)  # Transposition

    return d[len(s1) - 1, len(s2) - 1]



def spell_check(word):
    """Suggests a corrected word from COMMON_WORDS based on minimum edit distance."""
    if word in COMMON_WORDS:
        return word

    min_distance = float('inf')
    best_match = None

    for known_word in COMMON_WORDS:
        distance = levenshtein_distance(word, known_word)
        if distance < min_distance:
            min_distance = distance
            best_match = known_word

    return best_match if min_distance <= 2 else word



def extract_city_and_state(user_input):
    city_state_map = {
        'mysore': 'Karnataka',
        'bangalore': 'Karnataka',
        'mumbai': 'Maharashtra',
        'pune': 'Maharashtra',
    }

    # Normalize input
    normalized_input = re.sub(r'[^a-zA-Z0-9\s]', ' ', user_input).lower()
    normalized_input = re.sub(r'\s+', ' ', normalized_input).strip()

    print(f"Normalized Input: {normalized_input}")

    # Correct spelling
    corrected_input = ' '.join(spell_check(word) for word in normalized_input.split())
    print(f"Corrected Input: {corrected_input}")

    detected_city = None
    detected_state = None
    min_distance = float('inf')

    # Check for exact matches from corrected input
    for city, state in city_state_map.items():
        if city in corrected_input:
            print(f"Exact match found for city: {city}")
            detected_city = city
            detected_state = state
            break  # Exit the loop since we found an exact match

    # If no exact match, check distances
    if not detected_city:
        for city, state in city_state_map.items():
            distance = levenshtein_distance(city, corrected_input)
            print(f"Checking city: {city}, distance: {distance}")
            if distance < min_distance:
                min_distance = distance
                detected_city = city
                detected_state = state

    print(f"Detected City: {detected_city}, Detected State: {detected_state}")

    # Return if city and state are detected
    if detected_city and detected_state and min_distance <= 3:
        return detected_city, detected_state

    return detected_city, detected_state

    

import importlib

def load_state_handler(state):
    """Dynamically load the appropriate state handler."""
    state_handlers = {
        'karnataka': 'Adrscheck.models.state_handlers.karnataka_handler.KarnatakaHandler',
        'maharashtra': 'Adrscheck.models.state_handlers.maharashtra_handler.MaharashtraHandler',
    }

    handler_path = state_handlers.get(state.lower())
    if handler_path:
        module_name, class_name = handler_path.rsplit('.', 1)
        module = importlib.import_module(module_name)
        handler_class = getattr(module, class_name)
        print(handler_class)
        return handler_class()  # Initialize and return the handler instance
    return None

def input_handler(user_input):
    # Extract the city and state from the user input
    city, state = extract_city_and_state(user_input)

    if city is not None and state is not None:
        print(f"City: {city}, State: {state}")
        
        # Dynamically load the state handler based on the extracted state
        state_handler = load_state_handler(state)
        
        if state_handler:
            # Use the appropriate state handler to perform fuzzy validation
            matches = state_handler.fuzzy_validate_address(city, user_input)
            # Display the closest matching addresses
            print("Closest matching addresses:",matches)
            return matches
            
        else:
            print(f"No handler found for state: {state}")
    else:
        print("City or state could not be determined from input.")



