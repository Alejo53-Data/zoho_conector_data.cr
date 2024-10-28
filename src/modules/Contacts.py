from src.utils.BooksContacts import BooksContacts
from src.mssql_connector.DBConnector import *
import traceback


def CreateContacts(contact):
    contact_fields = QueryRequestTableColumns("zb_contacts")
    
    data = {}
    for k,v in contact.items():
        if k in contact_fields:
            if v in [False,"false","False"]:
                v = 0
            if v in [True,"true","True"]:
                v = 1
            if v in [None,'']:
                v = 'null'

            data[k]=v

    for k,v in data.items():
        try:
            if "time" in k or "date" in k:
                data[k] = v.replace("T"," ")[:-5]
        except: continue

    column =''
    value =''

    for k,v in data.items():
        column += k + ", "
        try:
            x=int(v)
            if len(str(x))>=38:
                value += "'" + str(v).replace("'","") + "', "
                continue
            value += str(v) + ', '
        except:
            if v == 'null': 
                value += v + ', '
            else:
                value += "'" + str(v).replace("'","") + "', "

    column = column[:-2]
    value = value[:-2]
    query_sql = "INSERT INTO zb_contacts (" + column + ") VALUES (" + value + ");"
    
    try:
        Query(query_sql)
        return "Registro Creado - Contact - ID " + data["contact_id"] + "\n"

    except:
        return traceback.format_exc()


def UpdateContacts(contact_id):
    contacts = BooksContacts()
    contact_fields = QueryRequestTableColumns("zb_contacts")
    
    contact = contacts.get_record(int(contact_id))["contact"]
    data = {}
    for k,v in contact.items():
        if k in contact_fields:
            if v in [False,"false","False"]:
                v = 0
            if v in [True,"true","True"]:
                v = 1
            if v in [None,'']:
                v = 'null'

            data[k]=v

    for k,v in data.items():
        try:
            if "time" in k or "date" in k:
                data[k] = v.replace("T"," ")[:-5]
        except: continue

    data_to_set =''

    for k,v in data.items():
        column = k + "="
        try:
            x=int(v)
            if len(str(x))>=38:
                value += "'" + str(v).replace("'","") + "', "
                data_to_set += column
                continue
            column += str(v) + ', '

        except:
            if v == 'null': 
                column += v + ', '
            else:
                column += "'" + str(v).replace("'","") + "', "

        data_to_set += column
        
    data_to_set = data_to_set[:-2]

    query_sql = "UPDATE zb_contacts SET "+data_to_set+" WHERE contact_id = "+str(contact_id)+";"

    try:
        Query(query_sql)
        return "Registro Actualizado - Contact - ID " + str(data["contact_id"]) + "\n"

    except:
        return traceback.format_exc()
