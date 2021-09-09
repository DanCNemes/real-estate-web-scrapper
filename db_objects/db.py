from sqlalchemy import *
from db_objects.config import host, port, database, user, password
from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DbRealEstate:
    def __init__(self):
        self.conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(self.conn_str)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.base = declarative_base()
        self.metadata = MetaData(self.engine)

        self.scrapped_real_estate = Table('scrapped_real_estate', self.metadata,
                                Column('header_id', String, primary_key=True),
                                Column('num_of_rooms', String),
                                Column('surface', String),
                                Column('compartment', String),
                                Column('floor', String),
                                Column('construction_year', String),
                                Column('property_type', String),
                                Column('parking_space', String),
                                Column('balcony', String),
                                Column('location_city', String),
                                Column('price_value', String),
                                Column('source', String),
                                Column('seller_type', String),
                                Column('header_date', String),
                                Column('location_area', String),
                                Column('price_currency', String))

    def header_id_exists(self, header_id):
        header_exists = self.session.query(self.session.query(self.scrapped_real_estate).
                                           filter_by(header_id=header_id).exists()).scalar()

        return header_exists

    def insert_df_to_postgresql(self, df):
        df.to_sql(
            'scrapped_real_estate',
            self.engine,
            index=False,
            if_exists='append'  # if the table already exists, append this data
        )

    def get_last_ten_rows(self):
        query = self.session.query(self.scrapped_real_estate).filter(self.scrapped_real_estate.columns.
                header_date.isnot(None)).order_by(self.scrapped_real_estate.columns.header_date.desc()).limit(10)

        return query
