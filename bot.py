#!/usr/bin/env python3

from trabalhabrasil import TrabalhaBrasilBOT
import json
import time
import logging
import sqlite3
import sys

def main():
    try:
        MAX_SECONDS_RESTART = 5 * 60

        logging.basicConfig(level = logging.ERROR, filename = 'logs/bot.log', format = "%(asctime)s - %(levelname)s - %(message)s")

        con = sqlite3.connect("models/history")

        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY,
            url VARCHAR(512) NOT NULL UNIQUE,
            visited DATETIME DEFAULT CURRENT_TIMESTAMP
        );""")

        if sys.argv[-1] == 'LOCAL':
            input_file = 'local_params.json'
        else:
            input_file = 'params.json'

        with open(input_file, 'r') as f:
            params = json.load(f)

        cpf = params.get('cpf')
        data_nascimento = params.get('data_nascimento')
        keywords = params.get('keywords')
        location = params.get('location')
        home_office = params.get('home-office')
        ordenacao = params.get('ordenacao')

        bot = TrabalhaBrasilBOT(cpf, data_nascimento, home_office = home_office, ordenacao = ordenacao)

        countPages = bot.countSearchPages(keywords, location)
    
        print(f'foram encontradas {countPages} páginas')
        
        last_time = time.time()

        collected = []

        for page in range(1, countPages + 1):
            jobs = bot.search(keywords, page, location)

            for job in jobs:
                
                cur_time = time.time()

                if cur_time - last_time >= MAX_SECONDS_RESTART:
                    print('RESTART')
                    bot.restart()
                    last_time = cur_time
                    
                cur.execute("SELECT 1 from history WHERE url = ?", (job, ))

                results = cur.fetchall()

                if len(results):
                    print(f'o {job} já está no histórico de candidaturas')
                    continue

                if bot.apply(job):
                    cur.execute("INSERT INTO history(id, url) VALUES (NULL, ?)", (job, ))

    except Exception as ex:
        logging.error(f'error when running bot: {ex}')

    finally:
        bot.quit()
        con.commit()
        con.close()

if __name__ == '__main__':
    main()
