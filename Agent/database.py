"""Database storage system"""
import sqlite3 as sql
from os.path import isfile

import enums
from object import Shape, CombinedObject
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
    if isinstance(obj, CombinedObject):
        _insert_combined_object(cursor, obj)
    elif isinstance(obj, Shape):
        _insert_basic_object(cursor, obj)

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


def _insert_basic_object(cursor, obj):
    symbols = []
    for symbol in obj.symbols:
        cursor.execute(res('sql\\insert\\shape'),
                       [None, symbol.type.value, symbol.width.value, symbol.height.value, symbol.color.value,
                        symbol.pattern.value, symbol.pattern_color.value])
        symbols.append(cursor.lastrowid)
    cursor.execute(res('sql\\insert\\shape'),
                   [None, obj.type.value, obj.width.value, obj.height.value, obj.color.value, obj.pattern.value,
                    obj.pattern_color.value])
    shape = cursor.lastrowid
    for symbol in symbols:
        cursor.execute(res('sql\\insert\\symbol'), [shape, symbol])
    cursor.execute(res('sql\\insert\\object'), [None, shape, None])
    return shape


def _insert_combined_object(cursor, obj):
    parts = []
    for part in obj.parts:
        part_id = _insert_basic_object(cursor, part)
        parts.append(part_id)

    cursor.execute(res('sql\\insert\\combined_object'),
                   [None, obj.type.value, obj.width.value, obj.height.value])
    combined_id = cursor.lastrowid
    for part_id in parts:
        cursor.execute(res('sql\\insert\\combined_object_parts'),
                       [combined_id, part_id])
    cursor.execute(res('sql\\insert\\object'), [None, None, combined_id])
    return combined_id

