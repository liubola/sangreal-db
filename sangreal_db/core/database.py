from collections import Iterable

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base

from ..orm import SangrealSession


class DataBase:
    metadata = MetaData()

    def __init__(self, bind, schema=None):
        self.bind = bind
        self.schema = schema
        self.session = SangrealSession(bind)
        self.tables = self._get_tables(bind)
        for table in self.tables:
            setattr(self, table, 'None')

    def __getattribute__(self, table_name):
        if object.__getattribute__(self, table_name) == 'None':
            setattr(self, table_name, self._reflect_table(table_name))
        return object.__getattribute__(self, table_name)

    def __getattr__(self, name):
        raise ValueError(f'<{name}> is not the right table of this database, \
please check the table name!')

    def _reflect_table(self, table_name):
        self.metadata.reflect(
            bind=self.bind, schema=self.schema, only=[table_name])
        Base = automap_base(metadata=self.metadata)
        Base.prepare()
        try:
            return Base.classes[table_name]
        except KeyError:
            raise ValueError(f"There must be a primary key in {table_name}!")

    def _get_tables(self, bind):
        insp = reflection.Inspector.from_engine(bind)
        tables = insp.get_table_names(schema=self.schema, )
        return tables

    def query(self, *columns):
        return self.session.query(*columns)

    def update(self, t_obj):
        if isinstance(t_obj, Iterable):
            self.session.add_all(t_obj)
        else:
            self.session.add(t_obj)
        self.session.commit()

    def delete(self, t_obj):
        self.session.delete(t_obj)
        self.session.commit()

    def close(self):
        self.session.close()


if __name__ == '__main__':
    engine = create_engine("mysql://root:123@localhost:3306/blog?charset=utf8")
    db0 = DataBase(engine)
    df = db0.query(db0.users.id).filter().to_df()
    print(df)
    print(db0.tables)
