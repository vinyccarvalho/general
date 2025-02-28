import os
import sys
import json


if __name__ == '__main__':
    FILE_CUSTOM_DATA = "C:/outsourcing/totvs/cloud/scripts/protheus/setup/custom-data.json"

    if os.path.exists(FILE_CUSTOM_DATA):
        with open(FILE_CUSTOM_DATA) as json_file:
            custom_data = json.load(json_file)
            json_file.close()
    else:
        raise Exception("Arquivo {0} nao encontrado".format(FILE_CUSTOM_DATA))

    # db_type = (Get-DBNameByType -DBType $custom_data.topology.databases[0].type).tolower()
    db_type = custom_data['topology']['databases'][0]['type']
    print("db_type: {0}".format(db_type))
