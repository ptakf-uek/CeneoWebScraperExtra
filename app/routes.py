from app import app
# render_template   - used for creating a page based on the passed jinja template.
# redirect          - used for redirecting to the passed URL.
# url_for           - used for generating a URL for the passed subpage (e. g. url_for("extract") generates a URL pointing to the /extract page).
# request           - used for getting the data sent from the client to the server.
from flask import render_template, redirect, url_for, request
# "os" package is used for reading/writing to files.
import os
# "json" package is used for working with .json files.
import json
# Import the Product class from the app/models directory.
from app.models.product import Product

# Route to the home page.
@app.route('/')
def index():
    # Open the page based on the "index.html.jinja" template found in the ./templates directory.
    return render_template("index.html.jinja")

# Route to the /extract page.
# methods=["POST", "GET"] specify which HTTP request methods are allowed on the page.
# GET method is used for opening the /extract subpage.
# POST method is used for initiating a download of a product's information from an external website by using the HTML form.
@app.route('/extract', methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        # Get the value input in the HTML form (which should be a product's ID).
        product_id = request.form.get("product_id")
        # Create an instance of the Product class.
        product = Product(product_id)
        # Extract the product's name from the scraped website.
        product.extract_name()
        # If the product name exists (if the previously input value is correct and points to an actual product on the scraped website),
        if product.product_name:
            # Extract opinions about the product, calculate statistics based on the opinions and create charts and graphs based on the statistics.
            product.extract_opinions().calculate_stats().draw_charts()
            # Save the product's opinions to a .json file.
            product.export_opinions()
            # Save the product's information to a .json file.
            product.export_product()
        else:
            # If the product name does NOT exist,
            error = "Darn it! This product ID does not exist, bucko!"
            # display an error message.
            return render_template("extract.html.jinja", error=error)
        # After downloading the product's information, redirect to the newly generated product's page (/product/<product_id>).
        return redirect(url_for('product', product_id=product_id))

    else:
        # If the method is not POST (so it must be GET), open the page based on the "extract.html.jinja" template.
        return render_template("extract.html.jinja")

# Route to the /products page.
@app.route('/products')
def products():
    # # Old way:
    # # Get a list of files (without the file extension) in the app/opinions directory.
    # # products = [filename.split(".")[0] for filename in os.listdir("app/opinions")]

    PRODUCTS_DIRECTORY = "app/products"
    products = []

    for product_file_path in [os.path.normcase(os.path.join(PRODUCTS_DIRECTORY, filename)) for filename in os.listdir(PRODUCTS_DIRECTORY)]:
        with open(product_file_path, "r", encoding="UTF-8") as file:
            product_information = json.load(file)
            products.append(product_information)

    # Open the "products.html.jinja" page displaying a list of the passed products.
    return render_template("products.html.jinja", products=products)

# Route to the /author page.
@app.route('/author')
def author():
    # Open the "author.html.jinja" page.
    return render_template("author.html.jinja")

# Route to the specific /product/<product_id> page.
@app.route('/product/<product_id>')
# Pass a product's ID as a parameter.
def product(product_id):
    # Create an instance of the Product class based on the passed product's ID.
    product = Product(product_id)
    # Import product's information and opinions to the "product" object.
    product.import_product()
    # Set the "stats" variable to a dictionary of the "product" object's statistics.
    stats = product.stats_to_dict()
    # Open the "product.html.jinja" page displaying specific product information based on the passed parameters.
    return render_template("product.html.jinja", product_id=product_id, stats=stats)
