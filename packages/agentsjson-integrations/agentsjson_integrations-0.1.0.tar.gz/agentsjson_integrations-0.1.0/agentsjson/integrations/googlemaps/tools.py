import googlemaps
from typing import Any, Dict


def parse_location(location: str) -> Dict[str, Any]:
    split_location = location.split(',')
    return {
        'lat': float(split_location[0]),
        'lng': float(split_location[1])
    }

class Executor:
    @staticmethod
    def create_client(api_key: str, **kwargs) -> googlemaps.Client:
        """
        Creates and returns a Google Maps Client instance using the provided API key.
        
        Parameters:
            api_key (str): Google Maps API Key
        
        Returns:
            googlemaps.Client: Configured Google Maps Client
        """
        client = googlemaps.Client(key=api_key)
        return client

    @staticmethod
    def maps_geolocate(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        response = client.geolocate(**kwargs)
        return response

    @staticmethod
    def maps_directions(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'origin' in kwargs and isinstance(kwargs['origin'], str) and ',' in kwargs['origin']:
            kwargs['origin'] = parse_location(kwargs['origin'])
        if 'destination' in kwargs and isinstance(kwargs['destination'], str) and ',' in kwargs['destination']:
            kwargs['destination'] = parse_location(kwargs['destination'])
        return client.directions(**kwargs)

    @staticmethod
    def maps_elevation(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'locations' in kwargs and isinstance(kwargs['locations'], str) and ',' in kwargs['locations']:
            kwargs['locations'] = parse_location(kwargs['locations'])
        return client.elevation(**kwargs)

    @staticmethod
    def maps_geocode(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        return client.geocode(**kwargs)

    @staticmethod
    def maps_timezone(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'location' in kwargs and isinstance(kwargs['location'], str) and ',' in kwargs['location']:
            kwargs['location'] = parse_location(kwargs['location'])
        return client.timezone(**kwargs)

    @staticmethod
    def maps_snap_to_roads(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        return client.snap_to_roads(**kwargs)

    @staticmethod
    def maps_nearest_roads(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        return client.nearest_roads(**kwargs)

    @staticmethod
    def maps_distance_matrix(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'origins' in kwargs and isinstance(kwargs['origins'], str) and ',' in kwargs['origins']:
            kwargs['origins'] = parse_location(kwargs['origins'])
        if 'destinations' in kwargs and isinstance(kwargs['destinations'], str) and ',' in kwargs['destinations']:
            kwargs['destinations'] = parse_location(kwargs['destinations'])
        return client.distance_matrix(**kwargs)

    @staticmethod
    def maps_place_details(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        return client.place(**kwargs)

    @staticmethod
    def maps_find_place_from_text(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        return client.find_place(**kwargs)

    @staticmethod
    def maps_nearby_search(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'location' in kwargs and isinstance(kwargs['location'], str) and ',' in kwargs['location']:
            kwargs['location'] = parse_location(kwargs['location'])
        return client.places_nearby(**kwargs)

    @staticmethod
    def maps_text_search(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'location' in kwargs and isinstance(kwargs['location'], str) and ',' in kwargs['location']:
            kwargs['location'] = parse_location(kwargs['location'])
        return client.places(**kwargs)

    @staticmethod
    def maps_place_photo(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        return client.places_photo(**kwargs)

    @staticmethod
    def maps_query_autocomplete(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'location' in kwargs and isinstance(kwargs['location'], str) and ',' in kwargs['location']:
            kwargs['location'] = parse_location(kwargs['location'])
        return client.places_autocomplete_query(**kwargs)

    @staticmethod
    def maps_autocomplete(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'location' in kwargs and isinstance(kwargs['location'], str) and ',' in kwargs['location']:
            kwargs['location'] = parse_location(kwargs['location'])
        return client.places_autocomplete(**kwargs)

    @staticmethod
    def maps_street_view(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'location' in kwargs and isinstance(kwargs['location'], str) and ',' in kwargs['location']:
            kwargs['location'] = parse_location(kwargs['location'])
        return client.streetview(**kwargs)

    @staticmethod
    def maps_street_view_metadata(api_key: str, **kwargs) -> Dict[str, Any]:
        client = Executor.create_client(api_key)
        if 'location' in kwargs and isinstance(kwargs['location'], str) and ',' in kwargs['location']:
            kwargs['location'] = parse_location(kwargs['location'])
        return client.streetview_metadata(**kwargs)