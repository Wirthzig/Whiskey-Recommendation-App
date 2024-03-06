from employee import Employee
import pandas as pd
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


def test_register_purchase():
    customers_data = pd.read_csv(customers_path)
    customer_num_of_purchases_before = customers_data.loc[customers_data["customer_id"] == 0, "num_of_purchases"].values
    purchases_data_before = pd.read_csv(purchases_path)
    Employee.register_purchase(0, "Black Bowmore 42 year old 1964 vintage, 40.5%", "no")
    customers_data = pd.read_csv(customers_path)
    customer_num_of_purchases_after = customers_data.loc[customers_data["customer_id"] == 0, "num_of_purchases"].values
    purchases_data_after = pd.read_csv(purchases_path)

    # reset dataset to preliminary stage
    purchases_data = purchases_data_after.iloc[:-1, ]
    purchases_data.to_csv(purchases_path, index=False)
    customers_data.loc[customers_data["customer_id"] == 0, "num_of_purchases"] -= 1
    customers_data.loc[customers_data["customer_id"] == 0, "status"] = "platinum"
    customers_data.to_csv(customers_path, index=False)
    assert (customer_num_of_purchases_before + 1) == customer_num_of_purchases_after
    assert (len(purchases_data_before) + 1) == len(purchases_data_after)


def test_get_customer():
    assert Employee.get_customer(0) == ({'customer_id': 0, 'discount': '15%', 'favourite distillery': 'test-distillery',
                                        'num_of_purchases': 1000, 'status': 'platinum'},200)


def test_get_favorite():
    assert Employee.get_favourite(0) == ["test-distillery"]


def test_put_favourite():
    test_output = Employee.put_favourite(0, "new-test-distillery")
    # reset dataset to preliminary stage
    Employee.put_favourite(0, "test-distillery")
    assert test_output == ({'data': {'customer_id': {0: 0},
                                     'favourite': {0: 'new-test-distillery'},
                                     'num_of_purchases': {0: 1000},
                                     'status': {0: 'platinum'}}}, 200)


def test_delete_favorite():
    test_output = Employee.delete_favourite(0)
    # reset dataset to preliminary stage
    Employee.put_favourite(0, "test-distillery")
    assert test_output == ({'data': {'customer_id': {0: 0},
                                     'favourite': {0: ''},
                                     'num_of_purchases': {0: 1000},
                                     'status': {0: 'platinum'}}}, 200)


def test_get_purchases():
    assert Employee.get_purchases(0) == ['test-distillery']


def test_recommend():
    assert Employee.recommend(1, customer_id=28)[1] == 200
    # TODO change because its API LENGTH


def test_get_review():
    assert Employee.get_review("Black Bowmore 42 year old 1964 vintage, 40.5%") == (
    {0: {0: "What impresses me most is how this whisky evolves; it's incredibly "
            'complex',
         1: ' On the nose and palate, this is a thick, viscous, whisky with notes '
            'of sticky toffee, earthy oak, fig cake, roasted nuts, fallen fruit, '
            'pancake batter, black cherry, ripe peach, dark chocolate-covered '
            'espresso bean, polished leather, tobacco, a hint of wild game, and '
            'lingering, leafy damp kiln smoke',
         2: ' Flavors continue on the palate long after swallowing',
         3: ' This is what we all hope for (and dream of) in an older whisky!'}}, 200)

    assert Employee.get_review("not existing whiskey") == ({'ERROR': 'The whiskey is not existing in our database'}, 400)


def test_get_popup():
    customers_data = pd.read_csv(customers_path)
    customers_data.loc[customers_data["customer_id"] == 0, "status"] = "platinum"
    customers_data.to_csv(customers_path, index=False)
    shops_data = pd.read_csv(shops_path)
    shops_data = shops_data.append(
        {"shop_id": "0", "location": "test-location", "type": "Pop-up",
         "date": "test-date", "discount": "test-discount"}, ignore_index=True)
    shops_data.to_csv(shops_path, index=False)
    test_output = Employee.get_popup(0)
    index = len(shops_data) - 1

    # reset dataset to preliminary stage
    shops_data = pd.read_csv(shops_path)
    shops_data = shops_data.loc[shops_data['shop_id'] != 0]
    shops_data.to_csv(shops_path, index=False)
    customers_data = pd.read_csv(customers_path)
    customers_data.loc[customers_data["customer_id"] == 0, "status"] = "basic"
    customers_data.to_csv(customers_path, index=False)
    assert test_output[0][index] == {'date': 'test-date', 'discount': 'test-discount', 'location': 'test-location',
                                     'shop_id': 0}
    customers_data.loc[customers_data["customer_id"] == 0, "status"] = "platinum"



def test_update_status():
    customers_data = pd.read_csv(customers_path)
    customers_data.loc[customers_data["customer_id"] == 0, "status"] = "platinum"
    customers_data.to_csv(customers_path, index=False)
    Employee.update_status()
    customers_data = pd.read_csv(customers_path)
    assert customers_data.loc[customers_data["customer_id"] == 0, "status"].values == "basic"
    # For the API tests to run appropiately, we need to change the status of the test customer back to platinum
    customers_data.loc[customers_data["customer_id"] == 0, "status"] = "platinum"
    customers_data.to_csv(customers_path, index=False)

