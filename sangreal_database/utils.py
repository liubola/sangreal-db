import os
from configparser import ConfigParser, NoOptionError, NoSectionError

from sqlalchemy import create_engine
from sqlalchemy.engine import reflection

import cx_Oracle

BASE_DIR = os.path.abspath(os.path.expanduser('~/.sangreal'))
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)

config = ConfigParser()
config_path = f"{BASE_DIR}{os.sep}config.ini"
if not os.path.exists(config_path):
    config.add_section('db')
    config.set('db', 'db_type', '')
    config.set('db', 'engine', '')
config.read(config_path)
engine = config.get('db', 'engine')
db_type = config.get('db', 'db_type')
if not engine:
    raise ValueError(f'please add engine under {config_path}.')
if not db_type:
    raise ValueError(f'please add db_type under {db_type}.')
if db_type.lower() == 'oracle':
    ENGINE = cx_Oracle.connect(engine)
else:
    ENGINE = create_engine(engine)
insp = reflection.Inspector.from_engine(ENGINE)
TABLELIST = insp.get_table_names()

if __name__ == '__main__':
    print(ENGINE)
    print(TABLELIST)