'''
import logging
import json

from django.shortcuts import render
from django.http import HttpResponse

from db_accessor import get_pokemons_from_db 

import boto3
import s2sphere


SQS_QUEUE_NAME = "awseb-e-k4gwgatxz5-stack-AWSEBWorkerQueue-12UE2BKTWF3SW"

# Use s2sphere to get a set of S2 cells at level 15 covering a rectangle in (lat, lng) coordinates    
def break_down_area_to_cell(north, south, west, east):
    # Return a list of S2 cells
    result = []

    region = s2sphere.RegionCoverer()
    # set level to 15 to meet the requirement of Pokemon Go
    region.min_level = 15
    region.max_level = 15
    p1 = s2sphere.LatLng.from_degrees(north, west) # set upper-left corner 
    p2 = s2sphere.LatLng.from_degrees(south, east) # set bottom-right corner

    # optimization: do not scan the area if the area is larger than 7e-8 
    rect = s2sphere.LatLngRect.from_point_pair(p1, p2) # a rectangle in latitude-longitude space
    area = rect.area() # area in steradians
    if (area * 1000 * 1000 * 100 > 7):
        return result 
   
    cell_ids = region.get_covering(s2sphere.LatLngRect.from_point_pair(p1, p2))

    # convert hex cell_ids to decimal and add to result
    result += [ cell_id.id() for cell_id in cell_ids ]

    return result


# Scan an area and return all pokemon objects in that area. 
# An area is a square defined by 4 corner coordinates (lat, lng) on the map.  
def scan_area(north, south, west, east):
    result = []
        
    # 1. Find all points to search within the area using Google S2
    cell_ids = break_down_area_to_cell(north, south, west, east)
    
    # Get the service resource    
    work_queue = boto3.resource('sqs', region_name='us-west-2').get_queue_by_name(QueueName=SQS_QUEUE_NAME)

    # 2. Search each point, get result from api
    for cell_id in cell_ids: 
        print cell_id
        # Send request (cell_ids) to elastic beanstalk worker server
        work_queue.send_message(MessageBody=json.dumps({"cell_id":cell_id})) 
 
    return result


# Create your views here.
# Return pokemon info in the current map view defined by north, south, west, east bounds. 
# The pokemon info includes pokemon_id, expiration_timestamp_ms, longitude and latitude. 
def pokemons(request):
    # 1. Get bounds info  of the current map view from HttpRequest object
    north = request.GET["north"];
    south = request.GET["south"];
    west = request.GET["west"];
    east = request.GET["east"];

    # 2. Query database 
    result = get_pokemons_from_db(north, south, west, east)

    # 3. Publish crawl job
    scan_area(float(north), float(south), float(west), float(east))

    return HttpResponse(json.dumps(result))
'''

import logging
import json

import s2sphere
import boto3

from django.shortcuts import render
from django.http import HttpResponse

from db_accessor import get_pokemons_from_db 

SQS_QUEUE_NAME = "awseb-e-k4gwgatxz5-stack-AWSEBWorkerQueue-12UE2BKTWF3SW"

def break_down_area_to_cell(north, south, west, east):
    """ Return a list of s2 cell id """
    result = []

    region = s2sphere.RegionCoverer()
    region.min_level = 15
    region.max_level = 15
    p1 = s2sphere.LatLng.from_degrees(north, west)
    p2 = s2sphere.LatLng.from_degrees(south, east)

    rect = s2sphere.LatLngRect.from_point_pair(p1, p2)
    area = rect.area()
    if (area * 1000 * 1000 * 100 > 7):
        return result

    cell_ids = region.get_covering(s2sphere.LatLngRect.from_point_pair(p1, p2))
    result += [ cell_id.id() for cell_id in cell_ids ] 

    return result

def scan_area(north, south, west, east):
    result = []

    # 1. Find all point to search with the area
    cell_ids = break_down_area_to_cell(north, south, west, east)

    # 2. Search each point, get result from api
    work_queue = boto3.resource('sqs', region_name='us-west-2').get_queue_by_name(QueueName=SQS_QUEUE_NAME)
    for cell_id in cell_ids:
        print cell_id
        # 3. Send request to elastic beanstalk worker server
        work_queue.send_message(MessageBody=json.dumps({"cell_id":cell_id})) 

    return result


def pokemons(request):
    # 1. Get longitude latitude info
    north = request.GET["north"]
    south = request.GET["south"]
    west = request.GET["west"]
    east = request.GET["east"]

    # 2. Query database
    result = get_pokemons_from_db(north, south, west, east)

    # 3. Publish crawl job
    scan_area(float(north), float(south), float(west), float(east))
    
    return HttpResponse(json.dumps(result))
