import pandas as pd
import sys

sys.path.append('/home/dan/PycharmProjects/DissertationProject/db_objects')
sys.path.append('/home/dan/PycharmProjects/DissertationProject')
from db_objects import db
from helper_functions import clear_csv_file, whitespace_remover


db = db.DbRealEstate()
csv_path = '/home/dan/PycharmProjects/DissertationProject/csv_files/brasov_storia.csv'


def insert_csv_to_postgresql(csv_path_string):
    df = pd.read_csv(csv_path, header=None)
    df.columns = ['header_id', 'num_of_rooms', 'surface', 'compartment', 'floor', 'construction_year',
                  'property_type', 'parking_space', 'balcony', 'location', 'price', 'source', 'seller_type',
                  'header_date']
    df = df[df['header_id'].notna()]
    df = df.drop_duplicates(subset=['header_id'])
    df['header_date'] = pd.to_datetime(df['header_date'])
    df[['location_city', 'location_area']] = df['location'].str.split(',', expand=True)
    df['price_value'] = df['price'].str.replace(' ', '').str.extract('(\d+)')
    df['price_currency'] = df['price'].str.replace(' ', '').str.replace('\d+', '')
    df['num_of_rooms'] = pd.to_numeric(df['num_of_rooms'], errors='coerce')
    df['price_value'] = pd.to_numeric(df['price_value'], errors='coerce')
    df['surface'] = pd.to_numeric(df['surface'], errors='coerce')
    df['header_id'] = pd.to_numeric(df['header_id'], errors='coerce', downcast='integer')
    df = df.drop(columns=['price', 'location'])
    whitespace_remover(df)

    db.insert_df_to_postgresql(df)
    clear_csv_file(csv_path)


insert_csv_to_postgresql(csv_path)
