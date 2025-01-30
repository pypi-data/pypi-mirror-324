from outscraper import ApiClient
import overpy
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from pyspark.sql import SparkSession
import pandas as pd
import requests
import json
from pprint import pprint
import time
import os
from .outscraper_reviews import (
    OutscraperInterface,
    PlacesPlacesSchema,
    PlacesRawResponseSchema,
    PlacesReviewsSchema,
    PlacesTrafficSchema
)

def multiple_place_intel(api_key, place_groups, region, result_amount=20, radius=10):
    """Get intel on multiple top attractions based on a google maps search query. Provides polygon options for each attraction.
        
        Args:
            api_key (string): You Outscraper API key.
            place_groups (string): A type of location (hotels, hospitals, museums, etc).
            region (string): A city, zip code, county or any other gerneral geographical indicator (not addresses).
            result_amount (int) (optional): The number of attraction results the user would like to recieve. Defaults to 10.
            radius (string or int) (optional): The initial radius of the polygon search. Can be "s" (10 meters), "m" (30 meters), "l" (100 meters), or a custom radius amount.
                                               Defaults to 10 meters. Expands by 10 meters until a ccomplete polygon is found.
            
        Returns:
            A tuple comtaining the following:
                final: A list of dictionaries containing the following:
                    [{'place_id': Google Place ID, 'place_name': Place Name, 'place_groups': Place Group, 'query': Search Query Used, 'polygon_id', Individual ID for a polygon, 'possible_polygon': Polygon Coordinates}]
                polygon_list: A list of tuples with the individual attraction name and all of its polygon options to be used to create a KML file.
        """
    sizes = {"xs": 5, "s": 10, "m": 30, "l": 100}
    try:
        if isinstance(radius, str):
            radius = radius.lower()
            if radius in sizes:
                size = sizes[radius]
        elif isinstance(radius, int):
            size = radius
    except:
        return {"Error": "Invalid radius input."}
    query = f"{place_groups} in {region}"
    try:
        client = ApiClient(api_key)
    except Exception as e:
        return {"Error occurred while creating the API client": f"{e}"}
    results = client.google_maps_search(query, limit=result_amount,  language="en",)
    final = []
    polygon_list = []
    for r in results:
        for result in r:
            result_dict = {}
            polygons = _polygons(result['latitude'], result['longitude'], size)
            for polygon in polygons:
                result_dict = {
                    'place_id': result['place_id'],
                    'place_name': result['name'],
                    'place_group': place_groups,
                    'categories': result['subtypes'],
                    'rating': result['rating'],
                    'star_rating': result.get('about', {}).get('Other', {}).get('Star rating') or result.get('range') or "Null",
                    'query': query,
                    'polygon_id': list(polygon.keys())[0],
                    'possible_polygon': list(polygon.values())[0]
                }
                final.append(result_dict)
            polygon_list.append((result['name'], polygons))
    return final, polygon_list

def single_place_intel(api_key, place_name, radius=10):
    """Get intel on a single attraction based on a google maps search query. Provides polygon options for the attraction.
        
        Args:
            api_key (string): You Outscraper API key.
            place_name (string): The name, address, or Google Place ID of the location the user would like intel on.
            radius (string or int) (optional): The initial radius of the polygon search. Can be "s" (10 meters), "m" (30 meters), "l" (100 meters), or a custom radius amount.
                                               Defaults to 10 meters. Expands by 10 meters until a ccomplete polygon is found.
            
        Returns:
            final: A list with a nested dictionary containing the following:
                [{'place_id': Google Place ID, 'place_name': Place Name, 'place_groups': Place Group, 'query': Search Query Used, 'polygon_id', Individual ID for a polygon, 'possible_polygon': Polygon Coordinates}]
                polygon_list: A list of tuples with the individual attraction name and all of its polygon options to be used to create a KML file.
        """
    sizes = {"xs": 5, "s": 10, "m": 30, "l": 100}
    try:
        if isinstance(radius, str):
            radius = radius.lower()
            if radius in sizes:
                size = sizes[radius]
        elif isinstance(radius, int):
            size = radius
    except:
        return {"Error": "Invalid radius input."}
    query = f"{place_name}"
    try:
        client = ApiClient(api_key)
    except Exception as e:
        return {"Error occurred while creating the API client": f"{e}"}
    results = client.google_maps_search(query, limit=1,  language="en",)
    final = []
    result_dict = {}
    polygon_list = []
    for r in results:
        for result in r:
            polygons = _polygons(result['latitude'], result['longitude'], size)
            for polygon in polygons:
                result_dict = {
                    'place_id': result['place_id'],
                    'place_name': result['name'],
                    'place_group': 'Individual Search',
                    'categories': result['subtypes'],
                    'rating': result['rating'],
                    'star_rating': result.get('about', {}).get('Other', {}).get('Star rating') or result.get('range') or "Null",
                    'query': query,
                    'polygon_id': list(polygon.keys())[0],
                    'possible_polygon': list(polygon.values())[0]
                }
                final.append(result_dict)
            polygon_list.append((result['name'], polygons))
    return final, polygon_list

