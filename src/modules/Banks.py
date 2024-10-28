from src.utils.BooksBankAccounts import BooksBankAccounts
from src.mssql_connector.DBConnector import *
import traceback
import time

def CreateBanks(bank):
    bank_fields = QueryRequestTableColumns("zb_banks")
    
    data = {}
    for k,v in bank.items():
        if k in bank_fields:
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
    query_sql = "INSERT INTO zb_banks (" + column + ") VALUES (" + value + ");"
    
    try:
        Query(query_sql)
        return "Registro Creado - Banks - ID " + data["account_id"] + "\n"

    except:
        return traceback.format_exc()


def UpdateBanks(bank_id):
    banks = BooksBankAccounts()
    bank_fields = QueryRequestTableColumns("zb_banks")

    bank = banks.get_record(int(bank_id))
    if bank["message"] == 'success':
         bank = bank["bankaccount"]
    else:
        try:
            time.sleep(45)
            bank = banks.get_record(int(bank_id))["bankaccount"]
        except:
            return "No se pudo conseguir la información"

    data = {}
    for k,v in bank.items():
        if k in bank_fields:
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

    query_sql = "UPDATE zb_banks SET "+data_to_set+" WHERE account_id = "+str(bank_id)+";"

    try:
        Query(query_sql)
        return "Registro Actualizado - Banks - ID " + str(data["account_id"]) + "\n"

    except:
        return traceback.format_exc()

