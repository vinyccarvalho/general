import subprocess


def run_cmd(command):
  '''
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
  '''

  try:
      resultado = subprocess.run(
          command,
          check=True,
          capture_output=True,
          text=True
      )
      resultado_return=[True, resultado.returncode, resultado.stdout, resultado.stderr]

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

if __name__ == "__main__":
    cmd=['ls', '-l', '/']

    teste = run_cmd(cmd)

    if teste[0]:
        print("Feito!")
        print(f"code: {teste[1]}")
        print(f"stdout: {teste[2]}")
        print(f"stderr: {teste[3]}")

    else:
        print("Erro")
        print(f"code: {teste[1]}")
        print(f"stdout: {teste[2]}")
        print(f"stderr: {teste[3]}")
