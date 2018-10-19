from collections import Iterable

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

from ..orm import SangrealSession


class DataBase:
    def __init__(self, bind, schema=None):
        self.bind = bind
        self.metadata = MetaData(bind=bind, schema=schema)
        self.Base = declarative_base(metadata=self.metadata)
        self.session = SangrealSession(bind)
        self.tables = self._get_tables(bind, schema)
        for table in self.tables:
            setattr(self, table, 'None')

    def __getattribute__(self, table_name):
        if object.__getattribute__(self, table_name) == 'None':
            setattr(self, table_name, self._reflect_table(table_name))
        return object.__getattribute__(self, table_name)

    def __getattr__(self, name):
        raise ValueError(f'<{name}> is not the right table of this database, \
please check the table name!')

    def __repr__(self):
        return str(self.bind).replace('Engine', 'DataBase')

    def _reflect_table(self, table_name):
        self.metadata.reflect(only=[table_name])
        Base = automap_base(metadata=self.metadata)
        Base.prepare()
        try:
            return Base.classes[table_name]
        except KeyError:
            raise ValueError(f"There must be a primary key in {table_name}!")

    @staticmethod
    def _get_tables(bind, schema):
        insp = reflection.Inspector.from_engine(bind=bind)
        tables = insp.get_table_names(schema=schema)
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

    def commit(self):
        self.session.commit()

    def flush(self, objects=None):
        self.session.flush(objects=objects)

    def rollback(self):
        self.session.rollback()

    def create_all(self, tables=None, checkfirst=True):
        self.metadata.create_all(tables=tables, checkfirst=checkfirst)


if __name__ == '__main__':
    engine = create_engine("mysql://root:123@localhost:3306/test?charset=utf8")
    db0 = DataBase(engine)
    print(db0)
    df = db0.query(db0.TEST.fuck).filter().to_df()
    print(df)
    print(db0.tables)

    from sqlalchemy import Column, Integer, String

    class User(db0.Base):
        __tablename__ = 'fuckers'
        id = Column(Integer, primary_key=True)
        name = Column(String(20))
        fullname = Column(String(20))
        password = Column(String(20))

        def __repr__(self):
            return "<User(name='%s', fullname='%s', password='%s')>" % (
                self.name, self.fullname, self.password)

    db0.create_all()
