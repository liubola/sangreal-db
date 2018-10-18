from sqlalchemy.orm import Query
import pandas as pd


class SangrealQuery(Query):
    def to_df(self):
        return pd.read_sql(self.statement, self.session.bind)
