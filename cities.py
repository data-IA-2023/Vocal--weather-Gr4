import geonamescache

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
# print countries dictionary
print(countries)
# you really wanna do something more useful with the data...