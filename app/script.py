from bokeh.palettes import Spectral11, Plasma256, Spectral5
from bokeh.transform import factor_cmap
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from db_objects import db
import pandas as pd
from flask import render_template
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearColorMapper
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def home():
    db_session = db.DbRealEstate()
    pd.set_option('display.max_columns', None)
    stats_table = plot_cluj_statistics_table(db_session)
    general_view_table = plot_general_view_table(db_session)

    script1, div1, cdn_js1 = plot_count_per_source(db_session)
    script2, div2, cdn_js2 = plot_count_per_city(db_session)
    script3, div3, cdn_js3 = plot_avg_price_per_city(db_session)
    script4, div4, cdn_js4 = plot_avg_price_per_rooms_num(db_session)
    script5, div5, cdn_js5 = plot_avg_price_per_location_area(db_session)
    script6, div6, cdn_js6 = plot_avg_price_per_city_per_year(db_session)
    script7, div7, cdn_js7 = plot_avg_price_per_rooms_per_year(db_session)
    return render_template("index.html", tables=[general_view_table.to_html(classes='data'), stats_table.to_html(classes='data')],
                           titles=['index', 'General View', 'Statistics related to Cluj-Napoca'],
                           script1=script1, div1=div1, cdn_js1=cdn_js1, script2=script2, div2=div2, cdn_js2=cdn_js2,
                           script3=script3, div3=div3, cdn_js3=cdn_js3, script4=script4, div4=div4, cdn_js4=cdn_js4,
                           script5=script5, div5=div5, cdn_js5=cdn_js5, script6=script6, div6=div6, cdn_jsn6=cdn_js6,
                           script7=script7, div7=div7, cdn_js7=cdn_js7)


@app.route('/about', methods=("POST", "GET"))
def about():
    return render_template('about.html')


def plot_count_per_source(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)

    df.source = df.source.astype(str)

    group = df.groupby('source')

    source = ColumnDataSource(group)

    source_cmap = factor_cmap('source', palette=Spectral11, factors=sorted(df.source.unique()))

    p = figure(plot_height=650, plot_width=1200, x_range=group, title="Number of records", toolbar_location=None, tools="")

    p.vbar(x='source', top='surface_count', width=1, source=source, line_color=source_cmap, fill_color=source_cmap)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Source (website name)"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    script1, div1 = components(p)
    cdn_js1 = CDN.js_files[0]

    return script1, div1, cdn_js1


def plot_count_per_city(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)

    df.loc[df['location_city'].str.contains('Cluj|cluj|CLUJ', case=False), 'location_city'] = 'Cluj-Napoca'
    df.loc[df['location_city'].str.contains('bucuresti', case=False), 'location_city'] = 'Bucuresti'
    df.loc[df['location_city'].str.contains('timis', case=False), 'location_city'] = 'Timisoara'
    df.loc[df['location_city'].str.contains('brasov', case=False), 'location_city'] = 'Brasov'

    group = df.groupby('location_city')

    source = ColumnDataSource(group)

    source_cmap = factor_cmap('location_city', palette=Spectral11, factors=sorted(df.location_city.unique()))

    p = figure(plot_height=650, plot_width=1200, x_range=group, title="Number of records", toolbar_location=None, tools="")

    p.vbar(x='location_city', top='price_value_count', width=1, source=source, line_color=source_cmap,
           fill_color=source_cmap)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "City/Region"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    script2, div2 = components(p)
    cdn_js2 = CDN.js_files[0]

    return script2, div2, cdn_js2


def plot_avg_price_per_city(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)

    df.loc[df['location_city'].str.contains('Cluj|cluj|CLUJ', case=False), 'location_city'] = 'Cluj-Napoca'
    df.loc[df['location_city'].str.contains('bucuresti', case=False), 'location_city'] = 'Bucuresti'
    df.loc[df['location_city'].str.contains('timis', case=False), 'location_city'] = 'Timisoara'
    df.loc[df['location_city'].str.contains('brasov', case=False), 'location_city'] = 'Brasov'

    group = df.groupby('location_city')

    source = ColumnDataSource(group)

    source_cmap = factor_cmap('location_city', palette=Spectral11, factors=sorted(df.location_city.unique()))

    p = figure(plot_height=650, plot_width=1200, x_range=group, title="Average price", toolbar_location=None, tools="")

    p.vbar(x='location_city', top='price_value_mean', width=1, source=source, line_color=source_cmap, fill_color=source_cmap)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "City/Region"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    script3, div3 = components(p)
    cdn_js3 = CDN.js_files[0]

    return script3, div3, cdn_js3


def plot_avg_price_per_rooms_num(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)
    df_cluj = df[df.location_city.str.contains('Cluj', case=False)]
    df_cluj = df_cluj.dropna(axis=0, subset=['surface'])
    df_cluj = df_cluj.dropna(axis=0, subset=['price_value'])
    df_cluj.num_of_rooms = df_cluj.num_of_rooms.astype(str)
    group = df_cluj.groupby('surface')
    source = ColumnDataSource(group)

    p = figure(plot_width=1200, plot_height=650)

    p.circle('surface', 'price_value_mean', size=10, color="navy", alpha=0.5, source=source)
    p.xaxis.axis_label = "Surface (square meters)"
    p.yaxis.axis_label = "Average price"
    script4, div4 = components(p)
    cdn_js4 = CDN.js_files[0]

    return script4, div4, cdn_js4


