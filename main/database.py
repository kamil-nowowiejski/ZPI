"""Database storage system"""
import sqlite3 as sql
import Object as o
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
    if type(obj) is o.Cuboid:
        with open(res('sql\\insert\\cuboid')) as script:
            commands = script.read().split(';')
            cursor.execute(commands[0], (None, obj.height.value, obj.width.value, obj.depth.value, obj.color.value))
            cursor.execute(commands[1], (None, cursor.lastrowid, None))
    elif type(obj) is o.Sphere:
        with open(res('sql\\insert\\sphere')) as script:
            commands = script.read().split(';')
            cursor.execute(commands[0], (None, obj.size.value, obj.color.value))
            cursor.execute(commands[1], (None, None, cursor.lastrowid))
    connection.commit()
    connection.close()


def select(**kwargs):
    """Retrieve objects from database filtered by keyword arguments"""
    connection = _connect()
    cursor = connection.cursor()
    with open(res('sql\\select')) as script:
        script = script.read().replace('\n', ' ').split(';')
        list = []
        if len(kwargs) > 0:
            for table in script:
                table += 'WHERE '
                for kw in kwargs:
                    table += kw + ' ' + str(kwargs['kw']) + ', '
                table = table[-2:]
                cursor.execute(table)
                list += cursor.fetchall()
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
