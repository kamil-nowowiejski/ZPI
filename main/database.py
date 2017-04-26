"""Database storage system"""
import sqlite3 as sql
import Object as o
from os.path import isfile
from resources import res
from enum import Enum


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


def _insert(connection, table, *args):
    script = 'INSERT INTO %s VALUES(' % table
    values = [None]
    for arg in args:
        script += '?, '
        values.append(arg)
    script += '?);'
    connection.cursor().execute(script, values)


def insert(obj):
    """Insert object into database"""
    connection = _connect()
    cursor = connection.cursor()
    symbols = []
    for symbol in obj.symbols:
        symbol.type = symbol.type.value
        symbol.color = symbol.type.value
        cursor.execute(res('sql\\insert\\shape'), [None, symbol.type, symbol.height, symbol.width, symbol.color])
        symbols.append(cursor.lastrowid)
    obj.type = obj.type.value
    obj.color = obj.color.value
    cursor.execute(res('sql\\insert\\shape'), [None, obj.type, obj.height, obj.width, obj.color])
    shape = cursor.lastrowid
    for symbol in symbols:
        cursor.execute(res('sql\\insert\\symbol'), [shape, symbol])
    cursor.execute(res('sql\\insert\\object'), [None, shape])
    connection.commit()
    connection.close()


def select(**kwargs):
    """Retrieve objects from database filtered by keyword arguments
    
    examples:
    select()
    select(height=Object.Size.BIG)
    select(width=8)  
    select(color=Object.Color.GREEN, size=Object.Size.SMALL)
    """
    connection = _connect()
    cursor = connection.cursor()
    with open(res('sql\\select')) as script:
        script = script.read().replace('\n', ' ').split(';')
        list = []
        if len(kwargs) > 0:
            for table in script:
                table += ' WHERE '
                for kw in kwargs:
                    if isinstance(kwargs[kw], Enum):
                        table += kw + '=' + str(kwargs[kw].value) + ' AND '
                    else:
                        table += kw + '=' + str(kwargs[kw]) + ' AND '
                table = table[:-5]
                try:
                    cursor.execute(table)
                    list += cursor.fetchall()
                except sql.OperationalError:
                    pass
        else:
            for table in script:
                cursor.execute(table)
                list += cursor.fetchall()
    connection.close()
    for i in range(len(list)):
        if list[i][1] is not None:
            list[i] = o.Cuboid(o.Size(list[i][4]), o.Size(list[i][5]), o.Size(list[i][6]), o.Color(list[i][7]), list[i][0])
        elif list[i][2] is not None:
            list[i] = o.Sphere(o.Size(list[i][4]), o.Color(list[i][5]), list[i][0])
    return list
