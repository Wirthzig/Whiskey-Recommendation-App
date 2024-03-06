import pandas as pd
from manager import Manager
import pytest
import os

# paths ########################################
purchases_path = "data/purchases.csv"
whiskey_path = "data/whiskey86.csv"
review_path = "data/whiskey_review2020.csv"
customers_path = "data/customers.csv"
shops_path = "data/shops.csv"
availability_path = "data/availability.csv"
################################################


os.chdir('../')


def test_register_customer():
    Manager.register_customer("some favourite whiskey")
    customers_data = pd.read_csv(customers_path)
    assert customers_data["favourite"].iloc[-1] == "some favourite whiskey"
    customers_data = customers_data.loc[customers_data["favourite"] != "some favourite whiskey"]
    customers_data.to_csv(customers_path, index=False)


def test_delete_customer():
    Manager.register_customer("some favourite whiskey")
    Manager.register_customer("other favourite whiskey")
    customers_data = pd.read_csv(customers_path)
    Manager.delete_customer(max(customers_data["customer_id"]))
    customers_data = pd.read_csv(customers_path)
    assert customers_data["favourite"].iloc[-1] == "some favourite whiskey"
    customers_data = customers_data.loc[customers_data["favourite"] != "some favourite whiskey"]
    customers_data.to_csv(customers_path, index=False)


@pytest.mark.parametrize('location, distillery_list', [
    ("location one", ["Aberfeldy", "Bladnoch", "Dalmore"]),
    ("location two", [])
])
def test_add_shop(location, distillery_list):
    Manager.add_shop(location, distillery_list)
    shop_data = pd.read_csv(shops_path)
    availability_data = pd.read_csv(availability_path)
    assert shop_data["location"].iloc[-1] == location
    availability_data.set_index("shop_id", inplace=True)
    if distillery_list:
        for distillery in availability_data.loc[distillery_list][str(max(shop_data["shop_id"]))]:
            assert distillery == 1
    else:
        for distillery in availability_data.loc[distillery_list][str(max(shop_data["shop_id"]))]:
            assert distillery == 0
    Manager.delete_shop(max(shop_data["shop_id"]))


def test_add_popup():
    distillery_list = ["Aberfeldy", "Bladnoch"]
    Manager.add_popup("new location", "10.02.2022", 5, distillery_list)
    shop_data = pd.read_csv(shops_path)
    availability_data = pd.read_csv(availability_path)
    assert shop_data["location"].iloc[-1] == "new location"
    assert shop_data["type"].iloc[-1] == "Pop-up"
    availability_data.set_index("shop_id", inplace=True)
    for distillery in availability_data.loc[distillery_list][str(max(shop_data["shop_id"]))]:
        assert distillery == 1
    Manager.delete_shop(max(shop_data["shop_id"]))


def test_delete_shop():
    Manager.add_shop("new location", [])
    Manager.add_shop("other new location", [])
    shop_data = pd.read_csv(shops_path)
    Manager.delete_shop(max(shop_data["shop_id"]))
    shop_data = pd.read_csv(shops_path)
    assert shop_data["location"].iloc[-1] == "new location"
    Manager.delete_shop(max(shop_data["shop_id"]))


def test_add_distillery():
    whiskey_data_original = pd.read_csv(whiskey_path)
    availability_data_original = pd.read_csv(availability_path)
    Manager.add_distillery(distillery="New distillery", taste_list=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    whiskey_data = pd.read_csv(whiskey_path)
    assert whiskey_data["Distillery"].iloc[-1] == "New distillery"
    whiskey_data_original.to_csv(whiskey_path, index=False)
    availability_data_original.to_csv(availability_path, index=False)


def test_add_review():
    review_data_original = pd.read_csv(review_path)
    Manager.add_review("New distillery", "new name", "single", 93, 19,"$", "description")
    review_data = pd.read_csv(review_path)
    assert review_data["distillery"].iloc[-1] == "New distillery"
    review_data_original.to_csv(review_path, index=False)
