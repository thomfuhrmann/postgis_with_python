import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from mpl_toolkits.axes_grid1 import make_axes_locatable

place_name = "Helmut-Zilk-Park, 1100 Wien"
area = ox.geocode_to_gdf(place_name)

#area.plot()
#plt.show()

# OSM building footprints
tags = {'building': True}

buildings = ox.geometries_from_place(place_name, tags)
landuse = ox.geometries_from_place(place_name, tags={'landuse': True}, buffer_dist=500)
#fig, ax = plt.subplots(figsize=(15, 15))
#landuse.plot(column='landuse', ax=ax, legend=True)
#(landuse[landuse['landuse']=='grass']).plot(column='landuse', ax=ax)
#buildings.plot(ax=ax, color='None',lw=1,alpha=1)
#ax.axis('off')
#plt.show()

# saving buildings and landuse to a shapefile
buildings  = buildings.loc[:,buildings.columns.str.contains('geometry')]
buildings = buildings.loc[buildings.geometry.type=='Polygon']

#buildings.to_file('sonnwendviertel_buildings.shp')

landuse  = landuse.loc[:,landuse.columns.str.contains('landuse|geometry')]
landuse = landuse.loc[landuse.geometry.type=='Polygon']

#landuse.to_file('sonnwendviertel_landuse.shp')



db_string = "postgresql://postgres:sle888imp@localhost:5432/sonnwendviertel"
db_connection = create_engine(db_string)


within50 = gpd.GeoDataFrame.from_postgis("SELECT * FROM within50;", db_connection, geom_col='geom', index_col='gid', coerce_float=True)

#fig, ax = plt.subplots(figsize=(15, 15))
#within50.plot(ax=ax, color='None', alpha=1)
#(landuse[landuse['landuse']=='grass']).plot(color='g', ax=ax)
#ax.axis('off')
#plt.show()


distances = gpd.GeoDataFrame.from_postgis("SELECT * FROM buildingsDistances;", db_connection, geom_col='geom', crs=None, index_col='gid')

fig, ax = plt.subplots(figsize=(15, 15))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
im = distances.plot(column='dist', cmap='viridis', ax=ax, legend=True, cax=cax)
(landuse[landuse['landuse']=='grass']).plot(ax=ax, color='g')
plt.show()




