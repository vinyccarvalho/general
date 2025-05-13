import os
import platform
import stat
from colorama import init, Fore

# Inicializa colorama para compatibilidade no Windows
init(autoreset=True)

def formatar_saida(mensagem, status):
    """Formata a saída com cores e indentação."""
    cores = {
        "OK": Fore.GREEN,
        "ERRO": Fore.RED,
        "ALERTA": Fore.YELLOW
    }
    return f"{mensagem.ljust(50)} {cores.get(status, '')}{status}"

def verificar_sistema():
    """Verifica o sistema operacional."""
    sistema = platform.system()
    print(formatar_saida(f"Detectando sistema operacional: {sistema}", "OK"))
    return sistema

def verificar_arquivo(caminho):
    """Verifica se um arquivo existe."""
    if os.path.exists(caminho):
        print(formatar_saida(f"Verificando arquivo: {caminho}", "OK"))
    else:
        print(formatar_saida(f"Verificando arquivo: {caminho}", "ALERTA"))

def verificar_permissoes(caminho):
    """Verifica permissões básicas do arquivo."""
    if os.path.exists(caminho):
        permissoes = oct(os.stat(caminho).st_mode)[-4:]
        print(formatar_saida(f"Permissões do arquivo {caminho}: {permissoes}", "OK"))
    else:
        print(formatar_saida(f"Permissões do arquivo {caminho}: Arquivo não encontrado", "ALERTA"))

def verificar_processo(nome_processo):
    """Verifica se um processo está rodando."""
    try:
        if platform.system() == "Windows":
            comando = f'tasklist | findstr /I "{nome_processo}"'
        else:
            comando = f'ps aux | grep -i "{nome_processo}" | grep -v grep'
        
        resultado = os.popen(comando).read()
        if resultado:
            print(formatar_saida(f"Verificando processo: {nome_processo}", "OK"))
        else:
            print(formatar_saida(f"Verificando processo: {nome_processo}", "ALERTA"))
    except Exception as e:
        print(formatar_saida(f"Erro ao verificar processo: {e}", "ERRO"))

def executar_validacoes():
    """Executa todas as validações."""
    print("\n🔍 Iniciando validação do sistema...\n")
    verificar_sistema()
    verificar_arquivo("/etc/passwd" if platform.system() == "Linux" else "C:\\Windows\\System32\\cmd.exe")
    verificar_permissoes("/etc/passwd" if platform.system() == "Linux" else "C:\\Windows\\System32\\cmd.exe")
    verificar_processo("sshd" if platform.system() == "Linux" else "explorer.exe")
    print("\n✅ Validação concluída!\n")

if __name__ == "__main__":
    executar_validacoes()