def plot_avg_price_per_location_area(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)
    df_cluj = df[df.location_city.str.contains('Cluj', case=False)]
    df_cluj = df[df.location_area.str.contains(
        'Andrei Muresanu|Bulgaria|Buna Ziua|Centru|Manastur|Europa|gheorgheni|faget|grigorescu|gruia|iris|intre lacuri|'
        'marasti|someseni|sopor|zorilor|dambul rotund|becas|borhanci',
        case=False)]
    group = df_cluj.groupby('location_area')
    source = ColumnDataSource(group)

    source_cmap = factor_cmap('location_area', palette=Plasma256, factors=sorted(df_cluj.location_area.unique()))

    p = figure(plot_height=650, plot_width=1200, x_range=group, title="Average price", toolbar_location=None, tools="")

    p.vbar(x='location_area', top='price_value_mean', width=1, source=source, line_color=source_cmap,
           fill_color=source_cmap)

    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Location areas (Cluj-Napoca)"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    script5, div5 = components(p)
    cdn_js5 = CDN.js_files[0]

    return script5, div5, cdn_js5


def plot_avg_price_per_city_per_year(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)
    df = df.dropna(axis=0, subset=['header_date'])
    df.loc[df['location_city'].str.contains('Cluj|cluj|CLUJ', case=False), 'location_city'] = 'Cluj-Napoca'
    df.loc[df['location_city'].str.contains('bucuresti', case=False), 'location_city'] = 'Bucuresti'
    df.loc[df['location_city'].str.contains('timis', case=False), 'location_city'] = 'Timisoara'
    df.loc[df['location_city'].str.contains('brasov', case=False), 'location_city'] = 'Brasov'

    df.location_city = df.location_city.astype(str)
    df.header_date = pd.to_datetime(df['header_date'], format='%Y-%m-%d').dt.year
    df.header_date = df.header_date.astype(str)

    group = df.groupby(by=['location_city', 'header_date'])

    index_cmap = factor_cmap('location_city_header_date', palette=Spectral5, factors=sorted(df.location_city.unique()),
                             end=1)

    p = figure(plot_width=1200, plot_height=650, title="Pretul mediu al anunturilor",
               x_range=group, toolbar_location=None,
               tooltips=[("Price", "@price_value_mean"), ("location, date", "@location_city_header_date")])

    p.vbar(x='location_city_header_date', top='price_value_mean', width=1, source=group,
           line_color="white", fill_color=index_cmap)

    p.y_range.start = 0
    p.x_range.range_padding = 0.05
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Anul postarii anunturilor per Oras"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    script6, div6 = components(p)
    cdn_js6 = CDN.js_files[0]

    return script6, div6, cdn_js6


def plot_avg_price_per_rooms_per_year(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)
    df = df.dropna(axis=0, subset=['header_date'])
    df.loc[df['location_city'].str.contains('Cluj|cluj|CLUJ', case=False), 'location_city'] = 'Cluj-Napoca'
    df.loc[df['location_city'].str.contains('bucuresti', case=False), 'location_city'] = 'Bucuresti'
    df.loc[df['location_city'].str.contains('timis', case=False), 'location_city'] = 'Timisoara'
    df.loc[df['location_city'].str.contains('brasov', case=False), 'location_city'] = 'Brasov'
    df = df[df.num_of_rooms <= 4]

    df.location_city = df.location_city.astype(str)
    df.num_of_rooms = df.num_of_rooms.astype(str)
    df.header_date = df.header_date.astype(str)

    group = df.groupby(by=['location_city', 'num_of_rooms'])

    index_cmap = factor_cmap('location_city_num_of_rooms', palette=Spectral5, factors=sorted(df.location_city.unique()),
                             end=1)

    p = figure(plot_width=1200, plot_height=650, title="Pretul mediu al anunturilor",
               x_range=group, toolbar_location=None,
               tooltips=[("Price", "@price_value_mean"), ("location, num_rooms", "@location_city_num_of_rooms")])

    p.vbar(x='location_city_num_of_rooms', top='price_value_mean', width=1, source=group,
           line_color="white", fill_color=index_cmap)

    p.y_range.start = 0
    p.x_range.range_padding = 0.05
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = "Numarul de camere al apartamentelor per Oras"
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    script7, div7 = components(p)
    cdn_js7 = CDN.js_files[0]

    return script7, div7, cdn_js7


def plot_cluj_statistics_table(db_session):
    df = pd.read_sql_table('scrapped_real_estate', db_session.engine)
    df_cluj = df[df.location_city.str.contains('Cluj', case=False)]
    include = ['object', 'float', 'int']
    describe = df_cluj.describe(include=include)
    return describe


def plot_general_view_table(db_session):
    last_rows = db_session.get_last_ten_rows()
    last_rows_df = pd.DataFrame(last_rows)

    return last_rows_df


if __name__ == "__main__":
    app.run(debug=True)
