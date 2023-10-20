import sys

def arquivos_py_modificados(arquivos_como_texto: str) -> None:
    lista_arquivos = arquivos_como_texto.split('\n')
    arquivos_py = [arquivo for arquivo in lista_arquivos if arquivo.endswith('.py')]
    print(' '.join(arquivos_py))

if __name__ == '__main__':
    # recupera string passada como argumento
    arquivos_py_modificados(sys.argv[1])
