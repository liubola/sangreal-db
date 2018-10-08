from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.engine import reflection

from ..orm import SangrealSession


class DataBase:
    metadata = MetaData()

    def __init__(self, bind):
        self.bind = bind
        self.session = SangrealSession(bind)
        self.tables = self.get_tables(bind)
        for table in self.tables:
            setattr(self, table, None)

    def __getattribute__(self, name):
        if object.__getattribute__(self, name) is None:
            setattr(self, name, self.reflect_table(name))
        return object.__getattribute__(self, name)

    def __getattr__(self, name):
        raise ValueError(f'<{name}> is not the right table of this database, \
please check the table name!')

    def reflect_table(self, table_name):
        table = Table(
            table_name, self.metadata, autoload=True, autoload_with=self.bind)

        return table

    @staticmethod
    def get_tables(bind):
        insp = reflection.Inspector.from_engine(bind)
        tables = insp.get_table_names()
        return tables

    def query(self, table):
        return self.session.query(table)


if __name__ == '__main__':
    engine = create_engine(
        "mysql://root:123@localhost:3306/blog?charset=utf8"
    )
    db0 = DataBase(engine)
    df = db0.query(db0.users).to_df()
    print(df)
    print(db0.tables)
