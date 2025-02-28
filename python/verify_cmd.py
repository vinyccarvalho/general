import json
import re

def tcm_ananlyse_error(cmd_json, error_type):
     print("Comando {0}".format(cmd_json["command"]))

if __name__ == "__main__":
    pipeline_json_file = '/home/vinicius/Downloads/INC15863487/pipeline.json'
    tcm_agent_log_file = 'tcm_agent.log'

    with open(pipeline_json_file) as pipeline_file:
        pipeline_json = json.load(pipeline_file)

    print(f'Analisando o pipeline {pipeline_json["pipeline"]["pipeline_id"]}')

    for cmd in pipeline_json["tcm"]:
            match cmd["status"]:
                case "TIMEOUT":
                    print("Analisando no cmd_id: {0} ({1})".format(cmd["cmd_id"], cmd["status"]))

    # Expressão regular para buscar o trecho de código que você deseja
    #regex_pattern = r'seu_padrão_regex_aqui'

    # Abrindo o arquivo de log
    #with open(tcm_agent_log_file, 'r') as file:
        #log_contents = file.read()

    # Procurando todos os trechos que correspondem ao padrão regex
    #matches = re.findall(regex_pattern, log_contents)

    # Exibindo os resultados encontrados
    #for match in matches:
    #    print(match)
