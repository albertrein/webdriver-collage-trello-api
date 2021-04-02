from selenium import webdriver
import time
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def volta_para_home():
	time.sleep(4)
	driver.find_element_by_xpath('//*[@id="sidebar-menu"]/ul/li[1]/a').click()

def get_atividades():
	atividades = []
	itens_disciplina = driver.find_elements_by_class_name('row.p-a.m-l--22')
	if itens_disciplina.__len__() is 0:
		return []
	for item in itens_disciplina:
		if item.find_elements_by_class_name('fas.fa-star').__len__() > 0: # Possui icone da atividade
			atividades.append(item)

	return atividades


def get_atividade_dados(atividade):
	informacoes = atividade.find_elements_by_class_name('ng-binding') #capturando spans com os textos
	atividade_entregue = atividade.find_elements_by_class_name('borda-amarela') #capturando spans com os textos
	dict_atividade = ({'titulo' : informacoes[0].text, 'data' : informacoes[1].text})
	if atividade_entregue.__len__() > 0:
		dict_atividade.update({'status': 'concluida'})
		return dict_atividade
	dict_atividade.update({'status': 'nao-concluida'})
	return dict_atividade


def update_dados_cadeiras(lista1, lista2):
    for item_lista2 in lista2:
        item_lista1 = list(filter( lambda itm : itm['nome'] == item_lista2['nome'] , lista1))
        if item_lista1.__len__() > 0:
            for subitem_lista2 in item_lista2['atividades']:
                subitem_lista1 = list(filter(lambda subitm : subitm['titulo'] == subitem_lista2['titulo'], item_lista1[0]['atividades']))
                if subitem_lista1.__len__() > 0:
                	if subitem_lista1[0]['status'] == subitem_lista2['status'] and subitem_lista1[0]['data'] == subitem_lista2['data']:
                	    print('Item lista2:', item_lista2['nome'], 'Imutada atividade:', subitem_lista2['titulo'], '\n')
                	else:
                	    print('Item lista2:', item_lista2['nome'], 'atualizada atividade:', subitem_lista2['titulo'], '\n')
                else:
                    print('Item lista2:', item_lista2['nome'], 'Nova atividade:', subitem_lista2['titulo'], '\n')



"""
Desativa a visualização da página
options = webdriver.ChromeOptions();
options.add_argument('headless');
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
"""
#captura informações de configuração
with open('config/config.json') as file_config:
	config = json.load(file_config)
	file_config.close()

#Instancia webdriver como chrome
driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 50)
driver.get('https://servicos.ulbra.br/login/ava')
driver.set_window_size(1024, 768)

time.sleep(3)

login = driver.find_element_by_name('login')
login.send_keys(config['cgu'])

time.sleep(3)

proximo = driver.find_element_by_id('fazerLogin')
proximo.click()

time.sleep(3)

senha = wait.until(EC.presence_of_element_located((By.ID, 'senha')))
senha.send_keys(config['senha'])


time.sleep(3)

entrar = driver.find_element_by_id('fazerLogin')
entrar.click()

time.sleep(3)

wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
lista_de_cadeiras = driver.find_elements_by_tag_name('h2')

titulos_cadeiras = []
for cadeira in lista_de_cadeiras:
	titulos_cadeiras.append(cadeira.text)


cadeiras = []
for i in range(lista_de_cadeiras.__len__()):
	wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn.btn-block.btn-success.mt-2.ng-binding'))) #cadeiras
	links_salas_de_aula = driver.find_elements_by_class_name('btn.btn-block.btn-success.mt-2.ng-binding')
	links_salas_de_aula[i].click()
	try:
		wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row.p-a.m-l--22'))) #itens da cadeira
	except:
		volta_para_home()
		continue
	lista_atividade = get_atividades()
	cadeiras.append({'nome': titulos_cadeiras[i], 'atividades' : []})
	for atividade in lista_atividade:
		cadeiras[i]['atividades'].append(get_atividade_dados(atividade))
	
	volta_para_home()

#varifica mudanças
update_dados_cadeiras(config['aula'], cadeiras)
#atualiza informacoes
config['aula'] = cadeiras

#atualiza arquivo de configuracoes
with open('config/config.json', 'w', encoding='utf-8') as file_config:
	json.dump(config, file_config, ensure_ascii=False, indent=4)
