import subprocess


def run_cmd(command):
    """
    Roda um comando no S.O. e captura o resultado, retorna uma lista\n
    ['True/False',    # Se o comando deu certo ou nao\n
    'codigo_retorno', # Codigo de retorno 0,1,2...\n
    'stdout', # Texto de saida padrao do comando\n
    'sterr']  # Texto de saida do erro ou exception\n\n
    Ex de uso: \n
    run_cmd(['echo', '-e', 'Hello world!'])\n
    Ex de uso com erro:\n
    run_cmd(['ls', '-l', '/pasta_que_nao_existe'])\n
    Ex de uso com exception:\n
    run_cmd(['comando_que_no_ecsiste'])
    """

    try:
        resultado = subprocess.run(command, check=True, capture_output=True, text=True)
        resultado_return = [
            True,
            resultado.returncode,
            resultado.stdout,
            resultado.stderr,
        ]

        return resultado_return

    except subprocess.CalledProcessError as e:
        resultado_return = [False, e.returncode, e.stdout, e.stderr]
        return resultado_return
    except FileNotFoundError as e:
        resultado_return = [False, 1, None, e]
        return resultado_return
    except Exception as e:
        resultado_return = [False, 1, None, e]
        return resultado_return


def format_disk(dev, file_system):
    """
    Usage:\n
    mount_disk("/dev/sda1", "/mnt/disk", "xfs", False)
    """

    log.debug("Iniciando processo de formatacao do disco {0} em {1}".format(dev, file_system))

    format_cmd = ["mkfs." + file_system, dev]
    if run_cmd(format_cmd):
        log.debug("Disco {0} formatado com sucesso!".format(dev))

    return 0


if __name__ == "__main__":
    format_disk("/root/disco_virtual.img", "xfs")
