import requests
import json


class TrelloIntegration:
    authentication = {}
    trello_lists = []
    def __init__(self, key, token, lists):
        TrelloIntegration.authentication.update({'key' : key})
        TrelloIntegration.authentication.update({'token' : token})
        TrelloIntegration.trello_lists.append(lists)

    def update_key(self, key):
        TrelloIntegration.authentication['key'] = key


    def update_token(self, token):
        TrelloIntegration._authentication['token'] = token

    def update_card(self, dados):
        return 0

    def get_cards_list(self):
        return 0

    def convert_data(self, data_br):
        array_data = data_br.split('/')
        return array_data[1]+'/'+array_data[0]+'/'+array_data[2]

    def insert_new_card(self, titulo, vencimento, id_numero_lista):
        url = "https://api.trello.com/1/cards"

        query = {
           'key': TrelloIntegration.authentication['key'],
           'token': TrelloIntegration.authentication['token'],
           'name': titulo,
           'due': self.convert_data(vencimento),
           'idList': TrelloIntegration.trello_lists[id_numero_lista]
        }
        response = requests.request(
           "POST",
           url,
           params=query
        )
        return response.text

    def get_cards_list(self, id_lista):
        url = f"https://api.trello.com/1/lists/{id_lista}/cards"

        query = {
           'key': TrelloIntegration.authentication['key'],
           'token': TrelloIntegration.authentication['token'],
        }
        response = requests.request(
           "GET",
           url,
           params=query
        )
        return response.text

    def get_card_id_by_title(self, id_lista, card_titulo):
        response_list_of_cards = self.get_cards_list(id_lista)
        list_of_cards = json.loads(response_list_of_cards)        
        for card in list_of_cards:
            if card['name'] == card_titulo:
                return card['id']

        return False

    def update_card_list(self, id_lista_atual, id_lista_nova, card_titulo):
        id_card = self.get_card_id_by_title(id_lista_atual, card_titulo)
        if not id_card:
            return False
        url = f"https://api.trello.com/1/cards/{id_card}"

        query = {
           'key': TrelloIntegration.authentication['key'],
           'token': TrelloIntegration.authentication['token'],
           'idList': id_lista_nova,
           'dueComplete': 'true'
        }
        response = requests.request(
           "PUT",
           url,
           params=query
        )
        return response

    def show_authentication(self):
        print('>>', TrelloIntegration.authentication)



