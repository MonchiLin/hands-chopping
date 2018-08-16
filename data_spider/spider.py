import re

import gevent
import grequests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


from data_spider.model import Game,Price
from config import Config

session = grequests.Session()



def get_connection(config):
    # pool = redis.ConnectionPool(host=config.host, port=config.port, decode_responses=True)
    # return redis.Redis(connection_pool=pool)
    return create_engine(config.sqlite)


def get_data(link, config):
    price_number = None

    result = session.get(config.baseUrl + link["link"], headers=config.headers)
    soup = BeautifulSoup(result.text, "html5lib")
    body = soup.select("div.grid-cell__body")

    for content in body:
        info = content.find("a")
        price = content.select_one("h3.price-display__price")
        if price is None or price.text == "免费":
            # content.select_one("h3.price-display__price--is-plus-exclusive")
            price_number = 0
        else:
            prue_price = re.findall(r"\d+\.?\d*", price.text)
            price_number = float(''.join(prue_price))

        name = info.find("div").text
        number = re.split("/", info.attrs["href"])[-1]
        config.games.append({'id': number, 'name': name, "price": price_number})

        game_temp = Game(name, number, link['link'])
        price_temp = Price(price_number)
        game_temp.gama_price.append(price_temp)
        config.db.session.add(game_temp)
        config.db.session.commit()


def rua():
    pool = gevent.pool.Pool(20)
    config = Config()
    result = session.get(config.baseUrl, headers=config.headers)
    soup = BeautifulSoup(result.text, "html5lib")
    config.init_url(soup)
    threads = []
    for link in config.links:
        threads.append(pool.spawn(get_data, link, config))

    gevent.joinall(threads)



if __name__ == '__main__':
    rua()

# scheduler = BlockingScheduler()
# scheduler.add_job(rua, 'interval', seconds=3)
# scheduler.start()
