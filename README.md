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

# 表TABLE_NAME下以COLUMN为列名的Column类
table.COLUMN

# 继承了sqlalchemy的Query，支持同样方法
# 返回json类格式
db.query(table).filter(table.COLUMN==....).all() 

# 返回DataFrame
db.query(table).filter(...).to_df()

```

### 增/改

```python
# 增
t_obj_add = table(c1=xxx, c2=xxx, c3=xxx)
db.update(t_obj_add)

# 改
t_obj_update = db.query(table).filter(...).all()
for t in t_obj_update:
    t.c1 = xxx
db.update(t_obj_update)

# 或者一起搞
# 构建一个iterable对象
t_change = [t_obj_add] + t_obj_update
db.update(t_change)
```

### 删

```python
# 删
t_obj_delete = db.query(table).filter(...).first()
db.delete(t_obj_delete)
```

___

### ipython or jupyter-notebook

实例化Database类后，sangreal-db会自动为该实例添加以表名命名的属性，这点在交互式编程中十分方便。

**需要注意的是**，该属性为懒加载，并不会一次性将database下的所有表映射成Table类，只有在单独调用时才会映射对应的表，解决了性能问题。

![tables](img/tables.png)











