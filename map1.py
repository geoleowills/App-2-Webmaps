import folium
import pandas

# Decides the colour dependant on elevation


def colordecider(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


data = pandas.read_csv("volcano.txt")
# Creates lists for latitude, longitude and elevation to be iterated through

latlist = list(data["LAT"])
lonlist = list(data["LON"])
elev = list(data["ELEV"])

# Creates a base map
map = folium.Map(location=[38.58, -99.09],
                 zoom_start=6, tiles="Stamen Terrain")

# Creates a new layer for volcanoes
fgv = folium.FeatureGroup(name="Volcanoes")
# Adds the markers onto location of volcanoes on the fgv layer, chooses colour or marker using 'colordicider' function
for lt, ln, el in zip(latlist, lonlist, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=str(
        el)+"m", radius=10, fill_color=colordecider(el), color="grey", fill_opacity=0.7))

# Creates new layer for populations
fgp = folium.FeatureGroup(name="Population")
# Shades each country in one of three colours on the fgp layer, dependant on their populations size
fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                             style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# Adds layers onto original base map
map.add_child(fgv)
map.add_child(fgp)

# Adds option for layer control, choose which layer to show
map.add_child(folium.LayerControl())

map.save("Map1.html")
