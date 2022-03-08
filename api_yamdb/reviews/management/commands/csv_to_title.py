from django.core.management.base import BaseCommand # , no_translations
import sqlite3
import csv

    
def import_one_file_csv_to_sqlite():
    conn = sqlite3.connect('../db.sqlite2') 
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
    conn.close() 


# @no_translations
class Command(BaseCommand):
    help = 'Creates data base from CSV files'

    def handle(self, *args, **options):
        import_one_file_csv_to_sqlite()
