from bs4 import BeautifulSoup
import requests
url = "https://gist.github.com/amnrzv/9a701f419ad004e066e2d6007dae40ad"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
td_elements = soup.find_all("td", class_="blob-code blob-code-inner js-file-line")
pos_list = []
pos_dict2 = {}
for pos in td_elements:
    element = pos.get_text(strip=True)
    if element != "POS tag list:":
        pos_list.append(element)
        add_me = element.split('\t', 1)
        if len(add_me) == 2:
            pos_dict2[add_me[0]] = add_me[1]

# print(pos_dict2)
