import pandas as pd
from datetime import date
from recommendation import Recommend

# paths ########################################
purchases_path = "data/purchases.csv"
whiskey_path = "data/whiskey86.csv"
review_path = "data/whiskey_review2020.csv"
customers_path = "data/customers.csv"
shops_path = "data/shops.csv"
availability_path = "data/availability.csv"
################################################


class Employee:
    """Defines the functionalities and access level of an employee"""
    @staticmethod
    def register_purchase(customer_id, whiskey, recommended):
        """Registers what customers bought, including the date, name and distillery of the whiskey and if it was
        recommended or not."""
        purchases_data = pd.read_csv(purchases_path)
        customers_data = pd.read_csv(customers_path)
        review_data = pd.read_csv(review_path)
        if customer_id in customers_data["customer_id"].tolist():
            distillery = review_data.loc[review_data['name'] == whiskey, 'distillery'].tolist()
            distillery = distillery[0]
            purchases_data = purchases_data.append({"customer_id": customer_id, "date": date.today(),
                                                    "distillery": distillery, "whiskey": whiskey,
                                                    "recommended": recommended}, ignore_index=True)
            purchases_data.to_csv(purchases_path, index=False)
            customers_data.loc[customers_data["customer_id"] == customer_id, "num_of_purchases"] += 1
            customers_data.to_csv(customers_path, index=False)
            Employee.update_status()
            return {"data": purchases_data.loc[purchases_data["customer_id"] == customer_id].to_dict()}, 200
        else:
            return {"ERROR": f"Customer with ID {customer_id} is not existing in the system. Please ask the manager "
                             f"to register this customer."}, 400

    @staticmethod
    def get_customer(customer_id):
        """Returns customer information"""
        customers_data = pd.read_csv(customers_path)
        if customer_id in customers_data["customer_id"].tolist():
            customer_info = customers_data.loc[customers_data["customer_id"] == customer_id].values.tolist()[0]
            discounts = {"basic": "0%", "silver": "5%", "gold": "10%", "platinum": "15%"}
            return {"customer_id": customer_info[0],
                    "num_of_purchases": customer_info[1],
                    "favourite distillery": customer_info[3], "status": customer_info[2],
                    "discount": discounts[customer_info[2]]}, 200
        else:
            return {"ERROR": f"Customer with ID {customer_id} is not existing in the system."}, 400

    @staticmethod
    def get_favourite(customer_id):
        """Returns favourite distillery of customer"""
        customers_data = pd.read_csv(customers_path)
        if customer_id in customers_data["customer_id"].tolist():
            favourite = customers_data.loc[customers_data["customer_id"] == customer_id, "favourite"]
            if favourite.isna().bool():
                return None
            else:
                return list(favourite)
        else:
            return {"ERROR": f"Customer with ID {customer_id} is not existing in the system."}, 400

    @staticmethod
    def put_favourite(customer_id, favourite):
        """Add/change favourite distillery of customer"""
        customers_data = pd.read_csv(customers_path)
        if customer_id in customers_data["customer_id"].tolist():
            customers_data.loc[customers_data["customer_id"] == customer_id, "favourite"] = favourite
            customers_data.to_csv(customers_path, index=False)
            return {"data": customers_data.loc[customers_data["customer_id"] == customer_id].to_dict()}, 200
        else:
            return {"ERROR": f"Customer with ID {customer_id} is not existing in the system."}, 400

    @staticmethod
    def delete_favourite(customer_id):
        """Delete favourite distillery of customer"""
        customers_data = pd.read_csv(customers_path)
        if customer_id in customers_data["customer_id"].tolist():
            customers_data.loc[customers_data["customer_id"] == customer_id, "favourite"] = ""
            customers_data.to_csv(customers_path, index=False)
            return {"data": customers_data.loc[customers_data["customer_id"] == customer_id].to_dict()}, 200
        else:
            return {"ERROR": f"Customer with ID {customer_id} is not existing in the system."}, 400

    @staticmethod
    def get_purchases(customer_id):
        """Returns up to five last purchases as a list."""
        purchases_data = pd.read_csv(purchases_path)
        purchases_data = purchases_data.loc[purchases_data["customer_id"] == customer_id]
        purchases_data = purchases_data["distillery"].tolist()
        if len(purchases_data) == 0:
            return None
        elif len(purchases_data) >= 5:
            return purchases_data[-5:]
        else:
            return purchases_data

    @staticmethod
    def recommend(shop_id, customer_id=None, distilleries=None):
        """Always recommends five distinct whiskey distilleries based on customer preferences. Recommendations only
        include distilleries available in the shops but can be based on unavailable distilleries. One preferred
        distillery can be indicated if none exist in the database. Four distilleries can be added by choice (liked
        and or already bought by customer). In the case that the user has no preferences, up to three unique
        suggestions ranked by the average value of reviews from all the products for a given distillery are returned."""
        if distilleries is None and customer_id is None:
            recommended_whiskey = Recommend.recommend_review(shop_id)
        elif distilleries is not None and customer_id is None:
            x = Recommend.get_characteristics(distillery=Recommend.get_availability(shop_id))
            y = Recommend.get_characteristics(distillery=distilleries)
            recommended_whiskey = Recommend.knn_recommend(y, x)
        elif distilleries is not None and Employee.get_favourite(customer_id) is not None:
            x = Recommend.get_characteristics(distillery=Recommend.get_availability(shop_id))
            y = Recommend.get_characteristics(distillery=(Employee.get_favourite(customer_id) + distilleries))
            recommended_whiskey = Recommend.knn_recommend(y, x)
        elif distilleries is not None and Employee.get_favourite(customer_id) is None:
            x = Recommend.get_characteristics(distillery=Recommend.get_availability(shop_id))
            y = Recommend.get_characteristics(distillery=distilleries)
            recommended_whiskey = Recommend.knn_recommend(y, x)
        elif distilleries is None and Employee.get_favourite(customer_id) is None:
            recommended_whiskey = Recommend.recommend_review(shop_id)
        else:
            x = Recommend.get_characteristics(distillery=Recommend.get_availability(shop_id))
            y = Recommend.get_characteristics(distillery=Employee.get_favourite(customer_id))
            recommended_whiskey = Recommend.knn_recommend(y, x)
        return {"recommendations": recommended_whiskey}, 200

    @staticmethod
    def get_review(whiskey=""):
        """Returns what other people reviewed about a particular whiskey"""
        reviews_data = pd.read_csv(review_path)
        search = reviews_data.loc[reviews_data["name"] == whiskey, "description"]
        try:
            return pd.DataFrame(search.iloc[0].split(".")).to_dict(), 200
        except IndexError:
            return {"ERROR": "The whiskey is not existing in our database"}, 400

    @staticmethod
    def get_popup(customer_id):
        """Returns where/when there will be a new Pop-up, if the customer's status is gold or higher"""
        customers_data = pd.read_csv(customers_path)
        status = customers_data.loc[customers_data['customer_id'] == customer_id, 'status'].to_string(index=False)
        if status in ['gold', 'platinum']:
            shops_data = pd.read_csv(shops_path)
            return shops_data.loc[shops_data['type'] == 'Pop-up', ['shop_id', 'location', 'date', 'discount']].to_dict(
                orient='index'), 200
        return {'ERROR': 'The customer is not of rank Gold/Platinum or is not registered.'}, 400

    @staticmethod
    def update_status():
        """Updates the status of each customer based on number of purchases in one year"""
        customers_data = pd.read_csv(customers_path)
        purchases_data = pd.read_csv(purchases_path)

        for customer_id in customers_data["customer_id"].tolist():
            purchases_in_year = 0
            purchases_in_year = [purchases_in_year + 1 for i in range(len(purchases_data)) if
                                 purchases_data.iloc[i, 0] == customer_id and (
                                         date.today() - date.fromisoformat(purchases_data.iloc[i, 1])).days <= 365]
            purchases_in_year = sum(purchases_in_year)

            if purchases_in_year >= 50:
                customers_data.loc[customers_data["customer_id"] == customer_id, "status"] = "platinum"
            elif purchases_in_year >= 25:
                customers_data.loc[customers_data["customer_id"] == customer_id, "status"] = "gold"
            elif purchases_in_year >= 10:
                customers_data.loc[customers_data["customer_id"] == customer_id, "status"] = "silver"
            else:
                customers_data.loc[customers_data["customer_id"] == customer_id, "status"] = "basic"

            customers_data.to_csv(customers_path, index=False)

