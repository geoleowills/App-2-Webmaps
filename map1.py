# tiles = "Mapbox Bright"
# instead use
# tiles = "Stamen Terrain"

import folium
import pandas


def colordecider(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


data = pandas.read_csv("volcano.txt")

latlist = list(data["LAT"])
lonlist = list(data["LON"])
elev = list(data["ELEV"])

map = folium.Map(location=[38.58, -99.09],
                 zoom_start=6, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el in zip(latlist, lonlist, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=str(
        el)+"m", radius=10, fill_color=colordecider(el), color="grey", fill_opacity=0.7))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")
