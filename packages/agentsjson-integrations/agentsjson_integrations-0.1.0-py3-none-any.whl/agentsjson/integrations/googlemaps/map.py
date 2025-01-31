from .tools import Executor

map = {
    'maps_geolocate': Executor.maps_geolocate,
    'maps_directions': Executor.maps_directions,
    'maps_elevation': Executor.maps_elevation,
    'maps_geocode': Executor.maps_geocode,
    'maps_timezone': Executor.maps_timezone,
    'maps_snap_to_roads': Executor.maps_snap_to_roads,
    'maps_nearest_roads': Executor.maps_nearest_roads,
    'maps_distance_matrix': Executor.maps_distance_matrix,
    'maps_place_details': Executor.maps_place_details,
    'maps_find_place_from_text': Executor.maps_find_place_from_text,
    'maps_nearby_search': Executor.maps_nearby_search,
    'maps_text_search': Executor.maps_text_search,
    'maps_place_photo': Executor.maps_place_photo,
    'maps_query_autocomplete': Executor.maps_query_autocomplete,
    'maps_autocomplete': Executor.maps_autocomplete,
    'maps_street_view': Executor.maps_street_view,
    'maps_street_view_metadata': Executor.maps_street_view_metadata,
}