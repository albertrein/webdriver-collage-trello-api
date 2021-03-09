from selenium import webdriver
import time
import json
from webdriver_manager.chrome import ChromeDriverManager

def volta_para_home():
	time.sleep(4)
	driver.find_element_by_xpath('//*[@id="sidebar-menu"]/ul/li[1]/a').click()


"""
Desativa a visualização da página
options = webdriver.ChromeOptions();
options.add_argument('headless');
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
"""

with open('config/config.json') as file_config:
	config = json.load(file_config)
	file_config.close()


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://servicos.ulbra.br/login/ava')
driver.set_window_size(1024, 768)

time.sleep(3)

login = driver.find_element_by_name('login')
login.send_keys(config['cgu'])

time.sleep(3)

proximo = driver.find_element_by_id('fazerLogin')
proximo.click()

time.sleep(3)

senha = driver.find_element_by_id('senha')
senha.send_keys(config['senha'])


time.sleep(3)

entrar = driver.find_element_by_id('fazerLogin')
entrar.click()

time.sleep(3)


lista_de_cadeiras = driver.find_elements_by_tag_name('h2')

for cadeira in lista_de_cadeiras:
	print(cadeira.text)



for i in range(lista_de_cadeiras.__len__()):
	links_salas_de_aula = driver.find_elements_by_class_name('btn.btn-block.btn-success.mt-2.ng-binding')
	links_salas_de_aula[i].click()
	volta_para_home()
	time.sleep(3)





