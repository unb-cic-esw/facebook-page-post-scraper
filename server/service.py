import json
import psycopg2


class DBService:

    def __init__(self):
        self.params = {
            "host": "ec2-23-23-247-245.compute-1.amazonaws.com",
            "database": "dcut7901ku63t1",
            "user": "outvrxddgqtmwt",
            "password": "e4f2c7675d8bacc541b8e0162d5e023c63ce" +
            "63df91bcfbeaf9f1a3e803800add"
        }
        self.conn = psycopg2.connect(**self.params)

    def get_actors_from_db(self):
        """
        Coleta os atores no banco de dados para vizualiação web
        """
        sql_cmd = "SELECT DISTINCT file_name FROM Facebook"
        cur = self.conn.cursor()
        cur.execute(sql_cmd)
        self.conn.commit()
        actors = {'actors': []}
        actors_tuple = cur.fetchall()
        actors_list = []
        for row in actors_tuple:
            actors_list.append(row[0])
        actors['actors'] = actors_list
        actors = json.dumps(
            actors, indent=2, ensure_ascii=False
        )
        return actors

    def get_basic_actor_data(self, actor, date):
        """
        Coleta no banco de dados as informações sobre o ator
        de acordo com a data especificada
        """
        actor_dict = {}
        cur = self.conn.cursor()
        cur.execute(
            """SELECT DISTINCT * FROM Facebook
               WHERE file_name=%s AND date=%s""", (str(actor), str(date))
        )
        self.conn.commit()
        actor_tuple = cur.fetchall()
        actor_dict['name'] = actor_tuple[0][0]
        actor_dict['fan_count'] = actor_tuple[0][1]
        actor_dict['id'] = actor_tuple[0][2]
        actor_dict['date'] = actor_tuple[0][3]
        actor_dict['since_date'] = actor_tuple[0][4]
        actor_dict['until_date'] = actor_tuple[0][5]
        actor_dict['total_reactions'] = actor_tuple[0][6]
        actor_dict['total_comments'] = actor_tuple[0][7]
        actor_dict['total_shares'] = actor_tuple[0][8]
        actor_dict['total_posts'] = actor_tuple[0][9]
        actor_dict['average_reactions'] = actor_tuple[0][10]
        actor_dict['average_comments'] = actor_tuple[0][11]
        actor = json.dumps(
            actor_dict, indent=2, ensure_ascii=True, default=str
        )
        return actor

    def get_all_date(self):
        """
        Coleta no banco de dados as datas para vizualização web
        """
        date_dict = {'date': []}
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT date FROM Facebook")
        date_tuple = cur.fetchall()
        cur.execute("SELECT MAX(date) FROM Facebook")
        latest = cur.fetchall()
        self.conn.commit()
        for row in date_tuple:
            date_dict['date'].append(row[0])
        date_dict['latest'] = latest[0][0]
        date = json.dumps(
            date_dict, indent=2, ensure_ascii=False, default=str
        )
        return date


if __name__ == '__main__':
    dbs = DBService()
    dbs.get_basic_actor_data(actor='omercadopopular', date='2018-06-06')
    dbs.get_all_date()
