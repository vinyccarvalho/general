import configparser

def get_section_with_key(file_ini, key_name):
    """
    Retorna o nome das sessoes que possuem a chave informada
    """
    config = configparser.ConfigParser()
    config.sections()
    config.read(file_ini)

    sections_with_key = [ section for section in config.sections() if key_name in config(section) ]

    return sections_with_key


if __name__ == "__main__":
    file_ini = "/outsourcing/totvs/protheus/bin/appserver/appserver.ini"
    search_key = "RpoLanguage"

    sections_name = get_section_with_key(file_ini=file_ini, key_name=search_key)

    for section in sections_name:
        print("Sessão {0} encontrada.".format(section))
