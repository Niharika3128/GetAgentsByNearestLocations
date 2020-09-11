from django.core.management.base import BaseCommand

from GetNearestAgents.settings import AGENTS_DATA_FILE
from agents.models import AgentsModel,LatituteAndLongituteModel,GivenPlaces
import openpyxl
import xlrd2 as xl

from opencage.geocoder import OpenCageGeocode, RateLimitExceededError

class Command(BaseCommand):
    def handle(self, *args, **options):
        def getLatituteAndLongitute(place):
            try:
                key = '6c81f22653b6405cb3e5db02b048dbcb'  # get api key from:  https://opencagedata.com
                geocoder = OpenCageGeocode(key)
                results = geocoder.geocode(place)
                if results:
                    lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
                else:
                    results = geocoder.geocode(place.split(' ', 1)[1])
                    if results:
                        lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
                    else:
                        results = geocoder.geocode(place.rsplit(' ', 1)[1])
                        if results:
                            lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
                        else:
                            results = geocoder.geocode(place.rsplit(' ', 2)[1])
                            lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
                return lat, lng
            except RateLimitExceededError:
                return "Your rate limit has expired"

        given_places = ['New york city, New york', 'Boston, Massachusetts', 'Los Angeles, California',
                        'Chicago, Illinois', 'Houston, Texas', 'Phoenix, Arizona', 'San Diego, California',
                        'Dallas, Texas', 'San Jose, California', 'Austin, Texas', 'Columbus, Ohio']

        def savePlaces():
            for each_place in given_places:
                result = getLatituteAndLongitute(each_place)
                GivenPlaces(city_name=each_place, latitute=result[0], longitute=result[1]).save()
            print("Latitute and Longitude of Given Places are saved into Database")

        path = AGENTS_DATA_FILE
        wb_obj = openpyxl.load_workbook(path)
        wb = xl.open_workbook(path)
        sheet_obj = wb_obj.active
        list_of_agents = []
        s1 = wb.sheet_by_index(0)
        s1.cell_value(1, 0)  # initializing cell from the excel file mentioned through the cell position

        for cell in sheet_obj.iter_rows(min_row=2, min_col=1, max_row=s1.nrows - 1, max_col=s1.ncols):
            agent_data = []
            for i in cell:
                agent_data.append(i.value)
            list_of_agents.append(agent_data)

        for x in list_of_agents:
            AgentsModel(id=x[0], name=x[1], address=x[2], city=x[3], zipcode=x[4], state=x[5]).save()
        print("Agents Data is saved into Database")

        savePlaces()

        queryset = AgentsModel.objects.values_list('id', 'address')
        for each_object in queryset:
            result = getLatituteAndLongitute(each_object[1])
            LatituteAndLongituteModel(agents_id=each_object[0], latitute=result[0], longitute=result[1]).save()
        print("Latitute and Longitude of the agents address are saved into database")
