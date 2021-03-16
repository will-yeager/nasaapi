from PyQt5 import uic, QtWidgets

import PyQt5.QtGui as c
from time import sleep

import requests

from urllib.request import urlretrieve

import imageio
import os
import glob

# api_key = PARA USAR ESSE PROGRAMA É NECESSARIO GERA UMA API KEY NO SITE DA NASA --> https://api.nasa.gov/index.html#apply-for-an-api-key
api_key = 'API-KEY' # <-- INSIRA SUA API KEY EM API-KEY
# DIRETORIO = r'SEU DIRETORIO' por exemplo -- > r'C:\Users\XXXX\Desktop\Nasaapi\imgs'
diretorio = r"C:\Users\XXX\Desktop\Nasaapi\\"

app = QtWidgets.QApplication([])
nasa=uic.loadUi(diretorio + "interface.ui")


# FUNÇÃO PARA PEGAR OS ARQUIVOS DA API
def FUNÇAO_DATA_EARTH():
    nasa.loading.setText('GERANDO...')
    ano = nasa.ano_input.text()
    mes = nasa.mes_input.text()
    dia = nasa.dia_input.text()
    url_epic = f"https://api.nasa.gov/EPIC/api/natural/date/{ano}-{mes}-{dia}"
    params = {
        'api_key':api_key
    }
    
    response = requests.get(url_epic, params=params).json()
    try: 
        response[0]['image']
    except:
        nasa.loading.setText('A DATA DIGITADA NÃO É VÁLIDA!')
    else:
        for c in range(1, len(response)):
            x = response[c]['image']
            url_down = f"https://epic.gsfc.nasa.gov/archive/natural/{ano}/{mes}/{dia}/png/{x}.png"
            urlretrieve(url_down, diretorio + 'imgs' + f"\\earth{c}.png")
        making_gif()

# BOTÃO
def gerar():
    deletar()

    FUNÇAO_DATA_EARTH()

# Gerar o GIF
def making_gif():
    png_dir = diretorio + "imgs"
    images = []
    for file_name in sorted(os.listdir(png_dir)):
        if file_name.endswith('.png'):
            file_path = os.path.join(png_dir, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(diretorio + "imgs\\terra.gif", images)

    nasa.loading.setText('GERANDO...')
    gif = diretorio + "imgs\\terra.gif"
    gif_da_terra = c.QMovie(gif)
    nasa.imagem.setMovie(gif_da_terra)
    gif_da_terra.start()
    nasa.loading.setText('CARREGADO COM SUCESSO')

# DELETAR ARQUIVOS DA PASTA IMAGENS
def deletar():  
    limpar = ' '
    clean = c.QMovie(limpar)
    nasa.imagem.setMovie(clean)
    
    directory = diretorio + "imgs"
    
    files = glob.glob(directory + '\*')

    for f in files:
        os.remove(f)

nasa.gerar.clicked.connect(gerar)

nasa.show()
app.exec()

