from django.core.management.base import BaseCommand # , no_translations
import sqlite3
import csv

    
def import_files_csv_to_sqlite():
    conn = sqlite3.connect('../db.sqlite3') 
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        role TEXT,
        bio TEXT,
        first_name TEXT,
        last_name TEXT)'''
    )
    with open('../api_yamdb/static/data/users.csv', 'r', encoding='utf-8') as f_open_csv:
        rows = csv.reader(f_open_csv, delimiter=",")
        first_row = next(rows)
        for row in rows:
            c.execute('INSERT OR IGNORE INTO user VALUES (?, ?, ?, ?, ?, ?, ?)', row)       
    conn.commit()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY,
        name TEXT,
        slug TEXT) '''
    )
    with open('../api_yamdb/static/data/category.csv', 'r', encoding='utf-8') as f_open_csv:
        rows = csv.reader(f_open_csv, delimiter=",")
        first_row = next(rows)
        for row in rows:
            c.execute('INSERT OR IGNORE INTO category VALUES (?, ?, ?)', row)       
    conn.commit()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS genre (
        id INTEGER PRIMARY KEY,
        name TEXT,
        slug TEXT) '''
    )
    with open('../api_yamdb/static/data/genre.csv', 'r', encoding='utf-8') as f_open_csv:
        rows = csv.reader(f_open_csv, delimiter=",")
        first_row = next(rows)
        for row in rows:
            c.execute('INSERT OR IGNORE INTO genre VALUES (?, ?, ?)', row)       
    conn.commit()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS title (
        id INTEGER PRIMARY KEY,
        name TEXT,
        year INTEGER,
        category INTEGER,
        FOREIGN KEY(category) REFERENCES category(id))'''
    )
    with open('../api_yamdb/static/data/titles.csv', 'r', encoding='utf-8') as f_open_csv:
        rows = csv.reader(f_open_csv, delimiter=",")
        first_row = next(rows)
        for row in rows:
            c.execute('INSERT OR IGNORE INTO title VALUES (?, ?, ?, ?)', row)       
    conn.commit()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS genre_title (
        id INTEGER PRIMARY KEY,
        title_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY(title_id) REFERENCES title(id),
        FOREIGN KEY(genre_id) REFERENCES genre(id)) '''
    )
    with open('../api_yamdb/static/data/genre_title.csv', 'r', encoding='utf-8') as f_open_csv:
        rows = csv.reader(f_open_csv, delimiter=",")
        first_row = next(rows)
        for row in rows:
            c.execute('INSERT OR IGNORE INTO genre_title VALUES (?, ?, ?)', row)       
    conn.commit()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS review (
        id INTEGER PRIMARY KEY,
        title_id INTEGER,
        text TEXT,
        author TEXT,
        score INTEGER,
        pub_date TEXT,
        FOREIGN KEY(title_id) REFERENCES title(id),
        FOREIGN KEY(author) REFERENCES author(id))'''
    )
    with open('../api_yamdb/static/data/review.csv', 'r', encoding='utf-8') as f_open_csv:
        rows = csv.reader(f_open_csv, delimiter=",")
        first_row = next(rows)
        for row in rows:
            c.execute('INSERT OR IGNORE INTO review VALUES (?, ?, ?, ?, ?, ?)', row)       
    conn.commit()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS comment (
        id INTEGER PRIMARY KEY,
        review_id INTEGER,
        text TEXT,
        author TEXT,
        pub_date TEXT,
        FOREIGN KEY(review_id) REFERENCES review(id),
        FOREIGN KEY(author) REFERENCES author(id))'''
    )
    with open('../api_yamdb/static/data/comments.csv', 'r', encoding='utf-8') as f_open_csv:
        rows = csv.reader(f_open_csv, delimiter=",")
        first_row = next(rows)
        for row in rows:
            c.execute('INSERT OR IGNORE INTO comment VALUES (?, ?, ?, ?, ?)', row)       
    conn.commit()
    conn.close() 


# @no_translations
class Command(BaseCommand):
    help = 'Creates data base from CSV files'

    def handle(self, *args, **options):
        import_files_csv_to_sqlite()