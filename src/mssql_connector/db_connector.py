import pymssql

def query(q):
    connection = pymssql.connect("192.168.81.191:49170", "sa", "7ssvwAvKVUYB6", "ADNCube")

    cursor = connection.cursor(as_dict=True)

    cursor.execute(q)

    connection.commit()

    cursor.close()
    connection.close()