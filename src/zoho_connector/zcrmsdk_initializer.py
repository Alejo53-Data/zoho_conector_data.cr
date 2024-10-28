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
from zcrmsdk.src.com.zoho.crm.api.layouts import Layout
import random
import os

class ZCRM_Initializer:

    def __init__(self) -> None:        
        main_path = './'
        log_path = main_path + "logs/sdk_log.log"
        os.system(f'echo > "{log_path}"')
        # Logs path 
        logger = Logger.get_instance(level=Logger.Levels.INFO,
                                    file_path= log_path)
        # Create an UserSignature instance that takes user Email as parameter
        user = UserSignature(email="zohomanager@data.cr")
        # Choice the environment for work
        environment = USDataCenter.PRODUCTION()
        # Token creation "OJO CAMBIAR TOKEN EN CASO DE CAMBIAR LA EL REFRESH"
        token = OAuthToken(client_id='1000.ODFVF4TA4TKUU6D0ZFHAXRWK63WTRH', 
                    client_secret='e1128e2f6d734d63b2dc1b758850f401ca087b80cd', 
                    token='1000.7fa0e064f66aa6d4269c697909da9095.0c800966911d44c553ed8de290835adf',
                    token_type=TokenType.REFRESH, 
                    redirect_url="https://www.abc.com")
        # Path for store the tokens
        store = FileStore(main_path + 'logs/token')
        # Configurations
        config = SDKConfig(auto_refresh_fields=True, pick_list_validation=False)
        # Resources path
        resource_path = main_path
        # Initialize the connection to the API
        Initializer.initialize(user=user, environment=environment, token=token, sdk_config=config, resource_path=resource_path, logger=logger, store=store)
        self.operations = RecordOperations()
        self.user_operations = UsersOperations()

    #Get id of  records of main Module
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


    #Update consecutive zoho CRM Main RECORD
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
    
    def addField(field,value):
        if value != None:
            record.add_key_value(field, value)

 
    #Generar Consecutivo DAT en el modulo "Config. Consecutive"
    #se actualiza el consecutivo en la principal
    def create_cconsecutivo(self,data):
        self.operation = RecordOperations()
        
        records_list = []
        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)

        #Get Main consecutive
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
                print("Config_E1")
                response_object = response.get_object()
                print(response_object.get_data())
                if response_object is not None:
                    print("Config_E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("Config_E3")                        
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
    
    ## Create customer account in zoho CRM
    ## Main Function
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
        
        idcon=data.get("condominium")
        
        print(f"{namem}    {idcon}")
        data['idcon']=idcon
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
                print("Account_E1")
                response_object = response.get_object()
                print(response_object.get_data())
                if response_object is not None:
                    print("Account_E2")
                    if isinstance(response_object, RecordActionWrapper):
                        print("Account_E3")
                        
                        action_response_list = response_object.get_data()
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
                                
                                if data['nameaccm'] in ['ftth'] :
                                    #Generar Tarea a Desarrollo de red si es FTTH
                                    print("uwuu")
                                    data['task_type']='2'
                                    idfeas=self.create_feasibility_ftth(data)
                                    data['deals']=idfeas
                                    self.create_task(data)

                                self.create_record_contract(data)
                                #Generar Tarea a Ejecutivo
                                data['task_type']='1'
                                idtask=self.create_task(data)
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
        
    ## Create contract
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

        request = BodyWrappers()
        addField('Tipo_Fiscal', Choice(id_type))
        addField('Status',Choice('Fase 2'))
        addField('Tipo_de_Contrato', Choice('Contrato Nuevo'))
        random_name = random.randint(10000, 99999)
        addField('Subject', str(random_name))
        idf={}
        addField('Segmento', Choice('B2C'))
        contact_name = ZCRMRecord()
        acc = ZCRMRecord()
        
        print(data.get('idcont'))
        contact_name.add_field_value(Field.Contacts.id(), int(data.get('idcont')))
        
        record.add_field_value(Field.Sales_Orders.contact_name(), contact_name)
        user = User()
        
        #Si tiene codigo promocional pertenece a un ejecutivo, en caso
        #Contrario es el owner es Michael Green
        if len(data.get('promcode')) <10:
            user.add_key_value('id', 3413022000025351001)
            record.add_key_value('Modo_de_Pago', Choice('Deposito'))

        else :
            user.add_key_value('id', int(data.get('promcode')))
            modo = "Deposito" if data['pay_type'] == "Depósito" else data['pay_type']
            record.add_key_value('Modo_de_Pago', Choice(modo))

        addField('Owner', user)
        #user

        #ACC ID
        acc.add_field_value(Field.Accounts.id(), int(data.get("idacc")))

        record.add_field_value(Field.Sales_Orders.account_name(), acc)
        #Contact_Name.
        date_object=date.today()
        print(date_object)
        ar=[]
        ar.append(Choice('Fibra Óptica'))
        ar1=[]
        ar1.append(Choice('Contrato Nuevo Servicio'))
        addField('Contacto_T_cnico_a', data.get('name'))
        record.add_key_value('Contacto_Facturaci_n', contact_name)
        addField('Phone', data.get("phone"))
        addField('Mobile', data.get("mobile"))
        drop=round(float(data.get('drop'))*float(data.get('exchange_rate')),0)
        addField('Drop_Cliente',drop)
        addField('Costo_Recurrente_ADN', 0.0)
        addField('Costo_Instalacion', 0.0)
        addField('Fecha_Proyeccion_Venta', date_object)
        circuit = data.get("circuito")
        coord=data.get("coorda")
        idcon=data.get("idcon")
        conobj=self.get_by_id(data.get("namem"),int(idcon))
        if data['nameaccm'] in ['ftth'] :
            feas = ZCRMRecord()
            feas.add_field_value(Field.Deals.id(), int(data.get("deals")))
            record.add_field_value(Field.Sales_Orders.deal_name(),feas)
            

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
        #Correcion Relacion
        addField('Relaci_n', Choice('01:10'))
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

          #IPTV de cortesía si tiene doble o triple play
        if data.get('type') in ['triple-play','dual-play']:
            iptv_line_item = InventoryLineItems()
            iptv_item_product = LineItemProduct()
            idproducto = 3413022000079848076
            iptv_item_product.set_id(idproducto)
            iptv_line_item.set_product(iptv_item_product)
            iptv_line_item.set_quantity(float(1))
            iptv_line_item.set_product_description('1 iptv de cortesía')
            iptv_line_item.set_list_price(float(0))
            iptv_line_item.set_discount('0')
            inventory_line_item_list.append(iptv_line_item)
            record.add_key_value('Product_Details', inventory_line_item_list)
        
        # Si tiene algún iptv extra
        if(data.get('iptv') == True):
            newprice = data.get('tax_free_price') + (float(data.get('extra_iptv')*1400.0))
            iptv_line_item = InventoryLineItems()
            iptv_item_product = LineItemProduct()
            idproducto = 3413022000079848076
            iptv_item_product.set_id(idproducto)
            iptv_line_item.set_product(iptv_item_product)
            iptv_line_item.set_quantity(float(data.get('extra_iptv')))
            iptv_line_item.set_product_description('Servicio IPTV Adicional B2C')
            iptv_line_item.set_list_price(float(4000.0))
            iptv_line_item.set_discount('0')
            inventory_line_item_list.append(iptv_line_item)
            record.add_key_value('Product_Details', inventory_line_item_list)
        
        #Si el paquete incluye ip pulica
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

        #Si tiene ip publica adicional
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

    #Create Invoicing contact
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
        addField('Mobile', data.get("mobile"))

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

    #Create lead when client exits in ZohoCRM
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
    def create_task(self,data):
        self.operation = RecordOperations()
        records_list = []
        record = ZCRMRecord()

        def addField(field,value):
            if value != None:
                record.add_key_value(field, value)
    
        desc = "Nombre: "+data["name"] +" Teléfono: "+data["phone"]
        request = BodyWrappers()
      
        user = User()
        
        date_object=date.today()
        module = ZCRMRecord()
        addField('Status',Choice('No iniciado'))
        addField('Due_Date', date_object)
        addField('Send_Notification_Email', True)

        #Tarea Ejecutivo
        if data['task_type']=='1':
            print("coño")
            module.add_field_value(Field.Accounts.id(), data["idacc"])
            modulem='Accounts'
            if len(data.get('promcode')) <10:
            ## Task sin gestor Michael Green 3413022000025351001
                user.add_key_value('id', 3413022000025351001)
            else :
            #Ejecutivo Asignado
                user.add_key_value('id', int(data.get('promcode')))
                
            addField('Owner', user)
            addField('Description',desc + ': Revisión y Envío de Contrato a Firma')
            addField('$se_module', modulem)
            addField('What_Id', module)
            addField('Tipo', Choice('Contrato ADNPay'))
            addField('Subject', 'Revisión y Envío de Contrato a Firma')
        #Task Desarollo de red type 2
        else:
              module.add_field_value(Field.Deals.id(), data["deals"])
              modulem='Deals'
              #id Jose prerez
              user.add_key_value('id', 3413022000166008001)
              addField('Owner', user)
              addField('Description','Realizar el estudio Factibilidad')
              addField('$se_module', modulem)
              addField('What_Id', module)
              addField('Tipo', Choice('Factibilidad'))
              addField('Subject', 'Estudio de Factibilidad '+data['name']+' ADNPAY')
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

    def create_feasibility_ftth(self,data):
        self.operation = RecordOperations()
        records_list = []
        def addField(field,value):
            if value != None:
             record.add_key_value(field, value)
    
        date_object=date.today()
        record = ZCRMRecord()
        acc = ZCRMRecord()
        contact_name = ZCRMRecord()
        acc.add_field_value(Field.Accounts.id(), int(data.get("idacc")))

        record.add_field_value(Field.Sales_Orders.account_name(), acc)
        contact_name.add_field_value(Field.Contacts.id(), int(data.get('idcont')))
        record.add_field_value(Field.Sales_Orders.contact_name(), contact_name)
        print(data)
        random_name = random.randint(10000, 99999)
        record.add_key_value("Deal_Name",str(random_name))
        ##Diseño Fibra optica
        layout = Layout()
        layout.set_id(3413022000067149245)
        record.add_key_value("Layout", layout)
        record.add_key_value("Plataforma_de_Enlace", Choice("Fibra Óptica"))
        record.add_key_value("Stage", Choice("Estudio de Factibilidad"))
        record.add_key_value("Empresa_Owner", Choice("American Data Networks"))
        record.add_key_value("Capacidad1", Choice("Simetrico"))
        record.add_key_value('Direcci_n_Exacta',data.get("address"))
        record.add_key_value('Coordenadas',str(data.get("coordinate")))
        record.add_key_value('Capacidad_Primer_Enlace',int(data.get("upload")))
        print(data.get("coordinate"))
        record.add_key_value("Amount",float(0))
        record.add_key_value("Closing_Date",date_object)
        record.add_key_value("Tipo_de_Red",Choice("FTTH"))
        if data.get('type') in ['dual-play']:
            record.add_key_value("IPTV",True)
        elif data.get('type') in ['triple-play']:
            record.add_key_value("Telefon_a_B2C",True)
            record.add_key_value("IPTV",True)
            
        #Tipo_de_Red
        #Telefon_a_B2C
        #IPTV

        

        acc = ZCRMRecord()
        acc.add_field_value(Field.Accounts.id(), int(data.get("idacc")))
        addField('Account_Name', acc)

        user = User()
        if len(data.get('promcode')) <10:
            user.add_key_value('id', 3413022000025351001)
        else :
            user.add_key_value('id', int(data.get('promcode')))

        addField('Owner', user)

       
        request = BodyWrappers()
        records_list.append(record)
        print("Record List: ", records_list)
        request.set_data(records_list)
        try:
            response = self.operation.create_records("Deals", request)
            print("E1_feass")
            response_object = response.get_object()
            print("request: ", response_object)
            print(response_object.get_data())
            if response_object is not None:
                print("E2_feas")
                if isinstance(response_object, RecordActionWrapper):
                    print("E3_feas")
                    action_response_list = response_object.get_data()
                    print(action_response_list)
                    for action_response in action_response_list:

                        # Check if the request is successful
                        if isinstance(action_response, SuccessResponse):
                            # Get the details dict
                            zoho_id = action_response.get_details()["id"]
                            print(zoho_id)
                            print("zoho_id dealsss")
                            
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