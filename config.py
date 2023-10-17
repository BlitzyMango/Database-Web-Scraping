# PostgreSQL config settings (THE TABLES BELOW NEED TO BE MADE 
# BEFOREHAND IN videogame_database)
"""

CREATE TABLE consoles (
    c_id VARCHAR(10) PRIMARY KEY,
    console VARCHAR(255)
    );
    
    
CREATE TABLE videogames (
    videogame_id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(255),
    developer INTEGER,
    publisher VARCHAR(255),
    release_date DATE
    );
    
"""
database = 'videogame_database'
user = 'scraper'
password = 'password'
host = 'localhost'
port = '5432'
