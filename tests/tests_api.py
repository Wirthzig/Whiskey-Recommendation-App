import pandas as pd
import requests


def test_start_home():
    response = requests.get("http://127.0.0.1:5000/")
    assert str(response) == "<Response [200]>"


def test_start_employee():
    response = requests.get("http://127.0.0.1:5000/employee")
    assert str(response) == "<Response [200]>"


def test_start_manager():
    response = requests.get("http://127.0.0.1:5000/manager")
    assert str(response) == "<Response [200]>"


def test_api_register_purchase():
    response = requests.get("http://127.0.0.1:5000/employee/register_purchase?customer_id=1&whiskey=Black+Bowmore+42"
                            "+year+old+1964+vintage%2C+40.5%25&recommended=yes")
    assert str(response) == "<Response [200]>"


def test_api_get_customer():
    response = requests.get("http://127.0.0.1:5000/employee/get_customer?customer_id=0")
    assert str(response) == "<Response [200]>"
    response = requests.get("http://127.0.0.1:5000/employee/get_customer?customer_id=WRONGINPUT")
    assert str(response) == "<Response [400]>"


def test_api_put_favourite():
    response = requests.get("http://127.0.0.1:5000/employee/put_favourite?customer_id=0&favourite=test-distillery")
    assert str(response) == "<Response [200]>"
    response = requests.get(
        "http://127.0.0.1:5000/employee/put_favourite?customer_id=WRONGINPUT&favourite=test-distillery")
    assert str(response) == "<Response [400]>"


def test_api_delete_favourite():
    response = requests.get("http://127.0.0.1:5000/employee/delete_favourite?customer_id=0")
    assert str(response) == "<Response [200]>"
    response = requests.get("http://127.0.0.1:5000/employee/delete_favourite?customer_id=WRONGINPUT")
    assert str(response) == "<Response [400]>"
    requests.get("http://127.0.0.1:5000/employee/put_favourite?customer_id=0&favourite=test-distillery")


def test_api_recommend_whiskey():
    response = requests.get(
        "http://127.0.0.1:5000/employee/recommend?customer_id=&shop_id=1&distilleries=&distilleries=&distilleries"
        "=&distilleries=&distilleries=")
    assert str(response) == "<Response [200]>"
    response = requests.get("http://127.0.0.1:5000/employee/recommend?customer_id=&shop_id=WRONGINPUT&distilleries"
                            "=&distilleries=&distilleries=&distilleries=&distilleries=")
    assert str(response) == "<Response [400]>"


def test_api_get_review():
    response = requests.get(
        "http://127.0.0.1:5000/employee/get_review?whiskey=Brora%2C+30+year+old+%282009+Release%29%2C+53.2%25")
    assert str(response) == "<Response [200]>"
    response = requests.get("http://127.0.0.1:5000/employee/get_review?whiskey=WRONGINPUT")
    assert str(response) == "<Response [400]>"


def test_api_get_popup():
    response = requests.get("http://127.0.0.1:5000/employee/get_popup?customer_id=WRONGINPUT")
    assert str(response) == "<Response [400]>"


def test_api_register_customer():
    response = requests.get("http://127.0.0.1:5000/manager/register_customer?favourite=")
    assert str(response) == "<Response [200]>"


def test_api_delete_customer():
    test_customer = requests.get("http://127.0.0.1:5000/manager/register_customer?favourite=")
    id = [*test_customer.json()["data"]["customer_id"].values()][0]
    response = requests.get(f"http://127.0.0.1:5000/manager/delete_customer?customer_id={id}")
    assert str(response) == "<Response [200]>"


def test_api_add_shop():
    shops_data = pd.read_csv('../data/shops.csv')
    response = requests.get("http://127.0.0.1:5000/manager/add_shop?location=No_Place&distilleries=Aberfeldy"
                            "&distilleries=Aberlour&distilleries=AnCnoc&distilleries=Ardbeg")
    assert str(response) == "<Response [200]>"
    shops_data.to_csv('../data/shops.csv')


def test_api_add_popup():
    shops_data = pd.read_csv('../data/shops.csv')
    response = requests.get('http://127.0.0.1:5000/manager/add_popup?location=Taipe&date=2222-11-26&discount=100'
                            '&distilleries=Bowmore&distilleries=Bladnoch&distilleries=Benromach')
    assert str(response) == "<Response [200]>"
    shops_data.to_csv('../data/shops.csv')


def test_api_delete_shop():
    response = requests.get("http://127.0.0.1:5000/manager/add_shop?location=Places&distilleries=Aberfeldy"
                            "&distilleries=Aberlour&distilleries=AnCnoc&distilleries=Ardbeg")
    id = [*response.json()["data"]["shop_id"].values()][0]
    response_1 = requests.get(f"http://127.0.0.1:5000/manager/delete_shop?shop_id={id}")
    assert str(response_1) == "<Response [200]>"


def test_api_add_distillery():
    whiskey_data = pd.read_csv('../data/whiskey86.csv')
    availability_data = pd.read_csv('../data/availability.csv')
    response = requests.get("http://127.0.0.1:5000/manager/add_distillery?distillery=Diss-Tillary&taste_list=4"
                            "&taste_list=0&taste_list=0&taste_list=0&taste_list=0&taste_list=0&taste_list=0"
                            "&taste_list=0&taste_list=0&taste_list=0&taste_list=0&taste_list=0&postcode=666-666"
                            "&latitude=69&longitude=90")
    assert str(response) == "<Response [200]>"
    whiskey_data.to_csv("../data/whiskey86.csv", index=False)
    availability_data.to_csv("../data/availability.csv", index=False)


def test_api_add_review():
    review_data = pd.read_csv('../data/whiskey_review2020.csv')
    response = requests.get("http://127.0.0.1:5000/manager/add_review?distillery=Caol_Ila&name=Alex&category=krabumms"
                            "&points=100000&price=50000000000000&currency=%24&description=Pretty+expensive%2C+but"
                            "+gets+you+drunk%21")
    assert str(response) == "<Response [200]>"
    review_data.to_csv('../data/whiskey_review2020.csv', index=False)
