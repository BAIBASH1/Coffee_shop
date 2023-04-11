import json
import requests
from dotenv import load_dotenv
import os
from geopy import distance
import folium
from flask import Flask


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places =\
        response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance(coffeeshop):
    return coffeeshop['distance']


def create_map():
    with open('index.html', 'r') as file:
        return file.read()


def collect_necessary_inf(coffeeshops, user_coords):
    coffeeshops_necessary_inf = []
    for coffeeshop in coffeeshops:
        coffee_coords = coffeeshop['geoData']['coordinates'][::-1]
        distance_to_coffeeshop = distance.distance(coffee_coords, user_coords)
        coffeeshops_necessary_inf.append({
            'title': coffeeshop['Name'],
            'distance': distance_to_coffeeshop,
            'latitude': coffeeshop['geoData']['coordinates'][1],
            'longitude': coffeeshop['geoData']['coordinates'][0]
        }
        )
    return coffeeshops_necessary_inf


def add_maker(coords, map):
    tooltip = "Click me!"
    for coord in coords[:5]:
        folium.Marker(
            [coord['latitude'], coord['longitude']],
            popup="<i>Mt. Hood Meadows</i>",
            tooltip=tooltip
        ).add_to(map)
    return map


def main():
    load_dotenv()
    apikey = os.environ['YANDEX_APIKEY']
    address = input('Введите ваш адрес: ')
    user_coords = fetch_coordinates(apikey, address)[::-1]

    with open('coffee.json', 'r', encoding='CP1251') as file:
        coffeeshops = json.load(file)

    coffeeshops_necessary_inf = collect_necessary_inf(
        coffeeshops,
        user_coords
    )
    coffeeshops_sorted_by_distance = sorted(
        coffeeshops_necessary_inf,
        key=get_distance
    )
    map = folium.Map(
        location=[*user_coords],
        zoom_start=14,
        tiles="Stamen Terrain"
    )
    map_with_maker = add_maker(coffeeshops_sorted_by_distance[:5], map)

    map_with_maker.save('index.html')
    app = Flask(__name__)
    app.add_url_rule('/', 'hello', create_map)
    app.run('0.0.0.0')


if __name__ == '__main__':
    main()
