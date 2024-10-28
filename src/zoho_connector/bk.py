from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.record.body_wrapper import BodyWrapper as BodyWrappers
from zcrmsdk.src.com.zoho.crm.api.users import *
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
from zcrmsdk.src.com.zoho.crm.api import HeaderMap, ParameterMap
from datetime import date, datetime
from zcrmsdk.src.com.zoho.crm.api.record import SuccessResponse,APIException,Record as ZCRMRecord,ActionWrapper as RecordActionWrapper
from zcrmsdk.src.com.zoho.crm.api.users import User
from zcrmsdk.src.com.zoho.crm.api.util import Choice
import random

import os

class ZCRM_Initializer:

    def __init__(self) -> None:        
        main_path = './'
        #main_path = './src/zcrm-connector/'
        log_path = main_path + "logs/sdk_log.log"
        os.system(f'echo > "{log_path}"')
        # Logs path 
        logger = Logger.get_instance(level=Logger.Levels.INFO,
                                    file_path= log_path)
        # Create an UserSignature instance that takes user Email as parameter
        user = UserSignature(email="zohomanager@data.cr")
        # Choice the environment for work
        environment = USDataCenter.PRODUCTION()
        # Token creation
        token = OAuthToken(client_id='1000.ODFVF4TA4TKUU6D0ZFHAXRWK63WTRH', 
                    client_secret='e1128e2f6d734d63b2dc1b758850f401ca087b80cd', 
                    token='1000.7fa0e064f66aa6d4269c697909da9095.0c800966911d44c553ed8de290835adf',
                    #1000.27ad6bdfe37db528a2662ff7c100a264.535e41feff21d7530fcfcfeeccd13b07
                    #
                    token_type=TokenType.REFRESH, 
                    redirect_url="https://www.abc.com")
        # Path for store the tokens
        print(main_path)  
        store = FileStore(main_path + 'logs/token')
        # Configurations
        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)
        # Resources path
        resource_path = main_path
        # Initialize the connection to the API
        Initializer.initialize(user=user, environment=environment, token=token, sdk_config=config, resource_path=resource_path, logger=logger, store=store)
        self.operations = RecordOperations()
        self.user_operations = UsersOperations()

    def get_by_id(self,module='Contacts', id=3413022000124328993):
        req = self.operations.get_record(module_api_name=module, id=id)
        req_object = req.get_object()
        rec_list = req_object.get_data()
        for record in rec_list:
            values = record.get_key_values()
            for k,y in values.items():
                try:
                    y = y.get_key_values()['id']
                except:
                    pass
                try:
                    y = y.get_value()
                except:
                    pass
                try:
                    txt=""
                    for a in y:
                        txt+=str(a.get_value())+", "
                    y = txt[:-2]
                except:
                    pass
                values[k]=y
        return values

    def get_all(self,module_api_name='Sales_Orders'):
        npage = 1
        finish = True
        data = []
        while finish:
            param_instance = ParameterMap()
            param_instance.add(GetRecordsParam.page, npage)
            param_instance.add(GetRecordsParam.per_page, 200)
            header_instance = HeaderMap()
            req = self.operations.get_records(module_api_name,param_instance,header_instance)
            req_object = req.get_object()
            rec_list = req_object.get_data()
            print(len(rec_list))
            for record in rec_list:
                values = record.get_key_values()
                for k,y in values.items():
                    try:
                        y = y.get_key_values()['id']
                    except:
                        pass
                    try:
                        y = y.get_value()
                    except:
                        pass
                    try:
                        txt=""
                        for a in y:
                            txt+=str(a.get_value())+", "
                        y = txt[:-2]
                    except:
                        pass
                    if isinstance(y, datetime) or isinstance(y, date):
                        y=str(y)
                    if "api.layouts" in str(y):
                        y=str(y)
                    if ".tag" in str(y):
                        y=str(y)
                    if ".inventory_line_items" in str(y):
                        try:
                            lines = []
                            for i in y:
                                line = i.get_key_values()
                                line['product'] = line['product'].get_key_values()['id']
                                try:
                                    line['line_tax']  = sum([ x.get_value() for x in line['line_tax'] ])
                                except:
                                    line['line_tax'] = 0
                                lines.append(line)
                        except:
                            lines=[]
                        y=lines                      
                    if ".remind_at" in str(y):
                        y=str(y)       
                    values[k]=y
                data.append(values)
            if len(rec_list) == 200:
                npage+=1
                continue
            else:
                break
        return data
    
    def test(self,module_api_name='Sales_Orders'):
        npage = 1
        finish = True
        data = []
        while finish:
            param_instance = ParameterMap()
            param_instance.add(GetRecordsParam.page, npage)
            param_instance.add(GetRecordsParam.per_page, 200)
            header_instance = HeaderMap()
            req = self.operations.get_records(module_api_name,param_instance,header_instance)
            req_object = req.get_object()
            rec_list = req_object.get_data()
            print(len(rec_list))
            rec_list = [rec_list[0]]
            for record in rec_list:
                values = record.get_key_values()
                for k,y in values.items():
                    try:
                        y = y.get_key_values()['id']
                    except:
                        pass
                    try:
                        y = y.get_value()
                    except:
                        pass
                    try:
                        txt=""
                        for a in y:
                            txt+=str(a.get_value())+", "
                        y = txt[:-2]
                    except:
                        pass
                    if isinstance(y, datetime) or isinstance(y, date):
                        y=str(y)
                    if "api.layouts" in str(y):
                        y=str(y)
                    if ".tag" in str(y):
                        y=str(y)
                    if ".inventory_line_items" in str(y):
                        try:
                            lines = []
                            for i in y:
                                line = i.get_key_values()
                                line['product'] = line['product'].get_key_values()['id']
                                try:
                                    line['line_tax']  = sum([ x.get_value() for x in line['line_tax'] ])
                                except:
                                    line['line_tax'] = 0
                                lines.append(line)
                        except:
                            lines=[]
                        y=lines
                    if ".remind_at" in str(y):
                        y=str(y)       
                    values[k]=y
                data.append(values)
            if len(rec_list) == 200:
                npage+=1
            return 0
        
    def get_search(self,module='Accounts',changes={}):
        param_instance = ParameterMap()
        param_instance.add(SearchRecordsParam.page, 1)
        param_instance.add(SearchRecordsParam.per_page, 20)
        for k,v in changes.items():
            param_instance.add(SearchRecordsParam.criteria, f'({k}:equals:{v})')
            #print(f'({k}:starts_with:{v})')
        header_instance = HeaderMap()
        #print(param_instance)
        response_get = self.operations.search_records(module, param_instance,header_instance)
        print(response_get)
        if response_get is not None:
            
            print(response_get.get_status_code())
            if response_get.get_status_code() in [204, 304]:
                # print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                print( {'message': f'Cannot find content for the zoho account with id: {record_id}', 'code': 404})
                return None
            response_object = response_get.get_object()
            record_list = response_object.get_data()
            if response_object is not None:
                print(response_object.get_data()[0].get_id())
                print(response_object)
                record_list = response_object.get_data()
                record = [record for record in record_list if record.get_key_value('N_mero_Circuito') == record_id]
                record = record[0] if len(record) > 0 else None
                if record != None:
                    _record_id = record.get_id()
                    print(_record_id)


        #req_object = req.get_object()
        #print(req)
        #print(req_object)
        #rec_list = req_object.get_data()[0].get_id()
        return "0"
    def update_record(self,module_api_name,data1):
        request = BodyWrappers()
        # List to hold Record instances
        records_list = []
        # Get instance of Record Class
        record1 = ZCRMRecord()
        # ID of the record to be updated
        user = User()
        record1.add_key_value('id', 3413022000010257684)
        record1.add_key_value('Consecutivo_Principal', data1)
        records_list.append(record1)
        request.set_data(records_list)
        trigger = []
        request.set_trigger(trigger)
        header_instance = HeaderMap()
        response = self.operations.update_records("Config_Consecutivos", request, header_instance)
        print(response)
        return response
    def get_records(self,module='Contacts',dateT='2022-09-26T10:00:00-06:00'):
        npage = 1
        finish = True
        data = []
        while finish:
            param_instance = ParameterMap()
            param_instance.add(GetRecordsParam.page, npage)
            param_instance.add(GetRecordsParam.per_page, 200)
            # Get instance of HeaderMap Class
            header_instance = HeaderMap()
            # Possible headers for Get Records operation
            header_instance.add(GetRecordsHeader.if_modified_since, datetime.fromisoformat(dateT))
            response = self.operations.get_records(module, param_instance, header_instance)
            obj_res = response.get_object().get_data()
            for record in obj_res:
                values = record.get_key_values()
                for k,y in values.items():
                    try:
                        y = y.get_key_values()['id']
                    except:
                        pass
                    try:
                        y = y.get_value()
                    except:
                        pass
                    try:
                        txt=""
                        for a in y:
                            txt+=str(a.get_value())+", "
                        y = txt[:-2]
                    except:
                        pass
                    if isinstance(y, datetime) or isinstance(y, date):
                        y=str(y)
                    if "api.layouts" in str(y):
                        y=str(y)
                    if ".tag" in str(y):
                        y=str(y)
                    if ".inventory_line_items" in str(y):
                        try:
                            lines = []
                            for i in y:
                                line = i.get_key_values()
                                line['product'] = line['product'].get_key_values()['id']
                                try:
                                    line['line_tax']  = sum([ x.get_value() for x in line['line_tax'] ])
                                except:
                                    line['line_tax'] = 0
                                lines.append(line)
                        except:
                            lines=[]
                        y=lines
                    if ".remind_at" in str(y):
                        y=str(y)  
                    values[k]=y
                data.append(values)
            if len(obj_res) == 200:
                npage+=1
                continue
            else:
                break
        return data
    
    def get_user(self):
        npage = 1
        finish = True
        data = []
        while finish:
            param_instance = ParameterMap()
            param_instance.add(GetRecordsParam.page, npage)
            param_instance.add(GetRecordsParam.per_page, 200)
            # Get instance of HeaderMap Class
            header_instance = HeaderMap()
            response = self.user_operations.get_users(param_instance, header_instance)
            response_object = response.get_object()
            #print(response_object.get_message().get_value())
            user_list = response_object.get_users()
            for record in user_list:
                values = record.get_key_values()
                for k,y in values.items():
                    try:
                        y = y.get_key_values()['id']
                    except:
                        pass
                    try:
                        y = y.get_value()
                    except:
                        pass
                    try:
                        txt=""
                        for a in y:
                            txt+=str(a.get_value())+", "
                        y = txt[:-2]
                    except:
                        pass
                    if isinstance(y, datetime) or isinstance(y, date):
                        y=str(y)
                    if ".roles" in str(y):
                        y = y.get_name()
                    if "profiles.profile" in str(y):
                        y=y.get_name()
                    values[k]=y
                data.append(values)
            if len(user_list) == 200:
                npage+=1
                continue
            else:
                break
        return data
    
    def get_deleted_records(self,module='Contacts',dateT='2022-09-26T10:00:00-06:00'): 
        npage = 1
        finish = True
        data = []
        while finish:
            param_instance = ParameterMap()
            param_instance.add(GetDeletedRecordsParam.page, npage)
            param_instance.add(GetDeletedRecordsParam.per_page, 200)
            param_instance.add(GetDeletedRecordsParam.type, 'all')
            # Get instance of HeaderMap Class
            header_instance = HeaderMap()
            # Possible headers for Get Records operation
            header_instance.add(GetDeletedRecordsHeader.if_modified_since, datetime.fromisoformat(dateT))
            response = self.operations.get_deleted_records(module, param_instance, header_instance)
            obj_res = response.get_object().get_data()
            for record in obj_res:
                values = str(record.get_id())
                data.append(values)
            if len(obj_res) == 200:
                npage+=1
                continue
            else:
                break
        return data
    
    def mass_update(self,vent,ids):
        # Get instance of RecordOperations Class
        record_operations = self.operations
        # Get instance of MassUpdateBodyWrapper Class that will contain the request body
        request = MassUpdateBodyWrapper()
        # List to hold Record instances
        records_list = []
        # Get instance of Record Class
        record = ZCRMRecord()
        user = User()
        user.add_key_value('id', int(vent))
        user.add_key_value('Full_Name', "Alberth Astua")
        record.add_key_value('Ejecutivo_Asignado', user)
        #record.add_key_value('Ejecutivo_Asignado', vent)
        # Add the record instance to list
        records_list.append(record)
        # Set the array to data in MassUpdateBodyWrapper instance
        request.set_data(records_list)
        # Set the array of IDs to MassUpdateBodyWrapper instance
        request.set_ids(ids)
        # Set the value to over write
        request.set_over_write(True)
        # Call mass_update_records method that takes MassUpdateBodyWrapper instance, module_api_name as parameter.
        response = record_operations.mass_update_records("Accounts", request)
         
    def addField(field,value):
        if value != None:
            record.add_key_value(field, value)

    def create_record(self,module,data):
          def addField(field,value):
            if value != None:
                record.add_key_value(field, value)
                try:
                    #modulo= self.operations.create_records("")
                    #module = ZCRMModule.get_instance('Accounts')
                    record = ZCRMRecord("Accounts")
                    record.add_field_value(Field.Leads.company(), data["name"])
                    addField('Email', data["email_from"])
                    #record.add_key_value('Coordenadas_GPS', "9.4,-10.58")
                    record.add_key_value('Zona_Cobertura', Choice(data["x_studio_fiber_footprint"]))
                    addField('Description', data["description"])
                    #record.add_key_value('First_Name', "Marco")
                    addField('Last_Name', data["name"])
                    addField('Full_Name', data["contact_name"])
                    addField('Phone', data["phone"])
                    record.add_key_value('Tipo_de_Prospecto', Choice('Cuenta Empresarial'))
                    record.add_key_value('Provincia', Choice(data["state_id"]))
                    addField('Mobile', data["mobile"])
                    record.add_key_value('Segmento', Choice('B2B'))
                    addField('Direcci_n_Exacta', data["street"])
                    record.add_key_value('Industry', Choice(data["x_studio_industry"]))
                    record.add_key_value('Lead_Agent', Choice(data["x_studio_lead_agent"]))
                    record.add_key_value('Lead_Status', Choice('Pendiente Contactar'))
                    record.add_key_value('Odoo_Sync', True)
                    record.add_key_value('From_Odoo', True)
                    record.add_key_value('Lead_Source', Choice('Lead Center'))
                    user = User()
                    user.add_key_value('id', int(data["user_id"]["x_studio_zoho_id_1"]))
                    user.add_key_value('Full_Name', data["name"])
                    record.add_key_value('Owner', user)
                            
                    # Add Record instance to the list
                    records_list.append(record)
                    
                    # Set the list to data in BodyWrapper instance
                    request.set_data(records_list)

                    # Call create_records method that takes BodyWrapper instance and module_api_name as parameters
                    response = operation.create_records("Leads", request)

                    account.set_field_value('Nombre_de_cuenta', 'Mi_nueva_cuenta')
                    account.set_field_value('Industria', 'Servicios')
                    account.set_field_value('Tipo_de_cuenta', 'Cliente potencial')
                    response = account.create()
                    print(response)
                except Exception as e:
                    print(e)

    def get_zoho_record(self,module,record_id):

        """
        This method is used to update a single record of a module with ID and print the response.
        :param module_api_name: The API Name of the record's module.
        :param record_id: The ID of the record to be updated
        """
        module_api_name = module
        if record_id != None:
            # Get instance of RecordOperations Class
            record_operations = RecordOperations()

            # Get instance of ParameterMap Class
            param_instance = ParameterMap()
            # Possible parameters for Search Records operation
            param_instance.add(SearchRecordsParam.page, 1)
            param_instance.add(SearchRecordsParam.per_page, 5)


            _query = f'((Cedula_Jurida_Persona:equals:{record_id}))'
            param_instance.add(SearchRecordsParam.criteria,_query)

            header_instance = HeaderMap()

            # Call getRecord method that takes BodyWrapper instance, module_api_name and record_id as parameter.
            response_get = record_operations.search_records(module_api_name, param_instance, header_instance)
            
            NewZohoCustomerStruct =  {}


            ## FOR GET RECORD INFO METHOD
            if response_get is not None:

                # Get the status code from response
                # print('Status Code: ' + str(response.get_status_code()))
                if response_get.get_status_code() in [204, 304]:
                    # print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                    print( {'message': f'Cannot find content for the zoho888 account with id: {record_id}', 'code': 404})
                    return None
                # Get object from response
                response_object = response_get.get_object()

                if response_object is not None:

                    # Check if expected ResponseWrapper instance is received.
                    if isinstance(response_object, ResponseWrapper):
                        # Get the list of obtained Record instances
                        record_list = response_object.get_data()
                        record = [record for record in record_list if record.get_key_value('Cedula_Jurida_Persona') == record_id]
                        record = record[0] if len(record) > 0 else None
                        if record != None:
                            _record_id = record.get_id()
                            try:
                                NewZohoCustomerStruct = {
                                'CircuitNumber': record.get_key_value('N_mero_Circuito'),
                                'Name': record.get_key_value('Account_Name'),
                                'IDCard': record.get_key_value('Cedula_Jurida_Persona'),
                                'ZohoID': _record_id,
                                'Segmento': record.get_key_value('Segmento_Cuenta').get_value(),
                                'URL': f"https://crm.zoho.com/crm/org680056826/tab/Accounts/{_record_id}",
                                }
                            except Exception as err:
                                NewZohoCustomerStruct = {
                                    'CircuitNumber': record.get_key_value('N_mero_Circuito'),
                                    'Name': record.get_key_value('Account_Name'),
                                    'IDCard': record.get_key_value('Cedula_Jurida_Persona'),
                                    'ZohoID': _record_id,
                                    'Segmento': "",
                                    'URL': f"https://crm.zoho.com/crm/org680056826/tab/Accounts/{_record_id}",
                                }
                            return NewZohoCustomerStruct
                        return None
                    # Check if the request returned an exception
                    elif isinstance(response_object, APIException):      
                        print("Message: " + response_object.get_message().get_value())
                        return None
            return None
        else:
            return None

        #ids= [3413022000003184353,3413022000034981231,3413022000022778022,3413022000033734551,3413022000033734772,3413022000070906141,3413022000035231021,3413022000002032714,3413022000112681937,3413022000112681984,3413022000112735300,3413022000112727499,3413022000071888827,3413022000007034292,3413022000005023744,3413022000100396204,3413022000048579118,3413022000027079011,3413022000075122001,3413022000101989861,3413022000118423107,3413022000050854345,3413022000045669081,3413022000002000955,3413022000011870584,3413022000002033637,3413022000023699367,3413022000031052146,3413022000050435210,3413022000002021078,3413022000001995878,3413022000036935030,3413022000053073599,3413022000045641097,3413022000021092015,3413022000071603021,3413022000085162215,3413022000046653062,3413022000044325529,3413022000002043366,3413022000007328343,3413022000058906392,3413022000103137420,3413022000081573651,3413022000015154217,3413022000063543272,3413022000003935015,3413022000011281769,3413022000002044507,3413022000036955710,3413022000002033598,3413022000001995475,3413022000002033228,3413022000121537913,3413022000063321003,3413022000027929097,3413022000029992106,3413022000029992303,3413022000001995898,3413022000002023952,3413022000002032699,3413022000002032698,3413022000109189194,3413022000034423462,3413022000015088022,3413022000096195219,3413022000005853136,3413022000002044186,3413022000001995487,3413022000098698538,3413022000115699270,3413022000003600095,3413022000083085253,3413022000002043302,3413022000002043301,3413022000002022756,3413022000085140065,3413022000041014086,3413022000002000202,3413022000002033485,3413022000078772297,3413022000077344048,3413022000072243001,3413022000052108213,3413022000013308063,3413022000002044568,3413022000014186159,3413022000034198016,3413022000076085555,3413022000027403025,3413022000120760026,3413022000063847024,3413022000042425159,3413022000007516118,3413022000008587100,3413022000002033565,3413022000028325533,3413022000002023566,3413022000008944213,3413022000052388738,3413022000022166470,3413022000090729818,3413022000002032721,3413022000005153328,3413022000058856384,3413022000044666127,3413022000037720104,3413022000034238022,3413022000002000963,3413022000002000926,3413022000002043256,3413022000012992210,3413022000052356267,3413022000002044989,3413022000002044990,3413022000002020092,3413022000032917458,3413022000081967004,3413022000002022618,3413022000052362151,3413022000002033187,3413022000008284117,3413022000027079318,3413022000026817228,3413022000002033475,3413022000002033477,3413022000037660312,3413022000001995537,3413022000081030048,3413022000030520016,3413022000102788445,3413022000002000668,3413022000109011001,3413022000024826135,3413022000099338700,3413022000001993706,3413022000107898818,3413022000070937563,3413022000001995587,3413022000001995553,3413022000008034132,3413022000058692276,3413022000003957748,3413022000021608022,3413022000058143313,3413022000049254737,3413022000028716061,3413022000048144310,3413022000002033123,3413022000080229077,3413022000004364213,3413022000002043704,3413022000068900625,3413022000054530337,3413022000027145433,3413022000071108517,3413022000081159289,3413022000033586131,3413022000013126017,3413022000048371904,3413022000077042312,3413022000021846025,3413022000002033142,3413022000078246975,3413022000057536604,3413022000073543232,3413022000002044959,3413022000002023825,3413022000001992914,3413022000005750250,3413022000052867001,3413022000032375002,3413022000036893740,3413022000115967590,3413022000015940173,3413022000003689014,3413022000010201592,3413022000001995504,3413022000097996973,3413022000060871087,3413022000063531739,3413022000002023922,3413022000002023921,3413022000002023872,3413022000077751416,3413022000002032331,3413022000002022332,3413022000024166067,3413022000002000193,3413022000002044121,3413022000039949507,3413022000024382206,3413022000034585403,3413022000024996009,3413022000055970027]

    def create_cconsecutivo(self,data):
        self.operation = RecordOperations()
        
        records_list = []
        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)


        e=self.get_by_id("Config_Consecutivos",3413022000010257684)
        consecutivo=e.get("Consecutivo_Principal") +1
        
        circuitl="DAT-"+ str(consecutivo) + "-001"
        print("Dat consecutivo", circuitl)

        request = BodyWrappers()
        addField('Name', circuitl)
        acc = ZCRMRecord()
        print(consecutivo)
        acc.add_field_value(Field.Accounts.id(), int(data))
        addField('Cuenta',acc)
        addField('Consecutivo_Principal', consecutivo)
        addField('Consecutivo_Sucursal', 0)

        print("Testst")
        request2 = BodyWrappers()
        record1 = ZCRMRecord()
        record1.add_key_value('Consecutivo_Principal',int(consecutivo))
        arr =[]
        arr.append(record1)
        request2.set_data(arr)
        #Se actualiza el consecutivo
        records_list.append(record)
        request.set_data(records_list)
        self.operation.update_record(3413022000010257684,"Config_Consecutivos",request2)
        try:
            response = self.operation.create_records("Config_Consecutivos", request)
            if response is not None:
                print("E1")
                response_object = response.get_object()
                print(response_object.get_data())
                if response_object is not None:
                    print("E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("E3")                        
                        action_response_list = response_object.get_data()
                        print(action_response_list)
                        action_response_list
                        for action_response in action_response_list:

                            # Check if the request is successful
                            if isinstance(action_response, SuccessResponse):
                                # Get the details dict
                                zoho_id = action_response.get_details()["id"]
                                print(zoho_id)
                                print("Consecutivo Generated")
                                print("Consecutivo: " + circuitl)
                                return circuitl
                            elif isinstance(action_response, APIException):
                                print(action_response.get_message())
                                print(action_response.get_code())
                                print(action_response.get_status())
                                print(action_response.get_details())
                                print("Eerrorrr 2" )
                                pass

                        # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        print(APIException.get_code())
                        print(APIException.get_message())
                        print(APIException.get_status())
                        print("Eerrorrr")
        except Exception as e:
            print(e)

    def create_record_account(self,data):

        self.operation = RecordOperations()

        records_list = []

        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)


        if data.get('id_type') in 'Cédula Jurídica':
            id_type='Cédula Jurídica'
        elif data.get('id_type') in 'Cedula Fisica': 
            id_type='Cédula Física'
        else:
            id_type='DIMEX'

        request = BodyWrappers()
        addField('Account_Name', data.get('name'))
        addField('Segmento_Cuenta',Choice('B2C'))
        addField('Estado', Choice('Cierre Venta'))
        addField('Fuente_de_Ingreso', Choice('Pagina Web'))
        addField('Referencia', Choice('ADN Pay'))
        addField('Industry',Choice('Condominios'))
        addField('Account_Type', Choice('Cuenta B2C'))
        addField('Estrategia_Segmento', Choice('Standar'))
        addField('Ownership', Choice('American Data Networks'))
        addField('Tipo', Choice('Servicio Único'))
        addField('Cargo_Autom_tico', Choice('NO'))
        addField('Tipo_Fiscal', Choice(id_type))
        addField('Zona_Cobertura', Choice('Dentro Zona Cobertura'))
        addField('Provincia', Choice(data.get("province")))
        addField('Cant_n', Choice(data.get("canton")))
        addField('Distritos', Choice(data.get('district')))
        addField('Direcci_n_Exacta',data.get("address"))
        addField('Raz_n_Social', data.get('name'))
        addField('Identifiacion_2', data.get('id'))
        addField('Segmentacion_Residencial', Choice(''))
        addField('Pago_realizado', True)
        circuit = data.get("circuito")
        ci=data.get('id')
        posicion_insercion = len(ci) // 2
        idcon=data.get("condominium")
        if data.get('ftth') is not None:
            if  'ftth' in  data.get('ftth'): 
                namem="FTTHs"
                nameaccm="ftth"
            else :
                namem="Condominios"
                nameaccm="Condominio_C"
        else:
            namem="Condominios"
            nameaccm="Condominio_C"
  
        print(namem)
        print(namem)
        conobj=self.get_by_id(namem,int(idcon))
        coord=conobj.get('Coordenadas')
        print("Conobj: ", conobj)
        idcondm=conobj.get('id')
        addField('Coordenadas', coord)
        data['coorda']=coord
        addField('N_mero_Circuito', circuit)
        condm = ZCRMRecord()
        condm.set_id(idcondm)
        record.add_key_value(nameaccm, condm)

        cadena_con_guion = ci[:posicion_insercion] + "." + ci[posicion_insercion:]
        print("Cadena ", cadena_con_guion)
        addField('Cedula_Jurida_Persona', data.get('id'))
        user = User()
        if len(data.get('promcode')) < 10:
            user.add_key_value('id', 3413022000025351001)
        else :
            user.add_key_value('id', int(data.get('promcode')))

        addField('Owner', user)
       
        records_list.append(record)
        request.set_data(records_list)
        
      
        try:
            response = self.operation.create_records("Accounts", request)
            if response is not None:
                print("E1")
                response_object = response.get_object()
                print(response_object.get_data())
                if response_object is not None:
                    print("E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("E3")
                        
                        action_response_list = response_object.get_data()
                        print(action_response_list)
                        action_response_list
                        for action_response in action_response_list:

                            # Check if the request is successful
                            if isinstance(action_response, SuccessResponse):
                                # Get the details dict
                                
                                
                                zoho_id = action_response.get_details()["id"]
                                print(zoho_id)
                                print("zoho_id cuenta")
                                dat=self.create_cconsecutivo(zoho_id)
                                addField('N_mero_Circuito',dat)
                                data['idacc']=zoho_id
                                print("ZID: ", zoho_id)
                                print("DAT: ", dat)
                                iptv = data['extra_iptv']
                                if(iptv > 0):
                                    data['iptv'] = True
                                else:
                                    data['iptv'] = False
                                request1 = BodyWrappers()
                                record1 = ZCRMRecord()
                                record1.add_key_value('N_mero_Circuito', str(dat))
                                arr1 =[]
                                arr1.append(record1)
                                request1.set_data(arr1)
                                var1 = self.operations.update_record(zoho_id, "Accounts", request1)
                                idcont=self.create_record_contacts(data)
                                
                                #Para asignar a contratos,
                                data['namem']=namem
                                data['nameaccm']=nameaccm
                                data['idcontact']=idcont


                            #if "ftth" not in data.get('ftth'):
                                self.create_record_contract(data)
                                
                                idtask=self.create_account_task(data)
                                data['idtask']=idtask

                            elif isinstance(action_response, APIException):
                                print(action_response.get_message())
                                print(action_response.get_code())
                                print(action_response.get_status())
                                print(action_response.get_details())
                                print("Eerrorrr 22" )
                                pass

                        # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        print(APIException.get_code())
                        print(APIException.get_message())
                        print(APIException.get_status())
                        print("Eerrorrr")
        except Exception as e:
            print("Json Error")

            print(e)
        
        return data
        

    def create_record_contract(self,data):
        print(data)
        records_list = []
        #Fecha Firma
        date_object=date.today()
        meses = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre"
        }

        self.operation = RecordOperations()
        record = ZCRMRecord()
        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)
        
        if data.get('id_type') in 'Cédula Jurídica':
            id_type='Cédula Jurídica'
        elif data.get('id_type') in 'Cedula Fisica': 
            id_type='Cédula Física'
        else:
            id_type='DIMEX'

        #namem="FTTHs"
        #nameaccm="ftth"
        #data['namem']=namem
        #data['nameaccm']=nameaccm
        request = BodyWrappers()
        addField('Tipo_Fiscal', Choice(id_type))
        addField('Status',Choice('Fase 2'))
        addField('Tipo_de_Contrato', Choice('Contrato Nuevo'))
        random_name = random.randint(10000, 99999)
        addField('Subject', str(random_name))
        idf={}
        addField('Segmento', Choice('B2C'))
        contact_name = ZCRMRecord()
        contact_name.add_field_value(Field.Contacts.id(), int(data.get('idcontact')))
        #contact_name.add_field_value(Field.Contacts.id(), int(3413022000266266241))
        record.add_field_value(Field.Sales_Orders.contact_name(), contact_name)
        user = User()
        
        user = User()
        if len(data.get('promcode')) <10:
            user.add_key_value('id', 3413022000025351001)
            record.add_key_value('Modo_de_Pago', Choice('Deposito'))

        else :
            user.add_key_value('id', int(data.get('promcode')))
            modo = "Deposito" if data['pay_type'] == "Depósito" else data['pay_type']
            print(modo)
            record.add_key_value('Modo_de_Pago', Choice(modo))

        addField('Owner', user)
        #user

        cont = ZCRMRecord()
        cont.add_field_value(Field.Contacts.id(), int(data.get("idcont")))
        #cont.add_field_value(Field.Contacts.id(), int(3413022000266266241))
        acc = ZCRMRecord()
        acc.add_field_value(Field.Accounts.id(), int(data.get("idacc")))
        #acc.add_field_value(Field.Accounts.id(), int(3413022000266241008))
        record.add_field_value(Field.Sales_Orders.account_name(), acc)
        #Contact_Name.
        date_object=date.today()
        print(date_object)
        ar=[]
        ar.append(Choice('Fibra Óptica'))
        ar1=[]
        ar1.append(Choice('Contrato Nuevo Servicio'))
        addField('Contacto_T_cnico_a', data.get('name'))
        record.add_key_value('Contacto_Facturaci_n', cont)
        addField('Numero_Telefonico', data.get('phone'))
        drop=round(float(data.get('drop'))*float(data.get('exchange_rate')),0)
        addField('Drop_Cliente',drop)
        addField('Costo_Recurrente_ADN', 0.0)
        addField('Costo_Instalacion', 0.0)
        addField('Fecha_Proyeccion_Venta', date_object)
        circuit = data.get("circuito")
        #circuit = "DAT-8369-001"
        
        coord=data.get("coorda")
        idcon=data.get("condominium")
        #idcon=3413022000228433373
        
        conobj=self.get_by_id(data.get("namem"),int(idcon))
        plan=data.get("plan")
        coord=conobj.get('Coordenadas')
        idcondm=conobj.get('id')
        addField('N_mero_Circuito', circuit)
        addField('Coordenadas_Actuales', coord)
        condm = ZCRMRecord()
        condm.set_id(idcondm)
        record.add_key_value(data.get("nameaccm"), condm)
        upload = data.get('upload')
        download = data.get('download')
        addField('C_dula_Contrato_Sucursal', data.get('id'))
        addField('Plataforma_Actual', ar)
        addField('Capacidad_Mbps_Carga', int(upload))
        addField('Capacidad_Mbps_Descarga', int(download))
        addField('Relaci_n', Choice('01:01'))
        addField('Pais', Choice('COSTA RICA'))
        addField('Provincia', Choice(data.get("province")))
        addField('Cant_n', Choice(data.get("canton")))
        addField('Distrito', data.get('district'))
        addField('Districts1', Choice(data.get('district')))
        addField('Direcci_n_Exacta',data.get("address"))
        addField('Tipo', ar1)
        addField('Mensualidad1', data.get('tax_free_price'))
        addField('Revision_1', True)
        addField('Revision_2', True)
        addField('borrador', True)
        addField('ADNPAY', True)
        addField('IPTV', data.get('iptv'))
        addField('Pago_Realizado', True)
        record.add_key_value('Fecha_de_Firma', date_object)
        record.add_key_value('Prorrateo', Choice('No'))
        record.add_key_value('Meses_de_Plazo_Contrato', 0)
        newprice = data.get('tax_free_price')
        print("Public ip")
        print(data['public_ip'])

        promou = 0 if data['promotion'] is None else data['promotion']
        if promou == '1' or promou==1:
            print("promoci[on]")
            record.add_key_value('Aplica_Promoci_n',True)
            record.add_key_value('Promoci_n', Choice(data["promotion_type"]))
            if data["promotion_type"] == 'Tercer Mes Gratis':
                if  data['promotion_date'] is not None:
                    # Extraer la parte de la cadena que representa la fecha
                    fecha_dt = data['promotion_date']

                    # Convertir la cadena de fecha a un objeto datetime.date
                    mes_numero = fecha_dt.month

                    inventory_line_item_list = []
                    mes_letra = meses[mes_numero]
                    record.add_key_value('Mes_que_aplica_la_promoci_n', Choice(mes_letra))
            
        inventory_line_item_list = []

        inventory_line_item = InventoryLineItems()
        line_item_product = LineItemProduct()
        a = data.get('idpro')
        line_item_product.set_id(int(a))
        inventory_line_item.set_product(line_item_product)
        inventory_line_item.set_quantity(1.0)
        inventory_line_item.set_product_description(data.get('description'))
        inventory_line_item.set_list_price(data.get('tax_free_price'))
        inventory_line_item.set_discount('0')
        product_line_taxes = []
        inventory_line_item_list.append(inventory_line_item)
        record.add_key_value('Product_Details', inventory_line_item_list)
        
        if(data.get('iptv') == True):
            newprice = data.get('tax_free_price') + (float(data.get('extra_iptv')*1400.0))
            iptv_line_item = InventoryLineItems()
            iptv_item_product = LineItemProduct()
            idproducto = 3413022000079848076
            iptv_item_product.set_id(idproducto)
            iptv_line_item.set_product(iptv_item_product)
            iptv_line_item.set_quantity(float(data.get('extra_iptv')))
            iptv_line_item.set_product_description('Servicio IPTV Adicional B2C')
            iptv_line_item.set_list_price(1400.0)
            iptv_line_item.set_discount('0')
            inventory_line_item_list.append(iptv_line_item)
            record.add_key_value('Product_Details', inventory_line_item_list)
        
        if(data.get('public_ip') == True or data['public_ip']==1 or data['public_ip']=='1' or data['public_ip'] ):
            
            iptv_line_item = InventoryLineItems()
            iptv_item_product = LineItemProduct()
            idproducto = 3413022000139385001
            iptv_item_product.set_id(idproducto)
            iptv_line_item.set_product(iptv_item_product)
            iptv_line_item.set_quantity(float(1))
            iptv_line_item.set_product_description('Servicio IP Publica')
            iptv_line_item.set_list_price(float(0))
            iptv_line_item.set_discount('0')
            inventory_line_item_list.append(iptv_line_item)
            record.add_key_value('Product_Details', inventory_line_item_list)


        if(data.get('public_ip_cus') == True):
            newprice +=  ((11500))
            iptv_line_item = InventoryLineItems()
            iptv_item_product = LineItemProduct()
            idproducto = 3413022000139385001
            iptv_item_product.set_id(idproducto)
            iptv_line_item.set_product(iptv_item_product)
            iptv_line_item.set_quantity(float(1))
            iptv_line_item.set_product_description('Servicio IP Publica Adicional')
            iptv_line_item.set_list_price(float(11500))
            iptv_line_item.set_discount('0')
            inventory_line_item_list.append(iptv_line_item)
            record.add_key_value('Product_Details', inventory_line_item_list)
        

            
        addField('Revenue', newprice)
        addField('Mensualidad1', newprice)
        j={}
        records_list.append(record)
        print("Record List: ", records_list)
        request.set_data(records_list)

        header_instance = HeaderMap()
       

        try:
            response = self.operation.create_records("Sales_Orders",request)
            if response is not None:
                print("E1")
                response_object = response.get_object()
                print("request: ", response_object)
                print(response_object.get_data())
                if response_object is not None:
                    print("E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("E3")
                        
                        action_response_list = response_object.get_data()
                        print(action_response_list)
                        action_response_list
                        for action_response in action_response_list:

                            # Check if the request is successful
                            if isinstance(action_response, SuccessResponse):
                                # Get the details dict
                                zoho_id = action_response.get_details()["id"]
                                data['idcontract']=zoho_id
                                print(zoho_id)
                                print("zoho_id CONTRACTT")
                                return zoho_id
                            elif isinstance(action_response, APIException):
                                print(action_response.get_message)
                                print(action_response.get_code())
                                print(action_response.get_status())
                                print(action_response.get_details())
                                print("Eerrorrr 2" )
                                pass

                        # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        print(APIException.get_code())
                        print(APIException.get_message())
                        print(APIException.get_status())
                        print("Eerrorrr")
        except Exception as e:
            print(e)

    def  create_record_contacts(self,data):
        self.operation = RecordOperations()
        records_list = []

        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)
        # // Factibilidad Deal_Name 3413022000187076509

        palabras = data.get("name").split()
        lastname = " ".join(palabras[-2:])
        name=palabras[0]

        request = BodyWrappers()
        addField('Tipo_de_Contacto', Choice('Contacto Contrato'))
        addField('First_Name',name)
        addField('Last_Name', lastname)
        addField('Email', data.get("email"))
        addField('Profesi_n_Ocupaci_n', ('Contrato Nuevo'))
        addField('Estado_Civil', Choice('Soltero (a)'))
        addField('N_mero_Cedula_Pasaporte', data.get('id'))

        addField('Phone', data.get("phone"))
        addField('Mobile', data.get("phone"))

        addField('Pais', Choice('COSTA RICA'))
        addField('Provincia', Choice(data.get("province")))
        addField('Cant_n', Choice(data.get("canton")))
        addField('Direcci_n_Exacta',data.get("district"))
        acc = ZCRMRecord()
        acc.add_field_value(Field.Accounts.id(), int(data.get("idacc")))
        addField('Account_Name', acc)

        user = User()
        if len(data.get('promcode')) <10:
            user.add_key_value('id', 3413022000025351001)
        else :
            user.add_key_value('id', int(data.get('promcode')))

        addField('Owner', user)
    
        records_list.append(record)
        print(records_list)
        print("Record: ", record)
        request.set_data(records_list)
        response = self.operation.create_records("Contacts", request)

        try:
            if response is not None:
                print("E1")
                response_object = response.get_object()
                print(response_object.get_data())
                if response_object is not None:
                    print("E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("E3")
                        
                        action_response_list = response_object.get_data()
                        print(action_response_list)
                        action_response_list
                        for action_response in action_response_list:

                            # Check if the request is successful
                            if isinstance(action_response, SuccessResponse):
                                # Get the details dict
                                zoho_id = action_response.get_details()['id']
                                data['idcont']=zoho_id
                                print(zoho_id)
                                print("zoho_id Contact")
                                return zoho_id
                            elif isinstance(action_response, APIException):
                                print(action_response.get_message)
                                print(action_response.get_code())
                                print(action_response.get_status())
                                print(action_response.get_details)
                                print("Eerrorrr 2" )
                                pass

                        # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        print(APIException.get_code())
                        print(APIException.get_message())
                        print(APIException.get_status())
                        print("Eerrorrr")
        except Exception as e:
            print(e)

    def  create_record_contacts(self,data):
        self.operation = RecordOperations()
        records_list = []

        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)
        # // Factibilidad Deal_Name 3413022000187076509

        palabras = data.get("name").split()
        lastname = " ".join(palabras[-2:])
        name=palabras[0]

        request = BodyWrappers()
        addField('Tipo_de_Contacto', Choice('Contacto Contrato'))
        addField('First_Name',name)
        addField('Last_Name', lastname)
        addField('Email', data.get("email"))
        addField('Profesi_n_Ocupaci_n', ('Contrato Nuevo'))
        addField('Estado_Civil', Choice('Soltero (a)'))
        addField('N_mero_Cedula_Pasaporte', data.get('id'))

        addField('Phone', data.get("phone"))
        addField('Mobile', data.get("phone"))

        addField('Pais', Choice('COSTA RICA'))
        addField('Provincia', Choice(data.get("province")))
        addField('Cant_n', Choice(data.get("canton")))
        addField('Direcci_n_Exacta',data.get("district"))
        acc = ZCRMRecord()
        acc.add_field_value(Field.Accounts.id(), int(data.get("idacc")))
        addField('Account_Name', acc)

        user = User()
        if len(data.get('promcode')) <10:
            user.add_key_value('id', 3413022000025351001)
        else :
            user.add_key_value('id', int(data.get('promcode')))

        addField('Owner', user)
    
        records_list.append(record)
        print(records_list)
        print("Record: ", record)
        request.set_data(records_list)
        response = self.operation.create_records("Contacts", request)

        try:
            if response is not None:
                print("E1")
                response_object = response.get_object()
                print(response_object.get_data())
                if response_object is not None:
                    print("E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("E3")
                        
                        action_response_list = response_object.get_data()
                        print(action_response_list)
                        action_response_list
                        for action_response in action_response_list:

                            # Check if the request is successful
                            if isinstance(action_response, SuccessResponse):
                                # Get the details dict
                                zoho_id = action_response.get_details()['id']
                                data['idcont']=zoho_id
                                print(zoho_id)
                                print("zoho_id Contact")
                                return zoho_id
                            elif isinstance(action_response, APIException):
                                print(action_response.get_message)
                                print(action_response.get_code())
                                print(action_response.get_status())
                                print(action_response.get_details)
                                print("Eerrorrr 2" )
                                pass

                        # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        print(APIException.get_code())
                        print(APIException.get_message())
                        print(APIException.get_status())
                        print("Eerrorrr")
        except Exception as e:
            print(e)

    def create_record_lead(self,data):      
        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)

        palabras = data.get("name").split()
        lastname = " ".join(palabras[-2:])
        name=palabras[0]
        
        record = ZCRMRecord() 
        self.operation = RecordOperations()
        records_list = []
        user = User()
        request = BodyWrappers()
        print("aquiii")
        record.add_field_value(Field.Leads.company(), data["name"])
        user = User()
        if len(data.get('promcode')) <10:
            user.add_key_value('id', 3413022000025351001)
           
            
        else :
            user.add_key_value('id', int(data.get('promcode')))


        addField('Owner', user)
        addField('Email', data["email"])
        addField('Phone', data["phone"])
        

        record.add_key_value('Zona_Cobertura', Choice(''))
        record.add_key_value('Tipo_de_Prospecto', Choice('Cuenta B2C'))
        record.add_key_value('Lead_Source', Choice('ADNPay'))
        record.add_key_value('Industry', Choice('Condominios'))
        record.add_key_value('Referencia', Choice('ADNPay'))
        record.add_key_value('Provincia', Choice(data["province"]))
        record.add_key_value('Cant_n', Choice(data["canton"]))
        record.add_key_value('Distritos', Choice(data["district"]))
        record.add_key_value('Direcci_n_Exacta', data["address"])
        record.add_key_value('Coordenadas_GPS', "0,-0")
        record.add_key_value('Segmento', Choice('B2C'))
        record.add_key_value('Lead_Status', Choice('Pendiente Contactar'))
        record.add_key_value('Company',data["name"])
        record.add_key_value('First_Name', name)
        record.add_key_value('Last_Name', lastname)
        record.add_key_value('Mobile', data["phone"])

     
        # Add Record instance to the list
        records_list.append(record)
        
        # Set the list to data in BodyWrapper instance
        request.set_data(records_list)

        # Call create_records method that takes BodyWrapper instance and module_api_name as parameters
        
        try:
            response = self.operation.create_records("Leads", request)
            print("Response: ", response)
            if response is not None:
                print("E1")
                response_object = response.get_object()
                print(response_object.get_data())
                if response_object is not None:
                    print("E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("E3")
                        
                        action_response_list = response_object.get_data()
                        print(action_response_list)
                        action_response_list
                        for action_response in action_response_list:

                            # Check if the request is successful
                            if isinstance(action_response, SuccessResponse):
                                # Get the details dict
                                zoho_id = action_response.get_details()["id"]
                                print(zoho_id)
                                print("zoho_id lead")
                                print("ZID: ", zoho_id)
                                data['idlead']=zoho_id
                                self.create_lead_task(data)
                            elif isinstance(action_response, APIException):
                                print(action_response.get_message())
                                print(action_response.get_code())
                                print(action_response.get_status())
                                print(action_response.get_details())
                                print("Eerrorrr 2" )
                                pass

                        # Check if the request returned an exception
                    elif isinstance(response_object, APIException):
                        print(APIException.get_code())
                        print(APIException.get_message())
                        print(APIException.get_status())
                        print("Eerrorrr")
        except Exception as e:
            print(e)


    def create_lead_task(self,data):
        print(data)
        self.operation = RecordOperations()
        records_list = []
        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)
    
        request = BodyWrappers()
        lead = ZCRMRecord()
        lead.add_field_value(Field.Leads.id(), data["idlead"])
        user = User()
        if len(data.get('promcode')) <10:
            #Kristel
            user.add_key_value('id', 3413022000025351001)
        else :
            #Ejecutivo Asignado
            user.add_key_value('id', int(data.get('promcode')))
        date_object=date.today()
        addField('Status',Choice('No iniciado'))
        addField('Due_Date', date_object)
        addField('Owner', user)
        addField('Description','Revisión y Envío de Contrato a Firma')
        addField('Send_Notification_Email', True)
        addField('$se_module', 'Leads')
        addField('What_Id', lead)
        addField('Tipo', Choice('Lead ADNPay'))
        addField('Subject', 'Revisión y Envío de Contrato a Firma')
        records_list.append(record)
        request.set_data(records_list)
        response = self.operation.create_records("Tasks", request)
        print("Response: ", response)


    #Task generated  Zoho crm
    def create_account_task(self,data):
        self.operation = RecordOperations()
        records_list = []
        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)
    
        desc = "Nombre: "+data["name"] +" Teléfono: "+data["phone"]
        request = BodyWrappers()
        account = ZCRMRecord()
        account.add_field_value(Field.Accounts.id(), data["idacc"])
        user = User()
        if len(data.get('promcode')) <10:
            ## Task sin gestor Michael Green 3413022000025351001
            ## 
            user.add_key_value('id', 3413022000025351001)
        else :
            #Ejecutivo Asignado
            user.add_key_value('id', int(data.get('promcode')))
        date_object=date.today()
        addField('Status',Choice('No iniciado'))
        addField('Due_Date', date_object)
        addField('Owner', user)
        addField('Description',desc + ': Revisión y Envío de Contrato a Firma')
        addField('Send_Notification_Email', True)
        addField('$se_module', 'Accounts')
        addField('What_Id', account)
        addField('Tipo', Choice('Contrato ADNPay'))
        addField('Subject', 'Revisión y Envío de Contrato a Firma')
        records_list.append(record)
        request.set_data(records_list)
        response = self.operation.create_records("Tasks", request)
        request = BodyWrappers()

        response_object = response.get_object()
        if response_object is not None:
            if isinstance(response_object, RecordActionWrapper):     
                action_response_list = response_object.get_data()
                print(action_response_list)
                action_response_list
                for action_response in action_response_list:
                    if isinstance(action_response, SuccessResponse):
                        zoho_id = action_response.get_details()["id"]
        

        return zoho_id