def hotel_intel(api_key, place_groups, region, ratings, result_amount=0, radius=10):
    """Get intel on multiple top attractions based on a google maps search query. Provides polygon options for each attraction.
        
        Args:
            api_key (string): You Outscraper API key.
            place_groups (string): A type of location (hotels, hospitals, museums, etc).
            region (string): A city, zip code, county or any other gerneral geographical indicator (not addresses).
            result_amount (int) (optional): The number of attraction results the user would like to recieve. Defaults to 10.
            ratings (int or list): Desired star ratings (e.g., 4, 5, or [4, 5]).
            radius (string or int) (optional): The initial radius of the polygon search. Can be "s" (10 meters), "m" (30 meters), "l" (100 meters), or a custom radius amount.
                                               Defaults to 10 meters. Expands by 10 meters until a ccomplete polygon is found.
            
        Returns:
            A tuple comtaining the following:
                final: A list of dictionaries containing the following:
                    [{'place_id': Google Place ID, 'place_name': Place Name, 'place_groups': Place Group, 'query': Search Query Used, 'polygon_id', Individual ID for a polygon, 'possible_polygon': Polygon Coordinates}]
                polygon_list: A list of tuples with the individual attraction name and all of its polygon options to be used to create a KML file.
        """
    sizes = {"xs": 5, "s": 10, "m": 30, "l": 100}
    try:
        if isinstance(radius, str):
            radius = radius.lower()
            if radius in sizes:
                size = sizes[radius]
        elif isinstance(radius, int):
            size = radius
    except:
        return {"Error": "Invalid radius input."}
    
    if not isinstance(ratings, list):
        ratings = [ratings]

    query = f"{place_groups} in {region}"
    try:
        client = ApiClient(api_key)
    except Exception as e:
        return {"Error occurred while creating the API client": f"{e}"}
    results = client.google_maps_search(query, limit=result_amount,  language="en",)
    final = []
    polygon_list = []
    for r in results:
        for result in r:
            star_rating = result.get('about', {}).get('Other', {}).get('Star rating')
            range_rating = result.get('range')
            if any(str(rating) in (star_rating or "") or str(rating) in (range_rating or "") for rating in ratings):
                result_dict = {}
                polygons = _polygons(result['latitude'], result['longitude'], size)
                for polygon in polygons:
                    result_dict = {
                        'place_id': result['place_id'],
                        'place_name': result['name'],
                        'place_group': place_groups,
                        'categories': result['subtypes'],
                        'rating': result['rating'],
                        'star_rating': result.get('about', {}).get('Other', {}).get('Star rating') or result.get('range') or "Null",
                        'query': query,
                        'polygon_id': list(polygon.keys())[0],
                        'possible_polygon': list(polygon.values())[0]
                    }
                    final.append(result_dict)
                polygon_list.append((result['name'], polygons))
    return final, polygon_list


