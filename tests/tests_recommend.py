import pytest
import pandas as pd
from recommendation import Recommend as Rec

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


@pytest.mark.parametrize('shop, distilleries', [
    (6, ["ArranIsleOf", "Clynelish", "Cragganmore"]),
    (7, ["Bowmore", "Longmorn", "Teaninich"])
])
def test_get_availability(shop, distilleries):
    assert Rec.get_availability(shop) == distilleries


@pytest.mark.parametrize('distilleries, characteristics, output', [
    (['Balblair', 'Deanston', 'Speyburn'], ['Body', 'Medicinal', 'Honey'], pd.DataFrame(
        {'Distillery': ['Balblair', 'Deanston', 'Speyburn'], 'Body': [2, 2, 2], 'Medicinal': [1, 0, 0],
         'Honey': [0, 2, 2]})),
    (['Aberfeldy', 'Aberlour', 'AnCnoc'], None,
     pd.read_csv(whiskey_path).iloc[0:3, 1:14]),
    (None, None, pd.read_csv(whiskey_path).iloc[:, 1:14]),
    (None, ['Body', 'Sweetness', 'Smoky'],
     pd.read_csv(whiskey_path).iloc[:, 1:5])
])
def test_get_characteristics(distilleries, characteristics, output):
    character = Rec.get_characteristics(distilleries, characteristics).reset_index(drop=True)
    assert character.equals(output)


indices = [[0, 17, 15, 7, 71, 52, 73, 14, 43, 70, 78], [1, 75, 70, 14, 48, 11, 52, 43, 15, 65, 56],
           [2, 22, 78, 41, 28, 8, 73, 71, 25, 0, 15], [3, 77, 23, 57, 58, 21, 66, 55, 39, 68, 74],
           [4, 67, 29, 73, 17, 53, 15, 0, 8, 7, 28]]
response = [['BlairAthol', 'Strathisla', 'Cardhu', 'Benromach', 'RoyalLochnagar'],
            ['Aberfeldy', 'Aberlour', 'AnCnoc', 'Aberfeldy', 'Aberlour']]
response_2 = [['BlairAthol', 'Strathisla', 'Cardhu', 'Talisker', 'OldFettercairn'],
              ['Aberfeldy', 'Aberlour', 'AnCnoc', 'Ardbeg', 'Ardmore']]
response_3 = [['BlairAthol', 'Benromach', 'Auchroisk', 'Scapa', 'Glenturret'], ['Aberfeldy', 'Aberfeldy', 'Aberfeldy',
                                                                                'Aberfeldy', 'Aberfeldy']]


@pytest.mark.parametrize('whiskey_data, distilleries, nearest_neighbours, output', [
    (pd.read_csv(whiskey_path),
     ['Aberfeldy', 'Aberlour', 'AnCnoc'],
     indices, response),
    (pd.read_csv(whiskey_path),
     ['Aberfeldy', 'Aberlour', 'AnCnoc', 'Ardbeg', 'Ardmore'],
     indices, response_2),
    (pd.read_csv(whiskey_path),
     ['Aberfeldy'],
     indices, response_3)
])
def test_provide_five(whiskey_data, distilleries, nearest_neighbours, output):
    rec_five = Rec.provide_five(whiskey_data, distilleries, nearest_neighbours)
    assert rec_five == output


@pytest.mark.parametrize('whiskey_data, available, output', [
    (pd.read_csv(whiskey_path).iloc[0:3, 1:14],
     pd.read_csv(whiskey_path).iloc[3:, 1:14], response),
    (pd.read_csv(whiskey_path).iloc[0:5, 1:14],
     pd.read_csv(whiskey_path).iloc[:, 1:14], response_2),
    (pd.read_csv(whiskey_path).iloc[:1, 1:14],
     pd.read_csv(whiskey_path).iloc[:, 1:14], response_3)
])
def test_knn_recommend(whiskey_data, available, output):
    rec_out = Rec.knn_recommend(whiskey_data, available)
    assert len(rec_out[0]) == len(output[0])
    assert len(rec_out[1]) == len(output[1])


data = pd.read_csv(review_path)


@pytest.mark.parametrize('distilleries, output', [
    (['Aberfeldy'], data[data['distillery'].isin(['Aberfeldy'])]),
    (['Aberfeldy', 'Dalmore', 'Bowmore'], data[data['distillery'].isin(['Aberfeldy', 'Dalmore',
                                                                        'Bowmore'])])
])
def test_get_points(distilleries, output):
    rev_out = Rec.get_points(distilleries)
    assert rev_out.equals(output)


@pytest.mark.parametrize('shop, output', [
    (6, ["Cragganmore", "Clynelish"]),
    (7, ["Bowmore", "Longmorn", "Teaninich"])
])
def test_recommend_review(shop, output):
    rec_rev = Rec.recommend_review(shop)
    assert rec_rev == output
