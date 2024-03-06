import pandas as pd
from employee import Employee

# paths ########################################
purchases_path = "data/purchases.csv"
whiskey_path = "data/whiskey86.csv"
review_path = "data/whiskey_review2020.csv"
customers_path = "data/customers.csv"
shops_path = "data/shops.csv"
availability_path = "data/availability.csv"
################################################


class Manager(Employee):
    """Defines the functionalities and access level of a manager"""

    @staticmethod
    def register_customer(favourite=""):
        """Registers new customer"""
        customers_data = pd.read_csv(customers_path)
        try:
            next_id = max(customers_data["customer_id"]) + 1
        except ValueError:
            next_id = 1
        customers_data = customers_data.append(
            {"customer_id": next_id, "num_of_purchases": 0,
             "status": "basic", "favourite": favourite}, ignore_index=True, )
        customers_data.to_csv(customers_path, index=False)
        return {"data": customers_data.loc[customers_data["customer_id"] == next_id].to_dict()}, 200

    @staticmethod
    def delete_customer(customer_id):
        """Deletes customer"""
        customers_data = pd.read_csv(customers_path)
        if customer_id in customers_data["customer_id"].tolist():
            customers_data = customers_data[customers_data["customer_id"] != customer_id]
            customers_data.to_csv(customers_path, index=False)
            return {"data": customers_data.loc[customers_data["customer_id"] == customer_id].to_dict()}, 200
        else:
            return {"ERROR": f"Customer with ID {customer_id} is not existing in the system."}, 400

    @staticmethod
    def add_shop(location, distillery_list=None):
        """Adds standard shop with location and its product availability"""
        shops_data = pd.read_csv(shops_path)
        try:
            next_id = max(shops_data["shop_id"]) + 1
        except ValueError:
            next_id = 1
        shops_data = shops_data.append(
            {"shop_id": next_id, "location": location, "type": "Standard"}, ignore_index=True)
        shops_data.to_csv(shops_path, index=False)

        availability_data = pd.read_csv(availability_path)
        if distillery_list is not None:
            availability_data[next_id] = [1 if availability_data.iloc[i, 0] in distillery_list
                                          else 0 for i in range(len(availability_data))]
        else:
            availability_data[next_id] = [0] * len(availability_data)
        availability_data.to_csv(availability_path, index=False)
        return {"data": shops_data.loc[shops_data["shop_id"] == next_id].to_dict()}, 200

    @staticmethod
    def add_popup(location, date, discount, distillery_list):
        """Adds Pop-up shop with associated discount, location, date and its product availability(limited to 3
        distilleries)"""
        if len(distillery_list) > 3:
            return {"ERROR": "A Pop-Up shop is limited to a maximum of three distilleries."}, 400
        else:
            shops_data = pd.read_csv(shops_path)
            try:
                next_id = max(shops_data["shop_id"]) + 1
            except ValueError:
                next_id = 1
            shops_data = shops_data.append(
                {"shop_id": next_id, "location": location, "type": "Pop-up",
                 "date": date, "discount": discount}, ignore_index=True)
            shops_data.to_csv(shops_path, index=False)
            availability_data = pd.read_csv(availability_path)
            availability_data[next_id] = [1 if availability_data.iloc[i, 0] in distillery_list else 0 for i in range(
                len(availability_data))]
            availability_data.to_csv(availability_path, index=False)
            return {"data": shops_data.loc[shops_data["shop_id"] == next_id].to_dict()}, 200

    @staticmethod
    def delete_shop(shop_id):
        """Deletes a specified shop in database"""
        try:
            availability_data = pd.read_csv(availability_path)
            shops_data = pd.read_csv(shops_path)
            del availability_data[str(shop_id)]
            shops_data = shops_data.loc[shops_data['shop_id'] != shop_id]
            if str(shop_id) not in availability_data.columns and str(shop_id) not in shops_data.columns:
                availability_data.to_csv(availability_path, index=False)
                shops_data.to_csv(shops_path, index=False)
                return {'MESSAGE': f"Shop {shop_id} has been successfully removed."}, 200
        except KeyError:
            return {'ERROR': f"Shops in availability.csv: {list(availability_data.columns)}"
                             f" // Shops in shops.csv: {list(shops_data['shop_id'])}"}, 400

    @staticmethod
    def add_distillery(distillery, taste_list, postcode=None, latitude=None, longitude=None):
        """Adds information (new distillery) to the taste categories dataset"""
        whiskey_data = pd.read_csv(whiskey_path)
        availability_data = pd.read_csv(availability_path)
        try:
            len(taste_list) == 12
        except ValueError:
            return {"ERROR": "The list with taste categories is invalid."}, 400
        try:
            next_id = max(whiskey_data["RowID"]) + 1
        except ValueError:
            next_id = 1
        whiskey_data = whiskey_data.append(
            {"RowID": next_id, "Distillery": distillery, "Body": taste_list[0], "Sweetness": taste_list[1],
             "Smoky": taste_list[2], "Medicinal": taste_list[3], "Tobacco": taste_list[4], "Honey": taste_list[5],
             "Spicy": taste_list[6], "Winey": taste_list[7], "Nutty": taste_list[8], "Malty": taste_list[9],
             "Fruity": taste_list[10], "Floral": taste_list[11], "Postcode": postcode, "Latitude": latitude,
             "Longitude": longitude}, ignore_index=True)
        whiskey_data.to_csv(whiskey_path, index=False)
        availability_data.loc[len(availability_data)] = [distillery] + ([0] * (len(availability_data.columns) - 1))
        availability_data.to_csv(availability_path, index=False)
        return {"data": whiskey_data.loc[whiskey_data["RowID"] == next_id].to_dict()}, 200

    @staticmethod
    def add_review(distillery, name, category, points, price, currency, description):
        """Adds information (new whiskey) to the review dataset"""
        review_data = pd.read_csv(review_path)
        try:
            next_id = max(review_data["id"]) + 1
        except ValueError:
            next_id = 1
        review_data = review_data.append(
            {"id": next_id, "distillery": distillery, "name": name, "category": category, "points": points,
             "price": price, "currency": currency, "description": description}, ignore_index=True)
        review_data.to_csv(review_path, index=False)
        return {"data": review_data.loc[review_data["id"] == next_id].to_dict()}, 200