def _polygons(latitude, longitude, size=10):
    """Get polygons on a location based on it's lat/long using overpy to access OpenStreetMap.
        
        Args:
            latitude (int): The latitude of the location.
            longitude (int): The longitude of the location.
            
        Returns:
            results: A list of dictionaries containing the polygons found from the provided lat/long.
        """
        #overpy query
        # Initialize Overpass API
    api = overpy.Overpass()

    # Initial radius and maximum radius
    initial_radius = size  # Starting search radius in meters
    increment = 10        # Increment for each step
    max_radius = 200      # Maximum search radius to prevent infinite loops

    # Function to fetch data with increasing radius
    def fetch_polygons(lat, lon, radius):
        query = f"""
        [out:json];
        (
        way(around:{radius},{lat},{lon});
        relation(around:{radius},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """
        return api.query(query)

    radius = initial_radius
    result = None

    # Keep increasing radius until we get results or hit the max radius
    while radius <= max_radius:
        print(f"Trying radius: {radius} meters...")
        try:
            result = fetch_polygons(latitude, longitude, radius)
            if result.ways or result.relations:  # Check if data is retrieved
                print(f"Data found with radius: {radius} meters")
                break
        except overpy.exception.OverpassTooManyRequests:
            print("Too many requests; please try again later.")
            break
        radius += increment

    # If no results found after max radius
    if not result or (not result.ways and not result.relations):
        print("No data found within the maximum radius.")
        return []
    else:
        final = []
        # Display polygon data
        for way in result.ways:
            lat_long_dict = {}
            lat_long_list = []
            print(f"Polygon for {way.tags.get('name', 'unknown')} (ID: {way.id}):")
            for node in way.nodes:
                print(f"{node.lat}, {node.lon}")
                lat_long_list.append([str(node.lat), str(node.lon)])
            # Only add lat_long_dict if it has more than two coordinate pairs
            if len(lat_long_list) > 2:
                lat_long_dict[str(way.id)] = lat_long_list
                final.append(lat_long_dict)

            print("\n")
            if len(final) > 3:
                break
        return final


def create_kml(polygon_data, output_file):
    """
    Creates a KML file with all polygons grouped into a single folder named after the query.
    
    Args:
        polygon_data (list[dicts]): A list of tuples, where each tuple contains a name and a list of polygons.
                                    Each polygon is a dictionary with ID as key and coordinates as values.
        output_file (string): The name of the KML file to use for Google My Maps. Can include ".kml" or not.
        query_name (string): The name of the folder grouping all polygons (e.g., the query like "Budget Hotels").
            
    Returns:
        KML file: A custom KML file with all polygons found in the provided data.
    """
    # Initialize the root KML structure
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")
    
    # Add default styles
    style_normal = ET.SubElement(document, "Style", id="poly-default-normal")
    line_style = ET.SubElement(style_normal, "LineStyle")
    ET.SubElement(line_style, "color").text = "ff000000"
    ET.SubElement(line_style, "width").text = "1.2"
    poly_style = ET.SubElement(style_normal, "PolyStyle")
    ET.SubElement(poly_style, "color").text = "4c000000"
    ET.SubElement(poly_style, "fill").text = "1"
    ET.SubElement(poly_style, "outline").text = "1"

    style_highlight = ET.SubElement(document, "Style", id="poly-default-highlight")
    line_style_hl = ET.SubElement(style_highlight, "LineStyle")
    ET.SubElement(line_style_hl, "color").text = "ff000000"
    ET.SubElement(line_style_hl, "width").text = "1.8"
    poly_style_hl = ET.SubElement(style_highlight, "PolyStyle")
    ET.SubElement(poly_style_hl, "color").text = "4c000000"
    ET.SubElement(poly_style_hl, "fill").text = "1"
    ET.SubElement(poly_style_hl, "outline").text = "1"

    # Create a single folder named after the query
    folder = ET.SubElement(document, "Folder")
    folder_name = ET.SubElement(folder, "name")
    folder_name.text = output_file

    # Add all polygons into the single folder, using names from polygon_data
    for name, polygons in polygon_data:
        for polygon in polygons:
            for _, coordinates in polygon.items():  # Use only the coordinates
                placemark = ET.SubElement(folder, "Placemark")
                name_elem = ET.SubElement(placemark, "name")
                name_elem.text = name  # Use the name from the tuple
                
                style_url = ET.SubElement(placemark, "styleUrl")
                style_url.text = "#poly-default-normal"
                
                polygon_elem = ET.SubElement(placemark, "Polygon")
                outer_boundary = ET.SubElement(polygon_elem, "outerBoundaryIs")
                linear_ring = ET.SubElement(outer_boundary, "LinearRing")
                coords_elem = ET.SubElement(linear_ring, "coordinates")
                
                # Format coordinates into a string
                coords_text = " ".join([f"{lon},{lat}" for lat, lon in coordinates])
                coords_elem.text = coords_text

    # Pretty-print the KML
    raw_kml = ET.tostring(kml, encoding="unicode")
    dom = parseString(raw_kml)
    pretty_kml = dom.toprettyxml(indent="  ")

    # Write to file
    if not output_file.lower().endswith(".kml"):
        output_file += ".kml"
    with open(output_file, "w", encoding="utf-8") as kml_file:  # Specify utf-8 encoding
        kml_file.write(pretty_kml)




