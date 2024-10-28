from zcrmsdk.src.com.zoho.crm.api.user_signature import UserSignature
from zcrmsdk.src.com.zoho.crm.api.dc import USDataCenter
from zcrmsdk.src.com.zoho.api.authenticator.store import FileStore
from zcrmsdk.src.com.zoho.api.logger import Logger
from zcrmsdk.src.com.zoho.crm.api.initializer import Initializer
from zcrmsdk.src.com.zoho.api.authenticator.oauth_token import OAuthToken, TokenType
from zcrmsdk.src.com.zoho.crm.api.record import *
from zcrmsdk.src.com.zoho.crm.api.users import *
from zcrmsdk.src.com.zoho.crm.api.sdk_config import SDKConfig
import datetime
from tzlocal import get_localzone
import pymssql

def query(q):
    connection = pymssql.connect("192.168.81.191:49170", "sa", "7ssvwAvKVUYB6", "ADNCube")

    cursor = connection.cursor(as_dict=True)

    cursor.execute(q)

    connection.commit()

    cursor.close()
    connection.close()


def QueryRequestOneColumn(column="id",table="crm_owner"):
    connection = pymssql.connect("192.168.81.191:49170", "sa", "7ssvwAvKVUYB6", "ADNCube")

    cursor = connection.cursor(as_dict=True)

    cursor.execute('SELECT '+str(column)+' FROM '+ str(table))
    resp_list = []
    for row in cursor:
        resp_list.append(row[str(column)])

    connection.close()
    return resp_list


def get_users_new():

    main_path = 'C:/Users/Progra/Documents/Dev/Python/LeadsCRMBOOKS/'
    # Logs path 
    logger = Logger.get_instance(level=Logger.Levels.INFO,
                                 file_path= main_path + "logs/sdk_log.log")

    # Create an UserSignature instance that takes user Email as parameter
    user = UserSignature(email="zohomanager@data.cr")

    # Choice the environment for work
    environment = USDataCenter.PRODUCTION()

    # Token creation
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

    # Request ====================================================================================================

    db_fields = ['id','country_locale','first_name','last_name','full_name','email','created_time','modified_time','status','zuid','currency','role','profile','created_by','modified_by','language']

    response = UsersOperations().get_users()

    response_object = response.get_object()

    user_list = response_object.get_users()

    data_ready = QueryRequestOneColumn()
    new_user =[]

    for user in user_list:

        user_data = user.get_key_values()
        if str(user_data["id"]) not in data_ready:
            new_dicc = {}

            for x,y in user_data.items():
                if x.lower() in db_fields:
                    if x in ['profile', 'Created_By', 'role', 'Modified_By']:
                        if x == 'profile':
                            y = user.get_profile().get_name()
                        elif x == 'role':
                            y = user.get_role().get_name()
                        else:
                            y= y.get_id()

                    new_dicc[x.lower()] = y
        
            new_user.append(new_dicc)
        else: continue

    return new_user


def user_create(resp):
    def tzlocal():
      tz = get_localzone()
      return tz

    for user in resp:
        column = ""
        value = ""

        user['created_time']=str(user['created_time'])[:-6]
        user['modified_time']=str(user['modified_time'])[:-6]

        for k,v in user.items():
            if v == False:
                user[k] = 0
            if v == True:
                user[k] = 1
            if v == None:
                user[k] = 'null'

        for k,v in user.items():
            column += k + ", "
            try:
                x=int(v)
                value += str(v) + ', '
            except:
                if v == 'null': 
                    value += v + ', '
                else:
                    value += "'" + str(v) + "', "


        column = column[:-2]
        value = value[:-2]


        query_sql = "INSERT INTO crm_owner (" + column + ") VALUES (" + value + ");"

        query(query_sql)


def user_update(resp):
    def tzlocal():
      tz = get_localzone()
      return tz

    for user in resp:
        data_to_set = ""

        user['created_time']=str(user['created_time'])[:-6]
        user['modified_time']=str(user['modified_time'])[:-6]

        account_id=0

        for k,v in user.items():
            if k == "id":
                account_id = v


        for k,v in user.items():
            if v == False:
                user[k] = 0
            if v == True:
                user[k] = 1
            if v == None:
                user[k] = 'null'

        for k,v in user.items():
            column = k + "="
            try:
                x=int(v)
                column += str(v) + ', '
            except:
                if v == 'null': 
                    column += v + ', '
                else:
                    column += "'" + str(v) + "', "
            
            data_to_set += column


        data_to_set = data_to_set[:-2]


        query_sql = "UPDATE owner_crm SET "+data_to_set+" WHERE id = "+str(account_id)+";"

        try:
            query(query_sql)
        except:pass

