from Adrscheck.models.city_handlers.mysore_handler import MysoreHandler
#from Adrscheck.models.city_handlers.bangalore_handler import BangaloreHandler
# Import other city handlers as needed

class KarnatakaHandler:
    def __init__(self):
        self.city_handlers = {
            'mysore': MysoreHandler(),
            #'bangalore': BangaloreHandler(),
            # Add other city handlers here
        }

    def get_city_handler(self, city):
        # Retrieve the appropriate city handler dynamically
        return self.city_handlers.get(city.lower())

    def fuzzy_validate_address(self, city, input_address):
        handler = self.get_city_handler(city)
        if handler:
            return handler.fuzzy_validate_address(input_address)
        else:
            print(f"No handler found for city: {city}")
            return None
