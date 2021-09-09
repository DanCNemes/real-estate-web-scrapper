import sys
import pandas as pd
sys.path.append('/home/dan/PycharmProjects/DissertationProject/db_objects')
sys.path.append('/home/dan/PycharmProjects/DissertationProject')
from db_objects import db
from helper_functions import clear_csv_file, whitespace_remover


db = db.DbRealEstate()
csv_path = '/home/dan/PycharmProjects/DissertationProject/csv_files/cluj_imobiliare.csv'


def insert_csv_to_postgresql(csv_path_string):
    df = pd.read_csv(csv_path, header=None)
    df.columns = ['header_id', 'num_of_rooms', 'surface', 'compartment', 'floor', 'construction_year',
                  'property_type', 'parking_space', 'balcony', 'location', 'price', 'source', 'seller_type',
                  'header_date']
    df = df.drop_duplicates(subset=['header_id'])
    df[['location_city', 'location_area']] = df['location'].str.replace('\n', '').str.replace('\r', '').str.split(',',
                                                                                                                  expand=True)
    df[['price_value', 'price_currency']] = df['price'].str.split(' ', expand=True)
    df['construction_year'] = pd.to_numeric(df['construction_year'], errors='coerce')
    df['location_area'] = df['location_area'].str.replace('zona', '').str.replace(' - HartaVezi harta', '')
    df['surface'] = df['surface'].str.extract('(\d+)')
    df['header_date'] = pd.to_datetime(df['header_date'])
    df = df.drop(columns=['price', 'location'])
    whitespace_remover(df)

    db.insert_df_to_postgresql(df)
    clear_csv_file(csv_path)


insert_csv_to_postgresql(csv_path)
