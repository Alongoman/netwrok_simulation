# Alon Goldmann 312592173
# Peleg Goldberger 206173585
#######################################################################################################################
#Exercise 6
#######################################################################################################################
import requests
from bs4 import BeautifulSoup

def get_ynet_page():
    url = "https://www.ynet.co.il/"
    page = requests.get(url)
    if page:
        return page
    else:
        print("couldn't find page "+url)
        exit(1)

def get_nyt_page():
    url = "https://www.nytimes.com/"
    page = requests.get(url)
    if page:
        return page
    else:
        print("couldn't find page "+url)
        exit(1)

def get_heb_text(text):
    return text[::-1]

def save_ynet_headlines(save_list,headlines):
    for elem in headlines:
        title = elem.find(class_="")
        if title is None:
            continue
        title_txt = title.get_text()
        if len(title_txt) <= 0 or title_txt is None:
            continue
        title_heb_txt = get_heb_text(title_txt)
        save_list.append(title_heb_txt)

def save_nyt_headlines(save_list,headlines):
    for elem in headlines:
        title_txt = elem.get_text()
        if len(title_txt) <= 0 or title_txt is None:
            continue
        save_list.append(title_txt)

def get_ynet_headlines():
    page = get_ynet_page()
    headlines = []
    soup = BeautifulSoup(page.content,"html.parser")
    normal_title = soup.find_all(class_="slotTitle")
    medium_title = soup.find_all(class_="slotTitle medium")
    small_title = soup.find_all(class_="slotTitle small")
    save_ynet_headlines(headlines,normal_title)
    save_ynet_headlines(headlines,medium_title)
    save_ynet_headlines(headlines,small_title)
    return headlines

def get_nyt_headlines():
    page = get_nyt_page()
    headlines = []
    soup = BeautifulSoup(page.content,"html.parser")
    title = soup.find_all(class_="css-jglldk e1lsht870")
    save_nyt_headlines(headlines,title)
    return headlines

if __name__ == "__main__":
    nyt_headlines = get_nyt_headlines()
    print("NYT headlines")
    for title in nyt_headlines:
        print(title)

    ynet_headlines = get_ynet_headlines()
    print("YNET ",end="")
    print(get_heb_text("כותרות של"))
    for title in ynet_headlines:
        print(title)