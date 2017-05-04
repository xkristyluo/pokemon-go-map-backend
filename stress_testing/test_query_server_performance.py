import requests
import time
from multiprocessing import Pool

def create_thousand_request(index):
    start = time.time()

    for i in range(1000):
        response = requests.get("http://query-server.uzmrbxifde.us-west-2.elasticbeanstalk.com/map/pokemons?east=-96.49933208864907&south=36.220743510181975&north=36.24487118302896&west=-96.53731216829995")

    end = time.time()

    print end - start


if __name__ == '__main__':
    p = Pool(20)
    print(p.map(create_thousand_request, range(20)))
