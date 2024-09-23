import requests
from bs4 import BeautifulSoup
import re

def pegar_conteudo_pagina(url):
    try:
        print(f"Fazendo requisição para: {url}")
        resposta = requests.get(url)
        if resposta.status_code == 200:
            print(f"Sucesso ao acessar a página: {url}")
            return resposta.text
        else:
            print(f"Erro ao acessar a página: {resposta.status_code}")
            return None
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

def extrair_links(html):
    sopa = BeautifulSoup(html, 'html.parser')
    padrao_url = re.compile(r'(https://riodejaneirosecreto.com/[a-zA-Z0-9-]+/)')

    print("Extraindo links das tags <script> e <a>...")

    links = []
    for script in sopa.find_all('script'):
        if script.string:
            links_encontrados = padrao_url.findall(script.string)
            links.extend(links_encontrados) 
        if 'src' in script.attrs:
            links_encontrados = padrao_url.findall(script['src'])
            links.extend(links_encontrados)

    for a in sopa.find_all('a', href=True):
        links_encontrados = padrao_url.findall(a['href'])
        links.extend(links_encontrados)

    print(f"Total de links encontrados: {len(links)}")
    return remover_links_duplicados(links)

def remover_links_duplicados(links):
    links_unicos = list(set(links))
    print(f"Total de links únicos: {len(links_unicos)}")
    return links_unicos

if __name__ == '__main__':
    url = 'https://riodejaneirosecreto.com/comer-e-beber/'
    conteudo_pagina = pegar_conteudo_pagina(url)

    if conteudo_pagina:
        links = extrair_links(conteudo_pagina)
        if links:
            print("Links:")
            for link in links:
                print(link)
        else:
            print("Nenhum link encontrado.")
