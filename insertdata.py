import cx_Oracle
import config as cfg


def insert_game(game_id, title, developer, publisher, release_date):
    sql = ('insert into videogames(videogame_id, title, developer, publisher, release_date) '
           'values(:videogame_id, :title, :developer, :publisher, :release_date)')

    try:
        # establish a new connection
        with cx_Oracle.connect(cfg.username,
                               cfg.password,
                               cfg.dsn,
                               encoding=cfg.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(
                    sql, [game_id, title, developer, publisher, release_date])
                # commit work
                connection.commit()
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)


def insert_console(console_id, console):
    sql = ('insert into consoles(c_id, console) '
           'values(:c_id, :console)')

    try:
        # establish a new connection
        with cx_Oracle.connect(cfg.username,
                               cfg.password,
                               cfg.dsn,
                               encoding=cfg.encoding) as connection:
            # create a cursor
            with connection.cursor() as cursor:
                # execute the insert statement
                cursor.execute(sql, [console_id, console])
                # commit work
                connection.commit()
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)