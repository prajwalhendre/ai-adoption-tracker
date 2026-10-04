import requests
import time
from datetime import datetime

#api endpoint for periods
url = 'https://www.census.gov/hfp/btos/api/periods'    


try:
    #send the actual reqest to api
    response = requests.get(url, timeout=(3.0, 30.0))

    #flag if successful (200)
    response.raise_for_status()

    #convert to json
    periods_data = response.json()
    print(periods_data)

#http error
except requests.exceptions.HTTPError as error:
    raise print(f"HTTP error occurred: {error}")
#generic error
except Exception as error:
    raise print(f"An error occurred: {error}")

#raw data from all periods
all_rows = []
for period in (periods_data):
    if datetime.strptime(period['COLLECTION_END'], '%d-%b-%y %I.%M.%S.%f %p') > datetime.now():
        continue
    
    period_url = f"https://www.census.gov/hfp/btos/api/periods/{period['PERIOD_ID']}/data"
    try:
        #send the actual reqest to api
        response = requests.get(period_url, timeout=(3.0, 30.0))
        time.sleep(1)
        
        #flag if successful (200)
        response.raise_for_status()

        #convert to json
        raw_data = response.json()
        all_rows.extend(raw_data)

    #http error
    except requests.exceptions.HTTPError as error:
        print(f"HTTP error occurred: {error}")
    #generic error
    except Exception as error:
        print(f"An error occurred: {error}")


print(len(all_rows))