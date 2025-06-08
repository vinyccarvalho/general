import json

def carregar_json(arquivo):
    """Carrega um JSON a partir de um arquivo e valida sua estrutura."""
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{arquivo}' contém um JSON inválido.")
        return None
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return None

def salvar_json(arquivo, data):
    """Salva um JSON em um arquivo."""
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def adicionar_trecho(json_completo, json_novo, local):
    """Adiciona um trecho ao JSON completo no local especificado."""
    if local not in json_completo:
        print(f"Erro: O caminho '{local}' não existe no JSON completo.")
        return json_completo

    json_completo[local].update(json_novo)
    return json_completo

def deletar_trecho(json_completo, local):
    """Remove um trecho do JSON no local especificado."""
    if local not in json_completo:
        print(f"Erro: O caminho '{local}' não existe no JSON completo.")
        return json_completo

    del json_completo[local]
    return json_completo

def modificar_campo(json_completo, local, chave, novo_valor):
    """Modifica um campo existente no JSON."""
    if local not in json_completo:
        print(f"Erro: O caminho '{local}' não existe no JSON completo.")
        return json_completo

    if chave not in json_completo[local]:
        print(f"Erro: A chave '{chave}' não existe em '{local}'.")
        return json_completo

    json_completo[local][chave] = novo_valor
    return json_completo

# 🏗️ Exemplo de uso
arquivo_json_completo = "json_completo.json"
arquivo_json_novo = "json_novo.json"
local_para_inserir = "config"

json_completo = carregar_json(arquivo_json_completo)
json_novo = carregar_json(arquivo_json_novo)

if json_completo and json_novo:
    json_completo = adicionar_trecho(json_completo, json_novo, local_para_inserir)
    json_completo = modificar_campo(json_completo, local_para_inserir, "versao", "2.0")
    json_completo = deletar_trecho(json_completo, "antigo")

    salvar_json(arquivo_json_completo, json_completo)
    print("✅ JSON atualizado com sucesso!")
