import reprlib
import pandas as pd
from collections import Iterable

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

from sangreal_db.orm import SangrealSession


class DataBase:
    """class for easy to use orm of your database/
    
    Raises:
        ValueError -- [bind must be sth like sqlalchemy's engine]
    
    Returns:
        [instance of DataBase] -- []
    """

    def __init__(self, bind, schema=None):
        if isinstance(bind, str):
            bind = create_engine(bind)
        self._bind = bind
        self._schema = schema
        self._metadata = MetaData(bind=bind, schema=schema)
        self.Base = declarative_base(metadata=self._metadata)
        self._session = SangrealSession(bind)
        self.tables = self._get_tables(bind, schema)
        for table in self.tables:
            setattr(self, table, 'None')

    def __getattribute__(self, table_name):
        if object.__getattribute__(self, table_name) == 'None':
            setattr(self, table_name, self._reflect_table(table_name))
        return object.__getattribute__(self, table_name)

    def __getattr__(self, name):
        raise AttributeError(
            f'<{name}> is not the right table name, such as {reprlib.repr(self.tables)}.'
        )

    def __repr__(self):
        return str(self._bind).replace(
            type(self._bind).__name__,
            type(self).__name__)

    @property
    def bind(self):
        return self._bind

    def _reflect_table(self, table_name):
        self._metadata.reflect(only=[table_name])
        Base = automap_base(metadata=self._metadata)
        Base.prepare()
        try:
            return Base.classes[table_name]
        except KeyError:
            raise ValueError(f"There must be a primary key in {table_name}! \
or <{table_name}> is not the right table name, such as {reprlib.repr(self.tables)}."
                             )

    @staticmethod
    def _get_tables(bind, schema):
        insp = reflection.Inspector.from_engine(bind=bind)
        tables = insp.get_table_names(schema=schema)
        return tables

    def query(self, *columns):
        """[session.query]
        
        Returns:
            [Query] -- [sqlalchemy Query cls]
        """

        return self._session.query(*columns)

    def update(self, t_obj):
        """[update table]
        
        Arguments:
            t_obj {[objs of DeclarativeMeta]} -- [update the table]
        """

        if isinstance(t_obj, Iterable):
            self._session.add_all(t_obj)
        else:
            self._session.add(t_obj)

    def insert(self, table, insert_obj, ignore=True):
        """[insert bulk data]
        
        Arguments:
            table {[DeclarativeMeta cls]} -- [reflection of table]
            insert_obj {[pd.DataFrame or list of dicts]} -- [insert_obj]
        
        Keyword Arguments:
            ignore {bool} -- [wether ignore exception or not] (default: {True})
        
        Raises:
            ValueError -- [f"The {reprlib.repr(insert_obj)} must be list of dicts type!"]
        
        Returns:
            [type] -- [description]
        """

        if isinstance(insert_obj, pd.DataFrame):
            insert_obj = insert_obj.to_dict(orient='records')
        elif not isinstance(insert_obj, list):
            raise ValueError(
                f"The {reprlib.repr(insert_obj)} must be list of dicts type!")

        ignore_str = 'IGNORE' if ignore else ''
        return self._session.execute(
            table.__table__.insert().prefix_with(ignore_str), insert_obj)

    def delete(self, t_obj):
        return self._session.delete(t_obj)

    def close(self):
        return self._session.close()

    def commit(self):
        return self._session.commit()

    def flush(self, objects=None):
        return self._session.flush(objects=objects)

    def rollback(self):
        return self._session.rollback()

    def create_all(self, tables=None, checkfirst=True):
        result = self._metadata.create_all(tables=tables, checkfirst=checkfirst)
        self.__init__(self._bind, self._schema)
        return result


if __name__ == '__main__':
    pass