def get_client_places_full(api_key, place_name, review_amount=1, result_amount=1, cutoff=None):
    """Get the raw data, places info, and requested amount of reviews for client based on Google Maps query and return as spark dataframe.
    
    Args:
        place_name (str): A google maps search query akin to searching results on google maps or a google place ID or a list of queries.
        review_amount (int): Amount of reviews returned. Defaults to 1 if not specified. 0 returns all reviews.
        result_amount (int): Amount of query results to return. Defaults to 1 if not specified.
        cutoff (int) (optional): A timestamp for the cutoff date to recieve reviews. All reviews will be after this timestamp.
    
    Returns:
        df_raw (spark): spark dataframe of raw query data.
        df_places (spark): spark dataframe of place data.
        df_reviews (spark): spark dataframe of reviews.
        df_reviews (spark): spark dataframe of traffic.
    """
    conn = OutscraperInterface(api_key, place_name=place_name)
    raw, places, reviews, traffic = conn.get_full_places(review_amount, result_amount, cutoff)
    return raw, places, reviews, traffic






# Define constants
API_ENDPOINT = "https://uberretailapi.uberads.com/v1/uberretailapi/createJob"
API_TOKEN = os.getenv(key="API_TOKEN")

def parse_kml(file_path):
    """
    Parse the KML file and extract relevant data (e.g., coordinates).
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    locations = []
    for placemark in root.findall('.//kml:Placemark', namespaces):
        name = placemark.find('kml:name', namespaces).text
        coords = placemark.find('.//kml:coordinates', namespaces).text.strip()
        locations.append({"name": name, "coordinates": coords})
    print(locations)
    return locations

def create_job_request(locations, start_date, end_date):
    """
    Construct the JSON payload for the API request.
    """
    features = []
    seen_names = {}  # Dictionary to track duplicate names

    for location in locations:
        # Handle duplicate names
        original_name = location["name"].strip()
        if original_name in seen_names:
            seen_names[original_name] += 1
            unique_name = f"{original_name} ({seen_names[original_name]})"
        else:
            seen_names[original_name] = 0
            unique_name = original_name

        # Split and clean up coordinates
        raw_coordinates = location['coordinates']
        try:
            # Ensure the coordinates are properly split
            coord_pairs = raw_coordinates.split()  # Split on whitespace between pairs
            coordinates = [
                list(map(float, coord.strip().split(',')))[:2]  # Extract lon, lat
                for coord in coord_pairs
            ]

            # Ensure coordinates are closed for a valid polygon
            if coordinates[0] != coordinates[-1]:
                coordinates.append(coordinates[0])

            features.append({
                "type": "Feature",
                "properties": {"name": unique_name},  # Use unique name
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates]  # Correct GeoJSON format
                }
            })
        except ValueError as e:
            print(f"Error processing location '{original_name}': {e}")
            continue  # Skip this location if there's an error

    payload = {
        "didReportTypes": ["CEL_CDL_LOCATION_REPORT"],
        "startDateTime": start_date,
        "endDateTime": end_date,
        "polygonInputOptions": {
            "polygonFormat": "GEOJSON",
            "geojson": {
                "type": "FeatureCollection",
                "features": features
            }
        }
    }
    return payload


def get_job_status(job_id):
    """
    Poll the API for job status using the job ID, and fetch results when completed.
    """
    url = f"{API_ENDPOINT.replace('createJob', 'getJobStatus')}?jobId={job_id}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    while True:
        response = requests.get(url, headers=headers)
        try:
            response_json = response.json()
        except ValueError:
            print("Response is not in JSON format")
            return {"error": "Non-JSON response from server"}

        # Print job status
        print("Job Status:", response_json)

        # Check job status
        if response_json.get("jobStatus") == "COMPLETED":
            print("Job is completed. Fetching results...")
            return get_job_results(job_id)
        elif response_json.get("jobStatus") in ["FAILED", "CANCELLED"]:
            print("Job failed or was cancelled.")
            return response_json

        # Wait before polling again
        print("Job is not completed yet. Retrying in 10 seconds...")
        time.sleep(10)

def call_api(payload):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=payload)

    # Check response status
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        if "jobId" in response_json:
            print("Job Created. ID:", response_json["jobId"])
            # Wait for the job to complete and fetch results
            results = get_job_status(response_json["jobId"])
            print("Results:", json.dumps(results, indent=2))
            return results
        return response_json
    except ValueError:
        print("Response is not in JSON format")
        return {"error": "Non-JSON response from server"}

def get_job_results(job_id):
    """
    Fetch the CEL/CDL data once the job is completed.
    """
    url = f"{API_ENDPOINT.replace('createJob', 'getJobResults')}?jobId={job_id}"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(url, headers=headers)

    # Print response for debugging
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Text:", response.text)

    try:
        return response.json()  # Parse JSON response
    except ValueError:
        print("Response is not in JSON format")
        return {"error": "Non-JSON response from server"}

def kml_refine(path):
    # Step 1: Parse the KML file
    file_path = path  # Update with the correct file path
    locations = parse_kml(file_path)
    
    # Step 2: Create the job request payload
    start_date = "2024-11-01 00:00:00"
    end_date = "2024-11-30 23:59:59"
    payload = create_job_request(locations, start_date, end_date)
    
    # Step 3: Call the API
    response = call_api(payload)
    print("API Response:", json.dumps(response, indent=2))


if __name__ == "__main__":
    # result = _polygons(39.1763123, -94.4862721)
    # output_kml_file = "omahazoo.kml"
    # create_kml(result, output_kml_file)
    # info, polygons = single_place_intel(api_key, "st. anthony hotel", "s")
    # create_kml(polygons, "st_anthony_hotel.kml")
    #key = 'NTQyYmMyNzc4MGM3NDU4OGE0ZGRjZTc0YTI0MTlmODJ8ZjZmYzU2N2Y1MA'
    #info, polygons = hotel_intel(key, "St. Anthony Hotel", "San Antonio, TX", [4, 5], 0)
    # info, polygons = multiple_place_intel(key, "Tourist Attractions", "San Antonio, TX", 0)
    #create_kml(polygons, "St.Anthony_Hotel")

    #data, polygons = single_place_intel(key, "St. Anthony Hotel, San Antonio")
    #for record in data:
        #print(record['polygon_id'])
    
    api_key = ''
    place_name = "San Antonio Restaurants"
    raw, places, reviews, traffic = get_client_places_full(api_key, place_name, review_amount=1, result_amount=1, cutoff=None)
    print(raw)
    print(places)
    print(reviews)
    print(traffic)

    #kml_refine(r"C:\Users\blake\.vscode\places_intel\St.Anthony_Hotel.kml")