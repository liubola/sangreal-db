from sangreal_db import DataBase
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

engine = create_engine("mysql://root:123@localhost:3306/test?charset=utf8")
db0 = DataBase(engine)
print(db0)
# print(db0.xxx)
df = db0.query(db0.TEST.fuck).filter().to_df()
print(df)
print(db0.tables)


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
