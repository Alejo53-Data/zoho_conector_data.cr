import datetime,traceback
from src.mssql_connector.DBConnector import *

def TimeCorrection(dicc,key):
    dicc[key] = str(dicc[key])[:-6].replace("T"," ")
    
def GeneralCreation(resp, table):
    fields = QueryRequestTableColumns(table)

    data = {}
    for k,v in resp.items():
        if k.lower() in fields:
            if v in [False,"false","False"]:
                v = 0
            if v in [True,"true","True"]:
                v = 1
            if v in [None,'']:
                v = 'null'

            data[k.lower()]=v

    for x in data:
        if "time" in x or ("date" in x and len(str(data[x])) > 12):
            TimeCorrection(data,x)

    column=""
    value=""
    
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

    query_sql = "INSERT INTO "+table+" (" + column + ") VALUES (" + value + ");"
    try:
        Query(query_sql)
    except:
        traceback.print_exc()
        print(table)


def GeneralUpdate(resp, table = "crm_accounts"):
    fields = QueryRequestTableColumns(table)
    data = {}
    for k,v in resp.items():
        if k.lower() in fields:
            if v in [False,"false","False"]:
                v = 0
            if v in [True,"true","True"]:
                v = 1
            if v in [None,'']:
                v = 'null'

            data[k.lower()]=v
        
    for x in data:
        if "time" in x or "date" in x:
            TimeCorrection(data,x)

    data_to_set = ""

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
    query_sql = "UPDATE "+table+" SET "+data_to_set+" WHERE id = "+str(data["id"])+";"

    try:
        Query(query_sql)
    except:
        traceback.print_exc()
        print(table)
