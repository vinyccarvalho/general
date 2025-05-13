import os

def lock_file_init():
  ''' Pega o nome do arquivo.py e retorna arquivo.lck '''
  SCRIPT_FILE=os.path.basename(__file__)
  PREFIX_FILE = os.path.splitext(SCRIPT_FILE)[0]
  LOCK_FILE = PREFIX_FILE + '.lck'
  PARAMS_FILE = PREFIX_FILE + ".args"
  files_return = [LOCK_FILE, PARAMS_FILE]

  return files_return


if __name__ == "__main__":
    files_log = lock_file_init()
    print(f'lck: {files_log[0]}')
    print(f'lck: {files_log[1]}')
