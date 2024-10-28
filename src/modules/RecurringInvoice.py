from src.mssql_connector.DBConnector import *
import traceback

def TimeCorrection(dicc,key,let):
    dicc[key] = dicc[key][:let].replace("T"," ")

def InvoiceCreate(data):
    contacts = QueryRequestOneColumn("contact_id","zb_contacts")
    columns = QueryRequestTableColumns("zb_invoice")
    query_data={}
    print()
    for k,v in data.items():
        if k in columns:
            query_data[k] = v
        elif k == "custom_field_hash":
            for k2,v2 in v.items():
                if k2 in columns:
                    query_data[k2] = v2
    
    for k,v in query_data.items():
        if v in [False,"false","False"]:
            query_data[k] = 0
        if v in [True,"true","True"]:
            query_data[k] = 1
        if v in [None,'']:
            query_data[k] = 'null'
        if k == "customer_id" and str(v) not in contacts:
            query_data[k] = 'null' 

    for x in query_data:
        if "time" in x and x !="client_viewed_time" or ("date" in x and len(str(query_data[x])) > 12):
            TimeCorrection(query_data,x,-5)

    for x in query_data:
        if "fecha" in x:
            TimeCorrection(query_data,x,-6)

    column = ''
    value = ''

    for k,v in query_data.items():
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

    query_sql = "INSERT INTO zb_invoice (" + column + ") VALUES (" + value + ");"

    try:
        Query(query_sql)
        return "Registro Creado - Invoice - ID " + query_data["invoice_id"] + "\n"

    except:
        print(query_sql)
        return traceback.format_exc()


def InvoiceUpdate(data):
    columns = QueryRequestTableColumns("zb_invoice")
    query_data={}
    for k,v in data.items():
        if k in columns:
            query_data[k] = v
        elif k == "custom_field_hash":
            for k2,v2 in v.items():
                if k2 in columns:
                    query_data[k2] = v2

    for k,v in query_data.items():
        if v in [False,"false","False"]:
            query_data[k] = 0
        if v in [True,"true","True"]:
            query_data[k] = 1
        if v in [None,'']:
            query_data[k] = 'null'    

    for x in data:
        if "time" in data[x] or "date" in data[x]:
            TimeCorrection(data,x)

    data_to_set =''
    
    for k,v in query_data.items():
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

    query_sql = "UPDATE zb_invoice SET "+data_to_set+" WHERE invoice_id = "+str(query_data["invoice_id"])+";"

    try:
        Query(query_sql)
        return "Registro Actualizado - Invoice - ID " + str(query_data["invoice_id"]) + "\n"

    except:
        return traceback.format_exc()
