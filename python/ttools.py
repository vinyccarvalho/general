import urllib3
import warnings
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

import os
import sys
import json
import logging
import datetime
import base64
import re

if sys.version_info.major == 3:
    import configparser as ConfigParser
else:
    import ConfigParser

#biblioteca de constantes essenciais para busca dos parametros da Topologia da VM
from protheus_utils import *

__version__ = '2.0.0'

def get_service_inventory():
    '''Funcao responsavel por buscar os dados de inventario no tcloud'''

    post_tcloud = { "topology_api_key":JSON_KEYS_CUSTOMER['topology_api_key'], \
                    "topology_api_secret":JSON_KEYS_CUSTOMER['topology_api_secret']}

    url_inventory = "curl -X POST https://api-tcloud.fluig.cloudtotvs.com.br/dev/customer/"+JSON_KEYS_CUSTOMER["customer"]+"/topologies/"+JSON_KEYS_CUSTOMER["topologies"]+"/inventory?action=get_inventory -d '{0}'".format(json.dumps(post_tcloud))

    try:
        json_inventory = os.popen(url_inventory).read().replace("\n","")
        ret_inventory = json.loads(json_inventory)
    except:
        ret_inventory = {}

    return ret_inventory


def set_inventory(file_json):

    print("Setando inventario")

    with open(file_json) as json_keys_connections:
        connections = json.load(json_keys_connections)
        json_keys_connections.close()

        #Registro do inventario no tcloud
        try:
            connections['version'] = get_release()
            connections['core_os_version'] = str(get_linux_version()[0])
        except Exception:
            pass

        put_service_inventory(connections)
        print(json.dumps(connections))


if __name__ == "__main__":

    if sys.argv[1] == "inventory":
        print(json.dumps(get_service_inventory()))

    if sys.argv[1] == "set_inventory":
        file_json = sys.argv[2]
        set_inventory(file_json)
        print(json.dumps(get_service_inventory()))

