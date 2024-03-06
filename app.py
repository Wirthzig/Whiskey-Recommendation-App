from flask import Flask, render_template
from flask_restful import reqparse
from employee import Employee
from manager import Manager
import pandas as pd

# paths ########################################
purchases_path = "data/purchases.csv"
whiskey_path = "data/whiskey86.csv"
review_path = "data/whiskey_review2020.csv"
customers_path = "data/customers.csv"
shops_path = "data/shops.csv"
availability_path = "data/availability.csv"
################################################

# Read in data-sets to pass the to the html templates
whiskey_data = pd.read_csv(whiskey_path)
distillery_list = whiskey_data["Distillery"].tolist()
review_data = pd.read_csv(review_path)
whiskey_list = review_data["name"].tolist()


app = Flask(__name__)


@app.route("/")
def start_home():
    """Loads the homepage"""
    return render_template("home.html"), 200


@app.route("/employee")
def start_employee():
    """Loads the employee interface"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id")
    args = parser.parse_args()
    if args["customer_id"] == "":
        args["customer_id"] = None
    if args["customer_id"] is not None:
        purchases_list = Employee.get_purchases(int(args["customer_id"]))
    else:
        purchases_list = None
    return render_template("employee.html", distilleries=distillery_list, whiskeys=whiskey_list,
                           customer_id=args["customer_id"], purchases_list=purchases_list), 200


@app.route("/manager")
def start_manager():
    """Loads the manager interface"""
    return render_template("manager.html", distilleries=distillery_list, whiskeys=whiskey_list), 200


@app.route("/employee/register_purchase")
def api_register_purchase():
    """Parsing information from URL and passing it to Employee.register_purchase()"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type=int)
    parser.add_argument("whiskey", type=str)
    parser.add_argument("recommended", type=str)
    args = parser.parse_args()
    return Employee.register_purchase(args["customer_id"],
                                      args["whiskey"],
                                      args["recommended"])


@app.route("/employee/get_customer")
def api_get_customer():
    """Parsing information from URL and passing it to Employee.get_customer()"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type=int)
    args = parser.parse_args()
    return Employee.get_customer(args["customer_id"])


@app.route("/employee/put_favourite")
def api_put_favourite():
    """Parsing information from URL and passing it to Employee.put_favourite()"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type=int)
    parser.add_argument("favourite", type=str)
    args = parser.parse_args()
    return Employee.put_favourite(args["customer_id"], args["favourite"])


@app.route("/employee/delete_favourite")
def api_delete_favourite():
    """Parsing information from URL and passing it to Employee.delete_favourite()"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type=int)
    args = parser.parse_args()
    return Employee.delete_favourite(args["customer_id"])


@app.route("/employee/recommend")
def api_recommend_whiskey():
    """Parsing information from URL and passing it to Employee.recommend()"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type=str)
    parser.add_argument("shop_id", type=int)
    parser.add_argument("distilleries", type=str, action="append", default=None)
    args = parser.parse_args()
    distilleries = [i for i in args["distilleries"] if i != ""]
    if len(distilleries) == 0:
        distilleries = None
    customer_id = args["customer_id"]
    if customer_id == "":
        customer_id = None
    else:
        customer_id = int(customer_id)
    try:
        return Employee.recommend(args["shop_id"], customer_id, distilleries)
    except ValueError:
        return {"message": "Duplicate or invalid list entry. Check entries and favourite distillery. "
                           "Also check ShopID, as recommendations are not possible for Pop-Up Shops."}, 400


@app.route("/employee/get_review")
def api_get_review():
    """Parsing information from URL and passing it to Employee.get_review()"""
    parser = reqparse.RequestParser()
    parser.add_argument("whiskey", type=str)
    args = parser.parse_args()
    return Employee.get_review(args["whiskey"])


@app.route("/employee/get_popup")
def api_get_popup():
    """Parsing information from URL and passing it to Employee.get_popup()"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type=int)
    args = parser.parse_args()
    return Employee.get_popup(args["customer_id"])


@app.route("/manager/register_customer")
def api_register_customer():
    """Parsing information from URL and passing it to Manager.register_customer()"""
    parser = reqparse.RequestParser()
    parser.add_argument("favourite", type=str)
    args = parser.parse_args()
    return Manager.register_customer(args["favourite"])


@app.route("/manager/delete_customer")
def api_delete_customer():
    """Parsing information from URL and passing it to Manager.delete_customer()"""
    parser = reqparse.RequestParser()
    parser.add_argument("customer_id", type=int)
    args = parser.parse_args()
    return Manager.delete_customer(args["customer_id"])


@app.route("/manager/add_shop")
def api_add_shop():
    """Parsing information from URL and passing it to Manager.add_shop()"""
    parser = reqparse.RequestParser()
    parser.add_argument("location", type=str)
    parser.add_argument("distilleries", type=str, action="append")
    args = parser.parse_args()
    return Manager.add_shop(args["location"], args["distilleries"])


@app.route("/manager/add_popup")
def api_add_popup():
    """Parsing information from URL and passing it to Manager.add_popup()"""
    parser = reqparse.RequestParser()
    parser.add_argument("location", type=str)
    parser.add_argument("date", type=str)
    parser.add_argument("discount", type=str)
    parser.add_argument("distilleries", type=str, action="append")
    args = parser.parse_args()
    return Manager.add_popup(args["location"], args["date"], args["discount"], args["distilleries"])


@app.route("/manager/delete_shop")
def api_delete_shop():
    """Parsing information from URL and passing it to Manager.delete_shop()"""
    parser = reqparse.RequestParser()
    parser.add_argument("shop_id", type=int)
    args = parser.parse_args()
    return Manager.delete_shop(args["shop_id"])


@app.route("/manager/add_distillery")
def api_add_distillery():
    """Parsing information from URL and passing it to Manager.add_distillery()"""
    parser = reqparse.RequestParser()
    parser.add_argument("distillery", type=str)
    parser.add_argument("taste_list", type=int, action="append")
    parser.add_argument("postcode")
    parser.add_argument("latitude")
    parser.add_argument("longitude")
    args = parser.parse_args()
    return Manager.add_distillery(args["distillery"], args["taste_list"], args["postcode"], args["latitude"],
                                  args["longitude"])


@app.route("/manager/add_review")
def api_add_review():
    """Parsing information from URL and passing it to Manager.add_review()"""
    parser = reqparse.RequestParser()
    parser.add_argument("distillery", type=str)
    parser.add_argument("name", type=str)
    parser.add_argument("category", type=str)
    parser.add_argument("points", type=int)
    parser.add_argument("price", type=int)
    parser.add_argument("currency", type=str, default="$")
    parser.add_argument("description", type=str)
    args = parser.parse_args()
    return Manager.add_review(args["distillery"], args["name"], args["category"], args["points"], args["price"],
                              args["currency"], args["description"])


if __name__ == "__main__":
    app.run(debug=True)
