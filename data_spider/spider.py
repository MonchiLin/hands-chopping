import re

import gevent
import grequests
from bs4 import BeautifulSoup
from pypinyin import pinyin, Style
from sqlalchemy import create_engine

from config import Config
from data_spider.model import Game, Price

session = grequests.Session()


def is_include_zh(s):
    for c in s:
        if not ('\u4e00' <= c <= '\u9fa5'):
            return False
    return True


def clear_text(text):
    return re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+'", '', text)


def get_connection(config):
    # pool = redis.ConnectionPool(host=config.host, port=config.port, decode_responses=True)
    # return redis.Redis(connection_pool=pool)
    return create_engine(config.sqlite)


def get_data(link, config):
    db = config.db

    result = session.get(config.baseUrl + link["link"], headers=config.headers)
    soup = BeautifulSoup(result.text, "html5lib")

    end_btn = soup.select("a.paginator-control__end")

    if len(end_btn) == 0:
        fetch(db, soup, config, link)
    else:
        end = re.split("/", end_btn[0].attrs["href"])[-1]
        for i in range(int(end)):
            url = config.baseUrl + link["link"] + '/' + str(i)
            res = session.get(url, headers=config.headers)
            content = BeautifulSoup(res.text, "html5lib")
            fetch(db, content, config, link)


def fetch(db, soup, config, link):
    price_number = None
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

        name = info.find("div").text.strip()
        number = re.split("/", info.attrs["href"])[-1]
        existed = Game.query.filter_by(game_number=number).first()

        if existed is None:
            game_temp = Game(name, number, info['href'])
            price_temp = Price(price_number)
            game_temp.game_price.append(price_temp)

            if is_include_zh(name[:4]):
                prue_name = clear_text(name)
                p = pinyin(prue_name)

                jianpin = pinyin(prue_name, style=Style.FIRST_LETTER)
                quanpin = pinyin(prue_name, style=Style.NORMAL)
                game_temp.game_jianpin = ''.join([j[0] for j in jianpin])
                game_temp.game_quanpin = ''.join([j[0] for j in quanpin])

            db.session.add(game_temp)
            db.session.commit()
        else:
            price_temp = Price(price_number)
            price_temp.game_id = existed.id
            db.session.add(price_temp)
            db.session.commit()


def rua():
    pool = gevent.pool.Pool(20)
    config = Config()
    result = session.get(config.baseUrl, headers=config.headers)
    soup = BeautifulSoup(result.text, "html5lib")
    config.init_url(soup)
    threads = []
    for link in config.links:
        threads.append(pool.spawn(get_data, link, config))
        # get_data(link, config)

    gevent.joinall(threads)
    print("rua!")


rua()

# sched = BlockingScheduler()
# sched.add_job(rua, 'interval', minutes=5)
# sched.start()
