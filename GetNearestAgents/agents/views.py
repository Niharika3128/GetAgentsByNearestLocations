from django.shortcuts import render
from agents.models import AgentsModel,LatituteAndLongituteModel,GivenPlaces
from django.core.paginator import Paginator

def getNearestLocations(request,pno=None,id=None):
    if not (pno and id):
        place_id = request.GET.get('id')
        page_no = 1
    else:
        place_id = id
        page_no = pno
    place = GivenPlaces.objects.get(id=place_id)
    queryset = LatituteAndLongituteModel.objects.all()
    city_list = [{'lat':x.latitute,'lon':x.longitute,'id':x.id} for x in queryset]
    city_to_find = {'lat': place.latitute, 'lon': place.longitute}
    nearest_locations = find_closest_lat_lon(city_list, city_to_find)
    nearest_locations.sort(key=lambda x: x[0])
    hundred_nearest_locations = nearest_locations[0:100]
    data = [LatituteAndLongituteModel.objects.get(id=each_location[1]) for each_location in hundred_nearest_locations]
    nearest_agents = [AgentsModel.objects.get(id=each_object.agents_id) for each_object in data]
    pg = Paginator(nearest_agents, 10)
    page = pg.page(page_no)
    return render(request, 'agents.html', {"agents_data":page, 'place_data':place})


def dist_between_two_lat_lon(*args):
    from math import asin, cos, radians, sin, sqrt
    lat1, lat2, long1, long2,place_id = args
    lat1, lat2, long1, long2,place = map(radians, args)
    dist_lats = abs(lat2 - lat1)
    dist_longs = abs(long2 - long1)
    a = sin(dist_lats / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_longs / 2) ** 2
    c = asin(sqrt(a)) * 2
    radius_earth = 6378
    return c * radius_earth,place_id


def find_closest_lat_lon(data, v):
    return [dist_between_two_lat_lon(v['lat'], v['lon'], x['lat'], x['lon'],x['id']) for x in data]
