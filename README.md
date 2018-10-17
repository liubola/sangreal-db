# sangreal-db
基于sqlalchemy的python数据库orm包，加入对交互式编程的支持，更简易的API。

## 安装

```pip install sangreal-db```

## 使用方法

### 查

```python
from sangreal_db import DataBase
from sqlalchemy import create_engine

engine = create_engine('mysql://....')

# 实例化
db = DataBase(engine, schema=None)

# database下以TABLE_NAME为表名的Table类
table = db.TABLE_NAME

# 表TABLE_NAME下以COLUMN为列名的column类
table.c.COLUMN

# 继承了sqlalchemy的Query，支持同样方法
# 返回json类格式
db.query(db.TABLE_NAME).filter(table.c.COLUMN==....).all() 

# 返回DataFrame
db.query(db.TABLE_NAME).filter(...).to_df()

```

### ipython or jupyter-notebook

实例化Database类后，sangreal-db会自动为该实例添加以表名命名的属性，这点在交互式编程中十分方便。

**需要注意的是**，该属性为懒加载，并不会一次性将database下的所有表映射成Table类，只有在单独调用时才会映射对应的表，解决了性能问题。

![tables](img/tables.png)











