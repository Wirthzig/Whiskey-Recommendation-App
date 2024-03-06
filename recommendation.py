import pandas as pd
from sklearn.neighbors import NearestNeighbors
from itertools import compress

# paths ########################################
purchases_path = "data/purchases.csv"
whiskey_path = "data/whiskey86.csv"
review_path = "data/whiskey_review2020.csv"
customers_path = "data/customers.csv"
shops_path = "data/shops.csv"
availability_path = "data/availability.csv"
################################################


class Recommend:
    """Includes functions to recommend whiskey distilleries based on customer preferences. Recommendations
    exclusively only include distilleries available in the shops but can be based on unavailable distilleries. One
    preferred distillery can be indicated if none exist in the database. Four distilleries can be added by choice (
    liked and or already bought by customer). In the case that the user has no preferences, up to three suggestions
    ranked by the average value of reviews from all the products for a given distillery are returned. """

    @staticmethod
    def knn_recommend(target, available):
        """Recommends new distilleries based on provided ones, excluding the input. It will recommend at least one
        distillery per given distillery."""
        available = available.loc[~available['Distillery'].isin(target['Distillery'])]
        available = available.filter(items=list(target))
        taste_data = pd.concat([target, available])
        model_data = taste_data.filter(items=list(taste_data)[1:])
        closest = NearestNeighbors(n_neighbors=11, algorithm='ball_tree').fit(model_data)
        distances, indices = closest.kneighbors(model_data)
        distillery = list(target['Distillery'])
        return Recommend.provide_five(taste_data, distillery, indices)

    @staticmethod
    def provide_five(taste_data, distilleries, indices):
        """Takes a list of at least one distillery and returns a list of exactly five recommendations.
        For every provided distillery in the list it will return at least one recommendation. It will not
        recommend a distillery, if it is already contained within the provided
        list of distilleries. Instead, it will provide a less similar distillery,
        that is not included in the input list."""
        close_list = [list(i) for i in indices]
        whiskey = [i for i in range(len(indices))]
        closest_five = list(compress(close_list, list(taste_data['Distillery'].isin(distilleries))))
        whiskey = list(compress(whiskey, list(taste_data['Distillery'].isin(distilleries))))
        recommended_from, recommendation = [], []
        i, j = 0, 0
        while True:
            if len(recommendation) < 5 and closest_five[i][j] not in whiskey \
                    and closest_five[i][j] not in recommendation:
                recommendation.append(closest_five[i][j])
                recommended_from.append(whiskey[i])
                i += 1
                j = 0
                if i == len(closest_five):
                    i = 0
            elif j < 10:
                j += 1
            elif j > 10:
                j = 0
                i += 1
            elif len(recommendation) == 5 or i == len(closest_five):
                break
        recommendation = [taste_data['Distillery'].tolist()[i] for i in recommendation]
        recommended_from = [taste_data['Distillery'].tolist()[i] for i in recommended_from]
        list_out = [recommendation, recommended_from]
        return list_out

    @staticmethod
    def get_availability(shop):
        """Returns a dataframe that includes all distilleries that are available in a given shop and their
        corresponding indices"""
        df = pd.read_csv(availability_path)
        df = df[df[str(shop)] == 1]
        return list(df["shop_id"])

    @staticmethod
    def get_characteristics(distillery=None, characteristics=None):
        """Provides specified characteristics for given distilleries. If no distilleries are specified the
        information for all distilleries will be returned. If no characteristics are specified, all characteristics
        will be returned."""
        df = pd.read_csv(whiskey_path)
        if distillery is None:
            distillery = list(df['Distillery'])

        if characteristics is None:
            characteristics = ['Body', 'Sweetness', 'Smoky', 'Medicinal', 'Tobacco', 'Honey', 'Spicy',
                               'Winey', 'Nutty', 'Malty', 'Fruity', 'Floral']
        characteristics = ['Distillery'] + characteristics
        df = df.filter(items=characteristics)
        df = df.loc[df['Distillery'].isin(distillery)]
        df['aux'] = pd.Categorical(df['Distillery'], categories=distillery)
        df = df.sort_values(by='aux')
        del df['aux']
        return df

    @staticmethod
    def get_points(distillery=None, name=None):
        """Retrieves scores associated with given distilleries"""
        df = pd.read_csv(review_path)
        if distillery is None and name is None:
            distillery = list(df['distillery'])
            return df.loc[df['distillery'].isin(distillery)]
        elif name is not None:
            return df.loc[df['name'].isin(name)]
        else:
            return df.loc[df['distillery'].isin(distillery)]

    @staticmethod
    def recommend_review(shop):
        """Returns up to three unique distilleries ranked by the average value of reviews from all products for a
        given distillery"""
        available = Recommend.get_availability(shop)
        review = Recommend.get_points(available)
        grouped = review.groupby('distillery').mean().sort_values(by=['points'], ascending=False)
        return list(grouped.iloc[:3].index)
