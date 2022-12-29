from scorer import Scorer
from sklearn.metrics import mean_absolute_error
import pandas as pd


class MyScorer(Scorer):

    def __init__(
            self, 
            public_path, 
            private_path, 
            metric
            ):
        super().__init__(public_path, private_path, metric)

    def calculate_score(
            self,
            submission_path,
            submission_type
            ):
        df_submission = pd.read_csv(submission_path)

        if submission_type == 'private':
            df_key = self.df_private_key
        else: 
            df_key = self.df_public_key

        # if input length not same, return None
        if len(df_key) != len(df_submission):
            print(len(df_key), len(df_submission))
            return ("NOT SAME LENGTH", None)
        
        df_merged = df_key.merge(df_submission, how ='inner', 
                                left_on='index', right_on='index', # adjust `on` columns as params
                                suffixes=('_key', '_submission')) 
        # When submission and key have different index value
        if len(df_key) != len(df_merged):
            return ("NOT SAME INDEX", None)

        # data size is same, time to get score
        y_key = df_merged['pkbhx_key']
        y_submission = df_merged['pkbhx_submission']

        if y_submission.isna().sum() > 0:
            return ("SUBMISSION HAS NULL VALUE", None)

        score = self.metric(y_key, y_submission)
        return ("SUBMISSION SUCCESS", score)


def my_metric(key, submission):
    return 100 * mean_absolute_error(key, submission)


if __name__ == "__main__":

    metric = my_metric #change the metric using sklearn function
    scorer = MyScorer(public_path = './master_key/public_key.csv', 
                    private_path = './master_key/private_key.csv', 
                    metric = metric) #change the metric using sklearn function
    score = scorer.calculate_score("./temp/test_private_submission-2.csv", "private")
    print(score)
