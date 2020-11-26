from sqlalchemy.orm import Query
import pandas as pd


class SangrealQuery(Query):
    def to_df(self, **kwargs):
        """[pandas.read_sql]
        
        Arguments:
            Query {[type]} -- [description]
        
        Returns:
            [pd.DataFrame or generate] -- [description]
        """

        return pd.read_sql(sql=self.statement, con=self.session.bind, **kwargs)
