"""Database storage system"""
import sqlite3 as sql
import enums
from object import Shape
from os.path import isfile
from resources import res


def _create_database():
    connection = sql.connect(res('sql\\connection'))
    with open(res('sql\\create'), 'r') as script:
        create = script.read().replace('\n', ' ').split(';')
        for table in create:
            connection.execute(table)
    connection.commit()
    connection.close()


def _connect():
    if not isfile(res('sql\\connection')):
        _create_database()
    return sql.connect(res('sql\\connection'))


def insert(obj):
    """Insert object into database"""
    connection = _connect()
    cursor = connection.cursor()
    symbols = []
    for symbol in obj.symbols:
        cursor.execute(res('sql\\insert\\shape'),
                       [None, symbol.type.value, symbol.height.value, symbol.width.value, symbol.color.value])
        symbols.append(cursor.lastrowid)
    cursor.execute(res('sql\\insert\\shape'),
                   [None, obj.type.value, obj.height.value, obj.width.value, obj.color.value])
    shape = cursor.lastrowid
    for symbol in symbols:
        cursor.execute(res('sql\\insert\\symbol'), [shape, symbol])
    cursor.execute(res('sql\\insert\\object'), [None, shape])
    cursor.close()
    connection.commit()
    connection.close()


def select():
    """Retrieve objects from database"""
    connection = _connect()
    cursor = connection.cursor()
    with open(res('sql\\select')) as script:
        script = script.read().replace('\n', ' ').split(';')
        cursor.execute(script[0])
        objects = cursor.fetchall()
        cursor.execute(script[1])
        symbols = cursor.fetchall()
        cursor.close()
        connection.close()
    list = []
    for obj in objects:
        syms = []
        for sym in [s for s in symbols if s[0] == obj[1]]:
            syms.append(Shape(enums.Shape(sym[3]), enums.Size(sym[4]), enums.Size(sym[5]), enums.Color(sym[6])))
        list.append(Shape(enums.Shape(obj[3]), enums.Size(obj[4]), enums.Size(obj[5]), enums.Color(obj[6]), syms, obj[0]))
    return list
