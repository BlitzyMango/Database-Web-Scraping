import requests
from bs4 import BeautifulSoup
import re
from dateutil.parser import parse
import insertdata as ins
from random import randint


# This function extracts the subdirectories for each game's wiki page
def scrape_game_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract video game title URLs from the 'td > i > a' structure
    video_game_urls1 = [a['href'] for a in soup.select('td > i > a') if a['href'].startswith('/wiki/')]

    # Extract video game title URLs from the 'td > a:has(> i)' structure
    video_game_urls2 = [a['href'] for a in soup.select('td > a:has(> i)') if a['href'].startswith('/wiki/')]

    # Combine the lists and return
    return video_game_urls1 + video_game_urls2


# This is a function for scrape_game(), used to extract the text in HTML tag(s)
def text_scrape(source, tag1):
    try:
        scraped_text = []
        div = source.find('div', class_="pi-data-value pi-font")
        for i in div.find_all(tag1):
            text = re.sub(r'\[.*?\]', '', i.text)
            if text != '':
                scraped_text.append(text)

        if len(scraped_text) == 0:
            scraped_text.append(div.text)

        return scraped_text
    except:
        return ''
    

# This is a function that scrapes the data from each individual game using their wiki page
def scrape_game(url):
    # Access the website of the specific game
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract the Game Title
    game_title = soup.find('h1', class_="page-header__title").text.strip('\n\t')

    # Find the Developer(s)
    try:
        dev = soup.find("div", attrs={"data-source": "developer"})
        game_developers = text_scrape(dev, 'a')
    except:
        game_developers = [None]

    # Find the Publisher(s)
    try:
        pub = soup.find("div", attrs={"data-source": "publisher"})
        game_publishers = text_scrape(pub, 'a')
    except:
        game_publishers = [None]
        

    # Find the Release Date(s)
    release_dates = []
    try:
        rel = soup.find("div", attrs={"data-source": "released"})
        rel_value = rel.find('div', class_="pi-data-value pi-font")
        
        if rel_value:
            for small in rel_value.find_all('small'):
                release_text = re.sub(r'\[.*?\]', '', small.next_sibling.text)
                if release_text != '':
                    try:
                        release_dates.append(parse(release_text, fuzzy=False))
                    except ValueError:
                        # print("Not a valid date")
                        pass

            if len(release_dates) == 0:
                release_text = re.sub(r'\[.*?\]', '', rel_value.text)
                try:
                    release_dates.append(parse(release_text, fuzzy=False))
                except ValueError:
                    # print('Not a valid date')
                    pass
        # Find the earliest release date
        oldest_date = min(release_dates)
    except:
        oldest_date = None

    # Find the Platform(s)
    try:
        plat = soup.find("div", attrs={"data-source": "platforms"})
        game_platforms = text_scrape(plat, 'a')
    except:
        game_platforms = [None]

    return game_title, game_developers, game_publishers, oldest_date, game_platforms


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1

    return randint(range_start, range_end)

def scrape_list_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # Extract <a> tags with 'List of' in their text
    list_links = [a['href'] for a in soup.find_all('a') if 'List of' in a.get_text()]

    return list_links


if __name__ == '__main__':
    domain = "https://sonic.fandom.com"
    game_list_subdir = "/wiki/Lists_of_games"
    
    subdirectory_list = []
    list_links = scrape_list_links(domain + game_list_subdir)
    for list_link in list_links:
        subdirectory_list.extend(scrape_game_links(domain + list_link))

    gID_list = []
    cID_list = []
    consoles = []
    for subdirectory in subdirectory_list:
        t, developers, publishers, release_date, platforms = scrape_game(
            domain + subdirectory)
        title = re.sub(' +', ' ', t)
        
        if publishers != '' and publishers[0] is not None:
            publisher = re.sub(' +', ' ', publishers[0])
        else:
            publisher = ''

        game_id = 'g' + str(random_with_N_digits(5))
        while (1):
            if game_id not in gID_list:
                gID_list.append(game_id)
                break
            else:
                game_id = 'g' + str(random_with_N_digits(5))

        for console in platforms:
            if console not in consoles:
                consoles.append(console)
                console_id = 'c' + str(random_with_N_digits(5))

                while 1:
                    if console_id not in cID_list:
                        cID_list.append(console_id)
                        break
                    else:
                        console_id = 'c' + str(random_with_N_digits(5))
                ins.insert_console(console_id, console)
            else:
                continue
        
        if developers != '' and developers[0] is not None:
            print(title + '\n' + developers[0] + '\n' + publisher + '\n' + str(release_date) + '\n')
            ins.insert_game(game_id, title, 1, publisher, release_date)
        else:
            print(title + '\n' + publisher + '\n' + str(release_date) + '\n')
            ins.insert_game(game_id, title, 0, publisher, release_date)
        print(domain+subdirectory)
        print('\n')
