#IMPORTANDO BIBLIOTECAS
import pyautogui
import time
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pyperclip
import milettoautorun as mlr
import milettoautowpp as wpp
import googlesheets_read as sheets

def conta_entradas(tabela):
    controle = tabela['Carimbo de data/hora'].count()
    return controle

def atualiza_tabela(SAMPLE_SPREADSHEET_ID, SERVICE_ACCOUNT_FILE):
    tabela = sheets.executar(SAMPLE_SPREADSHEET_ID, SERVICE_ACCOUNT_FILE)
    tabela = tabela.dropna(how="any", axis=0)
    tabela['Valor do pedido'] = tabela['Valor do pedido'].str.replace(',', '.', regex=True)
    tabela['Valor do pedido'] = pd.to_numeric(tabela['Valor do pedido'], errors='coerce', downcast='integer')
    return tabela

def filtra_novas_entradas(tabela, controle):
    list=[]
    for i in range(0, controle, 1):
        list.append(i)
    tabela_aux = tabela.drop(tabela.index[list])
    return tabela_aux

def envia_infos_nova_entrada(tabela, controle):
    tabela_aux = filtra_novas_entradas(tabela, controle)
    num = conta_entradas(tabela_aux)

    for i in range(0, num, 1):
        #salvar informações
        vendedor = tabela_aux.iloc[i]['Vendedor responsável pela venda']
        valor = tabela_aux.iloc[i]['Valor do pedido']
        pedido = tabela_aux.iloc[i]['id_pedido']
        print("O {} realizou uma venda no valor de R$ {}. Numero do pedido {}".format(vendedor, valor, pedido))
        texto = ("O {} realizou uma venda no valor de R$ {}. Numero do pedido {}".format(vendedor, valor, pedido))
        time.sleep(2)

    cria_graph(tabela)
    whats = wpp.Whatsapp()
    wpp.abrir_wpp(whats)
    wpp.abrir_grupo(whats, 'automacoes python')
    time.sleep(1)


    pyperclip.copy(texto)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    time.sleep(2)

    pyautogui.write('Segue status atualizado das vendas')
    wpp.enviar_foto_wpp(whats, r'C:\Users\THALES\PycharmProjects\automacoes\teste_graph_vendas.png')
    pyautogui.press('enter')

def cria_graph(tab):
    tabela = tab
    graph = sns.barplot(x=tabela['Vendedor responsável pela venda'], y=tabela['Valor do pedido'], data=tabela, ci=0)
    graph.set(xlabel='', ylabel='Valor Vendido (R$)')
    graph.axes.set_title('Vendas x Vendedor', fontsize=18, color="black", alpha=1)
    plt.savefig("teste_graph_vendas.png", format='png')

def executar():
    pyautogui.PAUSE = 0.5
    spreadsheet_id = '1xmDWfsWMqQbfnJXjIHJfw5jG85WdcH0aqreO_YvbZds'
    SERVICE_ACCOUNT_FILE = 'keys.json'

    tabela = atualiza_tabela(spreadsheet_id, SERVICE_ACCOUNT_FILE)
    print(tabela)
    tabela.info()
    cria_graph(tabela)

    controle = conta_entradas(tabela)
    print('Iniciando o código com {} entradas na base de dados!'.format(controle))
    print('Aguardando uma nova entrada...')
    x=0

    while x==0:
        time.sleep(10)
        tabela = atualiza_tabela(spreadsheet_id, SERVICE_ACCOUNT_FILE)
        if controle < conta_entradas(tabela):
            print("Nova entrada na base de dados detectada!")
            envia_infos_nova_entrada(tabela, controle)
            controle = conta_entradas(tabela)
            print('Aguardando uma nova entrada...')

if(__name__ == '__main__'):
    executar()