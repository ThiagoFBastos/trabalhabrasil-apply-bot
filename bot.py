#!/usr/bin/env python3

from trabalhabrasil import TrabalhaBrasil
import json
import time
import logging
import sqlite3

try:
    logging.basicConfig(level = logging.ERROR, filename = 'logs/bot.log', format = "%(asctime)s - %(levelname)s - %(message)s")

    con = sqlite3.connect("models/history")
    
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY,
        url VARCHAR(512) NOT NULL UNIQUE,
        visited DATETIME DEFAULT CURRENT_TIMESTAMP
    );""")

    with open('params.json', 'r') as f:
        params = json.load(f)

    cpf = params.get('cpf')
    data_nascimento = params.get('data_nascimento')
    keywords = params.get('keywords')
    location = params.get('location')

    bot = TrabalhaBrasil(cpf, data_nascimento)

    bot.login()

    countPages = bot.countSearchPages(keywords, location)

    for page in range(1, countPages + 1):
        jobs = bot.search(keywords, page, location)

        for job in jobs:
            cur.execute("SELECT 1 from history WHERE url = ?", (job, ))

            results = cur.fetchall()

            if len(results):
                continue

            if bot.apply(job):
                cur.execute("INSERT INTO history(id, url) VALUES (NULL, ?)", (job, ))
            
            time.sleep(1)

except Exception as ex:
    logging.error(f'error when execute bot: {ex}')

finally:
    bot.quit()
    con.commit()
    con.close()
