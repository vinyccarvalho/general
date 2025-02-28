# https://totvscloud.atlassian.net/browse/STCDP-3189
# Listagem de clientes e versão de e-Social (Ministerio do trabalho)
# Conecta em windows ou linux, em oracle ou sqlserver e realiza a query

import os
import sys
import json

PY2 = sys.version_info[0] == 2

try:
    import pymssql  # Para SQL Server
except ImportError:
    pymssql = None

try:
    import cx_Oracle  # Para Oracle
except ImportError:
    cx_Oracle = None


# Obter o tipo do so
def get_os():    
    os_name = os.name

    if os_name == 'posix':
        os_return = "linux"
    elif os_name == 'nt':
        os_return = "windows"
    
    return os_return


# Obtem o tipo de banco de dados
def get_db_type():
    if os_type == "linux":
        FILE_KEYS_CUSTOMER = "/opt/setup_protheus/keys_customer.txt"
        if os.path.exists(FILE_KEYS_CUSTOMER):
            with open(FILE_KEYS_CUSTOMER) as json_file:
                JSON_KEYS_CUSTOMER = json.load(json_file)
                json_file.close()

        # Obtem db_type
        if 'db_oracle' in JSON_KEYS_CUSTOMER and JSON_KEYS_CUSTOMER['db_oracle'] == 'True':
            db_type = 'oracle'
        elif 'db_postgresql' in JSON_KEYS_CUSTOMER and JSON_KEYS_CUSTOMER['db_postgresql'] == 'True':
            db_type = 'postgresql'
        else:
            db_type = 'mssql'

    elif os_type == "windows":
        if custom_data['topology']['databases'][0]['type'] == "oracleserver":
            db_type = 'oracle'
        elif custom_data['topology']['databases'][0]['type'] == "sqlserver":
            db_type = 'mssql'
        elif custom_data['topology']['databases'][0]['type'] == "postgres":
            db_type = 'postgres'

    return db_type


def get_infos():
    # Obtem os dados do custom data
    if os_type == "windows":
        FILE_CUSTOM_DATA = "C:/outsourcing/totvs/cloud/scripts/protheus/setup/custom-data.json"
        
    elif os_type == "linux":
        #diretorio base para os binarios do protheus no padrao de deploy JPS
        SETUP_PROTHEUS_DIR = '/opt/setup_protheus'
        FILE_CUSTOM_DATA = SETUP_PROTHEUS_DIR + "/custom-data.json"
        FILE_KEYS_CUSTOMER = SETUP_PROTHEUS_DIR + "/keys_customer.txt"

    if os.path.exists(FILE_CUSTOM_DATA):
        with open(FILE_CUSTOM_DATA) as json_file:
            custom_data = json.load(json_file)
            json_file.close()

def get_custom_data():
    # Obtem os dados do custom data
    if os_type == "windows":
        FILE_CUSTOM_DATA = "C:/outsourcing/totvs/cloud/scripts/protheus/setup/custom-data.json"
        
    elif os_type == "linux":
        FILE_CUSTOM_DATA = '/opt/setup_protheus/custom-data.json'

    if os.path.exists(FILE_CUSTOM_DATA):
        with open(FILE_CUSTOM_DATA) as json_file:
            custom_data = json.load(json_file)
            json_file.close()

    return custom_data


def db_connect():
    server   = "{0}:{1}".format(str(custom_data['topology']['databases'][0]['host']), str(custom_data['topology']['databases'][0]['port']))
    user     = str(custom_data['topology']['databases'][0]['db_users'][0]['name'])
    password = str(custom_data['topology']['databases'][0]['db_users'][0]['password'])
    database = str(custom_data['topology']['databases'][0]['name'])

    if db_type == "oracle":
        if not cx_Oracle:
            raise ImportError("cx_Oracle nao instalado! Instale com: pip install cx_Oracle")
        
        host     = str(custom_data['topology']['databases'][0]['host'])
        port     = str(custom_data['topology']['databases'][0]['port'])
        user     = str(custom_data['topology']['databases'][0]['user'])
        password = str(custom_data['topology']['databases'][0]['password'])            
        service_name = '{}_high.paas.oracle.com'.format(database)
        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
        conn.autocommit = True
        return conn

    elif db_type == "mssql":
        if not pymssql:
            raise ImportError("pymssql nao instalado! Instale com: pip install pymssql")
        
        conn = pymssql.connect(server=server, user=user, password=password, database=database)

        return conn
    else:
        raise Exception("Banco do tipo {0} nao suportado pelo script".format(db_type))


if __name__ == '__main__':

    # Sistema operacional
    os_type = get_os()

    # Custom data
    custom_data = get_custom_data() 

    # Tipo de banco
    db_type = get_db_type()

    # get_infos()

    # Tenta conectar e rodar a querie de acordo com cada tipo de banco
    try:
        conn = db_connect()
    except Exception as err:
        print("Nao foi possivel conectar no banco de dados {0}".format(err))

    if db_type == "mssql":
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.tables WHERE name LIKE 'SX6%'")

    elif db_type == "oracle":
        cursor = conn.cursor()
        # Query para buscar tabelas que comecam com SX6 no Oracle
        cursor.execute("SELECT TABLE_NAME FROM ALL_TABLES WHERE TABLE_NAME LIKE 'SX6%'")

    # Lista com o nome das tabelas SX6* encontradas
    tables = [row[0] for row in cursor.fetchall()]

    # Lista para armazenar os resultados
    result_list = []

    # Executar query para cada tabela e coletar resultados
    for table in tables:
        query = "SELECT X6_FIL, X6_VAR, X6_CONTEUD, X6_CONTSPA, X6_CONTENG FROM {} WHERE X6_VAR = 'MV_ESOCIAL' AND D_E_L_E_T_ = ' '".format(table)
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]  # Pegar nomes das colunas

        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))  # Transformar em dicionario
            row_dict["Origem"] = table  # Adicionar nome da tabela de origem
            result_list.append(row_dict)

    # Fechar conexao
    cursor.close()
    conn.close()

    # Converter a lista para JSON
    json_output = json.dumps(result_list, indent=4, ensure_ascii=False)

    print(json_output)

    # # Exibir JSON (compativel com Python 2 e 3)
    # if PY2:
    #     print json_output  # Python 2
    # else:
    #     print(json_output)  # Python 3
