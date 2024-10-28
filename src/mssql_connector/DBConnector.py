import pymssql

def Query(q):
    connection = pymssql.connect("192.168.81.191:49170", "sa", "7ssvwAvKVUYB6", "ADNCube")

    cursor = connection.cursor(as_dict=True)

    cursor.execute(q)

    connection.commit()

    cursor.close()
    connection.close()

def QueryRequestOneColumn(column,table):
    connection = pymssql.connect("192.168.81.191:49170", "sa", "7ssvwAvKVUYB6", "ADNCube")

    cursor = connection.cursor(as_dict=True)

    cursor.execute('SELECT '+str(column)+' FROM '+ str(table))
    resp_list = []
    for row in cursor:
        resp_list.append(row[str(column)])

    connection.close()
    return resp_list

def QueryRequestTableColumns(table):
    connection = pymssql.connect("192.168.81.191:49170", "sa", "7ssvwAvKVUYB6", "ADNCube")

    cursor = connection.cursor(as_dict=True)

    cursor.execute("select COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_SCHEMA = 'dbo' and TABLE_NAME = '"+ str(table)+ "'")
    resp_list = []
    for row in cursor:
        resp_list.append(row['COLUMN_NAME'])

    connection.close()
    return resp_list

