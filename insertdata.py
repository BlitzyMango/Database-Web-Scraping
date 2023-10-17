import psycopg2
import config as cfg

def connect():
    return psycopg2.connect(database=cfg.database, user=cfg.user, password=cfg.password, host=cfg.host, port=cfg.port)

def insert_game(game_id, title, developer, publisher, release_date):
    sql = ('INSERT INTO videogames(videogame_id, title, developer, publisher, release_date) '
           'VALUES (%s, %s, %s, %s, %s)')

    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(sql, (game_id, title, developer, publisher, release_date))
        connection.commit()
        cursor.close()
        connection.close()
    except psycopg2.Error as error:
        print('Error occurred:')
        print(error)

def insert_console(console_id, console):
    sql = ('INSERT INTO consoles(c_id, console) VALUES (%s, %s)')

    try:
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(sql, (console_id, console))
        connection.commit()
        cursor.close()
        connection.close()
    except psycopg2.Error as error:
        print('Error occurred:')
        print(error)
