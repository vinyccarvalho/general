import urllib3
import warnings
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

import os
import subprocess
import sys
import json

if sys.version_info.major == 3:
    import configparser as ConfigParser
else:
    import ConfigParser

#biblioteca de constantes essenciais para busca dos parametros da Topologia da VM
from protheus_utils import *

__version__ = '2.0.0'


def run_cmd(command, src_path=None, shell=False):
    """
    Roda um comando no S.O. e captura o resultado e retorna em uma lista
    """
    # Ajuste no path
    os.environ["PATH"] = "/sbin:" + os.environ["PATH"]
    os.environ["PATH"] = "/usr/sbin:" + os.environ["PATH"]
    os.environ["PATH"] = "/usr/local/sbin:" + os.environ["PATH"]

    try:
        # Define os parametros do Popen
        popen_kwargs = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "shell": shell
        }
        if src_path:
            popen_kwargs["cwd"] = src_path

        # Executa o comando
        process = subprocess.Popen(command, **popen_kwargs)
        stdout, stderr = process.communicate()

        if sys.version_info[0] < 3:
            resultado_return = {
                "success": process.returncode == 0,
                "return_code": process.returncode,
                "stdout": stdout,
                "stderr": stderr
            }
        else:
            resultado_return = {
                "success": process.returncode == 0,
                "return_code": process.returncode,
                "stdout": stdout.decode("utf-8"),
                "stderr": stderr.decode("utf-8")
            }

        return resultado_return

    except OSError as e:  # FileNotFoundError nao existe no Python 2
        return {
            "success": False,
            "return_code": 1,
            "stdout": None,
            "stderr": str(e)
        }
    except Exception as e:
        return {
            "success": False,
            "return_code": 1,
            "stdout": None,
            "stderr": str(e)
        }


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


def set_tp_teste():
    """
    Altera o ambiente para ser do tipo de desenvolvimento
    """

    keys_customer_cmd = 'sed -ri \'s/"tp_teste": "False"/"tp_teste": "True"/g\' /opt/setup_protheus/keys_customer.txt'
    keys_customer = run_cmd(command=keys_customer_cmd, shell=True)

    if keys_customer["success"]:
        print(keys_customer["stdout"])
    else:
        print(keys_customer["stderr"])

    tp_teste_cmd = "> /opt/setup_protheus/tp_teste"
    tp_teste = run_cmd(command=tp_teste_cmd, shell=True)

    if tp_teste["success"]:
        print(tp_teste["stdout"])
    else:
        print(tp_teste["stderr"])


if __name__ == "__main__":

    if sys.argv[1] == "inventory":
        print(json.dumps(get_service_inventory()))

    if sys.argv[1] == "set_inventory":
        file_json = sys.argv[2]
        set_inventory(file_json)
        print(json.dumps(get_service_inventory()))

    if sys.argv[1] == "set_tp_teste":
        set_tp_teste()
