# "Requests" package is used for sending HTTP requests.
import requests
# "json" package is used for working with .json files.
import json
# "os" package is used for reading/writing to files.
import os
# "Beautiful Soup" package is used for parsing HTML documents.
from bs4 import BeautifulSoup
# "pandas" package is used for generating and manipulating data and data structures.
import pandas as pd
# "NumPy" package is used for scientific computing.
import numpy as np
# "Matplotlib" package is used for generating charts and graphs.
from matplotlib import pyplot as plt
# Import the Opinion class from the app/models directory.
from app.models.opinion import Opinion
from app.utils import get_item

class Product():
    # Default values: product_name="" means that if no product_name parameters are passed, the default value for the product_name attribute is "".
    # The "product_id" variable must be passed while creating a Product object, otherwise the object will not be created.
    def __init__(self, product_id, opinions=[], product_name="", opinions_count=0, pros_count=0, cons_count=0, average_score=0):
        self.product_id = product_id
        self.opinions = opinions
        self.product_name = product_name
        self.opinions_count = opinions_count
        self.pros_count = pros_count
        self.cons_count = cons_count
        self.average_score = average_score
    
    def __str__(self) -> str:
        # Return a human-readable string representation of a Product object.
        # The "-> str" part is just for documentation purposes. It specifies that the return value is going to be a string.
        return f"""product_id: {self.product_id}<br>
        product_name: {self.product_name}<br>
        opinions_count: {self.opinions_count}<br>
        pros_count: {self.pros_count}<br>
        cons_count: {self.cons_count}<br>
        average_score: {self.average_score}<br>
        opinions: <br><br>
        """ + "<br><br>".join(str(opinion) for opinion in self.opinions)
        # For every opionion in the opinions attribute, convert the opinion to a string and append it to the end of a "<br><br>".

    def __repr__(self) -> str:
        # Return a string representation of a Product object readable by the Python interpreter.
        # If the __repr__ method is defined and the __str__ method is NOT defined, __str__ will return the same value as __repr__.
        return f"Product(product_id={self.product_id}, product_name={self.product_name}, opinions_count={self.opinions_count}, pros_count={self.pros_count}, cons_count={self.cons_count}, average_score={self.average_score}, opinions: [" + ", ".join(opinion.__repr__() for opinion in self.opinions) + "])" 

    def to_dict(self) -> dict:
        # Return a dictionary representation of a Product object.
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions_count": self.opinions_count,
            "pros_count": self.pros_count,
            "cons_count": self.cons_count,
            "average_score": self.average_score,
            "opinions": [opinion.to_dict() for opinion in self.opinions]
        }
        
    def extract_name(self):
        product_url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        # Send a GET request to the "product_url" website.
        response = requests.get(product_url)
        # Enable parsing the HTML document (using "html.parser" - Python's built-in HTML parser module)
        # found in a response from the GET request.
        page = BeautifulSoup(response.text, "html.parser")
        # Set the current Product object's name as the text found in the "h1.product-top__product-info__name" HTML element.
        self.product_name = get_item(page, "h1.product-top__product-info__name")
        return self

    def extract_opinions(self):
        product_url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"

        while product_url:
            # Send a GET request to the "product_url" website.
            response = requests.get(product_url)
            # Enable parsing the HTML document (using "html.parser" - Python's built-in HTML parser module)
            # found in a response from the GET request.
            page = BeautifulSoup(response.text, "html.parser")
            # From the "page" BeautifulSoup object create a list of sections of an HTML document containing the passed CSS selector.
            # "div.js_product-review" refers to every "div" HTML tag with a class attribute equal to "js_product-review".
            # "opinions" is not the same as "self.opinions". "opinions" is a local variable accessible only in this method,
            # "self.opinions" is the Product class's attribute, accesible anywhere.
            opinions = page.select("div.js_product-review")

            # For every opinion (section) in the "opinions" list
            for opinion in opinions:
                # add a new Opinion object to the current Product object's "opinions" attribute.
                self.opinions.append(Opinion().extract_opinion(opinion))

            # After extracting every opinion from the current page of opinions,
            # check if the current page is the last one available.
            try:
                product_url = "https://www.ceneo.pl" + get_item(page, "a.pagination__next", "href")
            # If there are no pages after the current page, stop extracting opinions.
            except TypeError:
                product_url = None
        return self

    def opinions_to_df(self):
        # Convert a list of dictionaries of opinion's attributes to a JSON formatted string and then convert that string to a pandas object.
        opinions = pd.read_json(json.dumps(self.opinions_to_dict()))
        # Replace every value (e.g "3,5/5", "0/5", "4/5") of "stars" attribute with a converted float value (e.g "3.5", "0.0", "4.0").
        # map() function applies a function to every element of an iterable.
        # "x.split("/")[0].replace(",",".")" splits "x" (here it may be e.g. "3,5/5") into two values using "/" character as a separator,
        # only keeps the first value (e.g. "3,5") and replaced "," characters with "." characters.
        opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",",".")))
        return opinions

    def stats_to_dict(self):
        # Return a dictionary containing statistics of the current object.
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "opinions_count": self.opinions_count,
            "pros_count": self.pros_count,
            "cons_count": self.cons_count,
            "average_score": self.average_score,
        }
    
    def opinions_to_dict(self):
        # Return a list of dictionaries of opinions' attributes.
        return [opinion.to_dict() for opinion in self.opinions]

    def calculate_stats(self):
        # Count the total amount of opinions.
        self.opinions_count = self.opinions_to_df().shape[0]
        # Count the amount of opinions with pros about the product.
        self.pros_count = int(self.opinions_to_df()["pros"].map(bool).sum())
        # Count the amount of opinions with cons about the product.
        self.cons_count = int(self.opinions_to_df()["cons"].map(bool).sum())
        # Calculate the mean of stars given.
        self.average_score = self.opinions_to_df()["stars"].mean().round(2)
        return self

    def draw_charts(self):
        opinions = self.opinions_to_df()

        # If the "app/static/plots" directory does NOT exist,
        if not os.path.exists("app/static/plots"):
            # create it.
            os.makedirs("app/static/plots")

        # Count the amount of each score given, sort them in an ascending order
        # and replace the old index with a new index ("Nie polecam", "Polecam", None).
        # "dropna=False" specifies counting the values even if they are missing (NaN).
        # "fill_value=0" specifies filling missing (NaN) values with 0s.
        recommendation = opinions["recommendation"].value_counts(dropna=False).sort_index().reindex(["Nie polecam", "Polecam", None], fill_value=0)
        # Generate a pie plot.
        recommendation.plot.pie(
            label="",
            # Generate and add percent values as labels of each wedge on the pie plot.
            autopct = lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',
            colors = ["crimson", "forestgreen", "lightskyblue"],
            labels = ["Nie polecam", "Polecam", "Nie mam zdania"]
        )

        plt.title("Rekomendacje")
        plt.savefig(f"app/static/plots/{self.product_id}_recommendations.png")
        plt.close()

        # Count the amount of each score given, sort them in an ascending order
        # and replace the old index (e.g. "0/5", "2/5", "4,5/5") with a new index (e.g. "0.0", "2.0", "4.5").
        # "fill_value=0" specifies filling missing (NaN) values with 0s.
        stars = opinions["stars"].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        # Generate a bar plot.
        stars.plot.bar(
            color = "coral"
        )
        plt.title("Oceny produktu")
        plt.xlabel("Liczba gwiazdek")
        plt.ylabel("Liczba opinii")
        plt.grid(True, axis="y")
        plt.xticks(rotation=0)
        plt.savefig(f"app/static/plots/{self.product_id}_stars.png")
        plt.close()
        return self

    def export_product(self):
        # If the "app/products" directory does NOT exist,
        if not os.path.exists("app/products"):
            # create it.
            os.makedirs("app/products")

        # Open a .json file with writing enabled.
        with open(f"app/products/{self.product_id}.json", "w", encoding="UTF-8") as jf:
            # Save the product's statistics to the .json file.
            # "ensure_ascii=False" enables saving non-ASCII characters (e. g. letters with accents) to the file.
            json.dump(self.stats_to_dict(), jf, indent=4, ensure_ascii=False)

    def export_opinions(self):
        # If the "app/opinions" directory does NOT exist,
        if not os.path.exists("app/opinions"):
            # create it.
            os.makedirs("app/opinions")

        # Open a .json file with writing enabled.
        with open(f"app/opinions/{self.product_id}.json", "w", encoding="UTF-8") as jf:
            # Save the product's opinons to the .json file.
            # "ensure_ascii=False" enables saving non-ASCII characters (e. g. letters with accents) to the file.
            json.dump(self.opinions_to_dict(), jf, indent=4, ensure_ascii=False)
    
    def import_product(self):
        # If a .json file with the passed product_id exists,
        if os.path.exists(f"app/products/{self.product_id}.json"):
            # open it with only reading enabled.
            with open(f"app/products/{self.product_id}.json", "r", encoding="UTF-8") as jf:
                # Convert a JSON object to a Python object.
                product = json.load(jf)

            self.product_id = product["product_id"]
            self.product_name = product["product_name"]
            self.opinions_count = product["opinions_count"]
            self.pros_count = product["pros_count"]
            self.cons_count = product["cons_count"]
            self.average_score = product["average_score"]

            # Open a (different) .json file with only writing enabled.
            with open(f"app/opinions/{self.product_id}.json", "r", encoding="UTF-8") as jf:
                # Convert a JSON object to a Python object.
                opinions = json.load(jf)
                
            # For every opinion found in the converted Python object
            for opinion in opinions:
                # add the opinion to the current object's "opinions" attribute.
                # "**opinion" means that every key-value pair in a the "opinion" variable (which is a dictionary)
                # is passed as separate parameter instead of passing the whole dictionary as a single parameter.
                # "**" (and "*") before a variable name specifies that the iterable will be unpacked.
                self.opinions.append(Opinion(**opinion))
