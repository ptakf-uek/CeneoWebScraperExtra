from app.parameters import selectors
from app.utils import get_item

# Class represention of a single opinion.
class Opinion():
    # Default values: author="" means that if no author parameters are passed, the default value for the author attribute is "".
    def __init__(self, author="", recommendation=None, stars=0, content="", useful=0, useless=0, published=None,
                 purchased=None, pros=[], cons=[], opinion_id=""):
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.published = published
        self.purchased = purchased
        self.pros = pros
        self.cons = cons
        self.opinion_id = opinion_id

    def __str__(self):
        # Return a human-readable string representation of an Opinion object.
        return f"opinion_id: {self.opinion_id}<br>" + "<br>".join(f"{key}: {str(getattr(self, key))}" for key in selectors.keys())

    def __repr__(self):
        # Return a string representation of an Opinion object readable by the Python interpreter.
        # If the __repr__ method is defined and the __str__ method is NOT defined, __str__ will return the same value as __repr__.
        return f"Opinion(opinion_id={self.opinion_id}, " + ", ".join(f"{key}={str(getattr(self, key))}" for key in selectors.keys()) + ")"

    def to_dict(self):
        # Return a dictionary of the current Opinion object's attributes.
        # The "|" operator merges two dictionaries together.
        return {"opinion_id": self.opinion_id} | {key: getattr(self, key) for key in selectors.keys()}

    # The "opinion" parameter isn't an Opinion object, but an HTML tag.
    def extract_opinion(self, opinion):
        # "selectors.items()" creates a (key, value) tuple from a pair of key-value from the selectors dictionary.
        # "for key, value [...]" unpacks the tuple into two separate variables "key" and "value".
        # "key" is a string, "value" is a list.
        for key, value in selectors.items():
            # setattr() function sets the value of the current object's attribute
            # named the same as the "key" value to the value returned by the get_item() function.
            # "*value" means that every element in the "value" variable (which is a list)
            # is passed as a separate parameter instead of passing the whole list as a single parameter.
            # "*" (and "**") before a variable name specifies that the iterable will be unpacked.
            setattr(self, key, get_item(opinion, *value))
        # Set the current object's "opinion_id" attribute to the value of the "data-entry-id" HTML div tag's class attribute.
        self.opinion_id = opinion["data-entry-id"]
        # Return the current object, now with the newly set attributes.
        return self
