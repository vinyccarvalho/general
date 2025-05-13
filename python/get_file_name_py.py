import os

# Obtem o nome do arquivo
nome_arquivo = os.path.basename(__file__)
nome_sem_extensao = os.path.splitext(nome_arquivo)[0]

print("Este script esta sendo executado como: " + nome_arquivo)
print("Este script esta sendo executado como: " + nome_sem_extensao)


