"""@page_scraper Responsavel por definir Scraper e seus metodos."""

import os
import json
import csv
import datetime
from time import strftime, sleep
import requests
import facebook
import psycopg2
from .get_posts import process_posts


class Scraper:
    """Scraper responsável por coletar posts do Facebook."""

    def __init__(self, token):
        """Construtor da classe, recebe token do Facebook como parâmetro."""
        self.token = token
        self.status_code = 400
        self.current_data = ''
        self.file_name = None
        self.actors_list = []
        self.date_list = []
        if not os.path.exists('csv/'):
            os.makedirs('csv/')
        if not os.path.exists('json/'):
            os.makedirs('json/')

    def check_valid_token(self):
        """Verifica se o token disponível é válido."""
        if (self.status_code is not 200):
            url = 'https://graph.facebook.com/v2.12/me?access_token=' \
                  + str(self.token)
            self.status_code = requests.get(url).status_code
        return (self.status_code == 200)

    def set_page(self, page):
        """Escolhe a pagina a ser raspada quando se há varias."""
        self.page = page
        self.file_name = (str(self.page))

    def get_current_page(self):
        """Verifica se uma página foi selecionada."""
        try:
            return self.page
        except Exception:
            return 'Page not set'

    def valid_page(self, page=None):
        """Verifica se uma página selecionada é válida."""
        if page is None:
            page = self.page
        valid_url = 'https://www.facebook.com/' + str(page)
        try:
            valid_status_code = requests.get(valid_url).status_code
        except Exception:
            valid_status_code = 400
        return (valid_status_code == 200)

    def scrape_current_page(self, page=None, feed=False, query=''):
        """Raspa dados de uma página selecionada."""
        if page is not None:
            self.set_page(page)
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        feed_statement = '/feed' if feed else ''
        try:
            post = graph.get_object(
                id=str(self.page) + feed_statement,
                fields=query
            )
            self.current_data = post
            self.current_data['date'] = strftime("%Y-%m-%d")
            # print(self.current_data)
            if 'name' in post.keys():
                return post['name']
            elif 'data' in post.keys():
                return True
        except Exception as inst:
            print(inst)
            return 'Page not defined or bad query structure'

    def write_to_json(self, actor_name=None, file=None):
        """Grava informações da página raspada em um arquivo JSON."""
        if file is None:
            file = self.file_name
        with open(
                'json/' + strftime("%Y-%m-%d") + '/' + file + '.json',
                'w', encoding='utf8'
        ) as data_file:
            data_file.write(
                json.dumps(self.current_data, indent=2, ensure_ascii=False)
            )  # pretty json
        if actor_name is not None:
            self.actors_list.append(actor_name)
        return True

    def get_page_name_and_like(self, page=None):
        """Grava nome e quantidade de likes da página raspada."""
        self.scrape_current_page(page, query='name,fan_count')
        return ([
            self.current_data['name'],
            # self.current_data['fan_count'],
            # self.current_data['id'],
            strftime("%Y-%m-%d")
        ])

    def write_to_csv(self, file_name='scraped'):
        """Grava informações da página raspada em um arquivo CSV."""

        def dict_to_list():
            content = []
            for column in column_names:
                content.append(str(self.current_data[column]))
            return content

        try:
            column_names = self.current_data.keys()
            if set(column_names) == {
                'name', 'id', 'date', 'since_date', 'until_date',
                'fan_count', 'total_posts', 'total_reactions',
                'total_comments', 'total_shares', 'average_reactions',
                'average_comments'
            }:
                column_names = [
                    'name', 'id', 'date', 'since_date', 'until_date',
                    'fan_count', 'total_posts', 'total_reactions',
                    'total_comments', 'total_shares', 'average_reactions',
                    'average_comments'
                ]
            elif set(column_names) == {
                'name', 'id', 'date', 'fan_count', 'total_posts',
                'total_reactions', 'total_comments', 'total_shares',
                'average_reactions', 'average_comments'
            }:
                column_names = [
                    'name', 'id', 'date', 'fan_count', 'total_posts',
                    'total_reactions', 'total_comments', 'total_shares',
                    'average_reactions', 'average_comments'
                ]
            elif set(column_names) == {'name', 'id', 'date', 'fan_count'}:
                column_names = ['name', 'id', 'date', 'fan_count']
        except Exception as inst:
            print(inst)
            return 'No content found.'
        today = strftime("%Y-%m-%d_%Hh")

        # Check if file already exists to append instead of create
        if os.path.exists('csv/{}_{}.csv'.format(file_name, today)):
            content = dict_to_list()
            # Check if content already exists in csv
            with open(
                    'csv/{}_{}.csv'.format(file_name, today), 'r') as csvfile:
                reader = csv.reader(csvfile)
                reader_list = list(reader)
                for row in reader_list:
                    if row == content:
                        return True
            # Write content on CSV because it's not duplicated
            with open(
                    'csv/{}_{}.csv'.format(file_name, today), 'a') as csvfile:
                info = csv.writer(csvfile)
                info.writerow(content)
            return True

        # Create file because file doesn't exist
        with open('csv/{}_{}.csv'.format(file_name, today), 'w') as csvfile:
            info = csv.writer(csvfile)
            content = dict_to_list()
            info.writerow(column_names)
            info.writerow(content)
        return True

    def process_facebook_page_feed_status(
            self, status, total_reaction, total_comments, total_shares
    ):
        """
        Responsável pelo processamento dos dados.

        Sendo eles o total de reações,comentários,compartilhamentos e posts.
        """
        status_id = status['id']

        status_published = datetime.datetime.strptime(
            status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
        # Heroku is 3 hours ahead of Brasilia time
        status_published = status_published + datetime.timedelta(hours=-3)
        status_published = status_published.strftime(
            '%Y-%m-%d %H:%M:%S')  # Converting from the way facebook gives us
        # the created time to a more readable

        # Nested items require chaining dictionary keys.

        num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
        num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
        num_shares = 0 if 'shares' not in status else status['shares']['count']
        total_reaction = total_reaction + num_reactions
        total_comments = total_comments + num_comments
        total_shares = total_shares + num_shares

        return status_id, status_published, num_reactions, num_comments, \
               num_shares, total_reaction, total_comments, total_shares

    def get_data(self, id_statuses, id_posts, fields):
        """Pega as informações brutas retornadas pela GraphAPI"""
        graph = facebook.GraphAPI(access_token=self.token, version="2.12")
        try:
            statuses = graph.get_object(
                id=id_statuses,
                fields=fields
            )
            post_message = graph.get_object(
                id=id_posts,
                fields="message,story"
            )
        except Exception as e:
            print('Erro na busca dos dados ' + str(e) +
                  '\nTentando de novo...')
            sleep(5.0)
            statuses = graph.get_object(
                id=id_statuses,
                fields=fields
            )
            post_message = graph.get_object(
                id=id_posts,
                fields="message,story"
            )
        return (statuses, post_message)

    def get_reactions(self, page=None, since_date=None, until_date=None):
        """Raspa informações da página referentes a reações."""
        if page is None:
            page = self.page
        if not self.valid_page(page):
            return "Page is not valid."
        if since_date is None:
            month = str(int(strftime("%m")) - 1)
            since_date = strftime("%Y-") + month + strftime("-%d")
        if until_date is None:
            until_date = strftime("%Y-%m-%d")
        total_reaction = 0
        total_comments = 0
        total_shares = 0
        total_posts = 0
        has_next_page = True
        num_processed = 0
        after = ''
        after_post = ''
        since = "&since={}".format(since_date) if since_date \
                                                  != '' else ''
        until = "&until={}".format(until_date) if until_date \
                                                  != '' else ''
        time_limit = since + until
        while has_next_page:
            after = '' if after == '' else "&after={}".format(after)
            fields = "fields=message,created_time,type,id," + \
                     "comments.limit(100).summary(total_count),shares," + \
                     "reactions.limit(0).summary(true),link,reactions." + \
                     "type(LIKE).limit(0).summary(total_count).as(like)" + \
                     ",reactions.type(WOW).limit(0).summary(total_count)" + \
                     ".as(wow),reactions.type(SAD).limit(0)." + \
                     "summary(total_count).as(sad),reactions.type(LOVE)" + \
                     ".limit(0).summary(total_count).as(love)," + \
                     "reactions.type(HAHA).limit(0).summary(total_count)" + \
                     ".as(haha),reactions.type(ANGRY).limit(0)." + \
                     "summary(total_count).as(angry)"
            id_statuses = str(self.page) + '/posts?' + after + \
                          '&limit=100' + time_limit
            id_posts = str(self.page) + '/posts?' + after_post + '&limit=100' \
                       + since + until
            statuses, post_message = self.get_data(
                id_statuses, id_posts, fields)
            for status in statuses['data']:
                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = self.process_facebook_page_feed_status(
                        status, total_reaction, total_comments, total_shares
                    )
                    total_reaction = status_data[5]
                    total_comments = status_data[6]
                    total_shares = status_data[7]
                    total_posts += 1
                    if not os.path.exists('json/posts/' + str(self.page)):
                        os.makedirs('json/posts/' + str(self.page))
                    process_posts(
                        self.page, status,
                        post_message['data'][num_processed % 100],
                        status_data[1]
                    )
                num_processed += 1
                if num_processed % 100 == 0:
                    print(
                        "{} Statuses Processed: {}".format(
                            num_processed, datetime.datetime.now()
                        )
                    )
            # if there is no next page, we're done.
            if 'paging' in statuses:
                after = statuses['paging']['cursors']['after']
                after_post = post_message['paging']['cursors']['after']
            else:
                has_next_page = False
        if total_posts != 0:
            average_reaction = total_reaction // total_posts
            average_comments = total_comments // total_posts
        else:
            average_reaction = total_reaction
            average_comments = total_comments
        self.current_data['since_date'] = since_date
        self.current_data['until_date'] = until_date
        self.current_data['total_reactions'] = total_reaction
        self.current_data['total_comments'] = total_comments
        self.current_data['total_shares'] = total_shares
        self.current_data['total_posts'] = total_posts
        self.current_data['average_reactions'] = average_reaction
        self.current_data['average_comments'] = average_comments

    def write_actors_and_date_file(self):
        """Escreve atores e datas no arquivo."""
        data = {'date': [], 'latest': strftime("%Y-%m-%d")}
        actors_dict = {'actors': self.actors_list}
        with open('json/' + 'actors.json', 'w', encoding='utf8') as actor_file:
            actor_file.write(
                json.dumps(actors_dict, indent=2, ensure_ascii=False)
            )
        try:
            date_file = open('json/date.json', 'r+', encoding='utf8')
            data = json.load(date_file)
            data['latest'] = strftime("%Y-%m-%d")
            date_file.seek(0)
            if strftime("%Y-%m-%d") not in data['date']:
                data['date'].append(strftime("%Y-%m-%d"))
            date_file.write(
                json.dumps(data, indent=2, ensure_ascii=False)
            )
        except FileNotFoundError:
            data['date'].append(strftime("%Y-%m-%d"))
            data['latest'] = strftime("%Y-%m-%d")
            with open('json/date.json', 'w', encoding='utf8') as date_file:
                date_file.write(
                    json.dumps(data, indent=2, ensure_ascii=False)
                )

    def call_db(self, actor_name=None, file=None):
        """Responsável pela chamada do banco de dados."""
        """Abre o arquivo JSON criado na função write_to_json"""
        if file is None:
            file = self.file_name
        with open(
                'json/' + strftime("%Y-%m-%d") + '/' + file + '.json',
                'r', encoding='utf8'
        ) as data_file:
            """Carrega o arquivo para a variável data"""
            data = json.load(data_file)
        data['file_name'] = file
        """Seta os parametros para conexão com o banco de dados"""
        params = {
            "host": "ec2-23-23-247-245.compute-1.amazonaws.com",
            "database": "dcut7901ku63t1",
            "user": "outvrxddgqtmwt",
            "password": "e4f2c7675d8bacc541b8e0162d5e023c" +
                        "63ce63df91bcfbeaf9f1a3e803800add"
        }
        """Conecta com o banco"""
        conn = psycopg2.connect(**params)
        """Seta o comando para inserir os dados do arquivo JSON no banco"""
        sql_cmd = """INSERT INTO Facebook(
            file_name, name, fan_count, id, date, since_date,
            until_date, total_reactions, total_comments, total_shares,
            total_posts, average_reactions, average_comments)
            SELECT
                CAST(src.MyJSON->>'file_name' AS TEXT),
                CAST(src.MyJSON->>'name' AS TEXT),
                CAST(src.MyJSON->>'fan_count' AS INTEGER),
                CAST(src.MyJSON->>'id' AS TEXT),
                CAST(src.MyJSON->>'date' AS DATE),
                CAST(src.MyJSON->>'since_date' AS DATE),
                CAST(src.MyJSON->>'until_date' AS DATE),
                CAST(src.MyJSON->>'total_reactions' AS INTEGER),
                CAST(src.MyJSON->>'total_comments' AS INTEGER),
                CAST(src.MyJSON->>'total_shares' AS INTEGER),
                CAST(src.MyJSON->>'total_posts' AS INTEGER),
                CAST(src.MyJSON->>'average_reactions' AS INTEGER),
                CAST(src.MyJSON->>'average_comments' AS INTEGER)
            FROM ( SELECT CAST(%s AS JSONB) AS MyJSON ) src"""

        """Converte o dicionário em um JSON nativo"""
        data_str = json.dumps(data)
        sql_params = (data_str,)
        try:
            """Executa o comando no banco com o JSON nativo"""
            cur = conn.cursor()
            cur.execute(sql_cmd, sql_params)
            conn.commit()
        except Exception as e:
            print('Error ', e)
            raise
        if actor_name is not None:
            self.actors_list.append(actor_name)
        return True
