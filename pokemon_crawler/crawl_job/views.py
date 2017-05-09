import logging 
import json
import redis

from django.shortcuts import render

from django.http import HttpResponse

from my_pokemon_api import *
from db_accessor import *

logger = logging.getLogger("worker")

class Config: 
    pass

def needs_to_crawl(cell_id):
    redis_client = redis.StrictRedis(host=os.environ["REDIS_HOST"], port=6379, db=0)
    response = redis_client.get(cell_id)
    if response == None:
        redis_client.setex(cell_id, 30, "1")
        return True
    else:
        return False


# Create your views here.
def add_crawl_point(request):
    # Print log 
    logger.info("I'm in add_crawl_point")

    # Crawl pokemon data 
    # 1. Get cell id from http request
    # Decoding JSON
    #print request.body
    request_obj = json.loads(request.body)
    cell_id = request_obj["cell_id"]
    
    # Optimization: check if the  pokemon of the cell_id is cached
    if not needs_to_crawl(cell_id):
        return HttpResponse("Skip")

    # 2. Call my search api my_pokemon_api.py
    # Initialize config 
    config = Config() 
    config.auth_service = "ptc"
    config.username = "testuser"
    config.password = "testuser"
    config.proxy = "socks5://127.0.0.1:9050"
    # Initialize pgoapi/mock_pgoapi
    api = init_api(config)
    # Call pgoapi/mock_pgoapi and get pokemon and other info of a cell_id 
    search_response = search_point(cell_id, api)
    # Parse pokemon info from response
    pokemons = parse_pokemon(search_response)
    
    # Print result to log file 
    #print pokemons
    logger.info("Crawl result: {0}".format(json.dumps(pokemons, indent=2)))
    

    # 3. Store search result into database
    # including encounter_id , expire , pokemon_id , latitude , longitude
    for pokemon in pokemons:
        add_pokemon_to_db(pokemon["encounter_id"],
                          pokemon["expiration_timestamp_ms"],
                          pokemon["pokemon_id"],
                          pokemon["latitude"],
                          pokemon["longitude"])   




    return HttpResponse("Response!")
    #return HttpResponse(search_response)
 
