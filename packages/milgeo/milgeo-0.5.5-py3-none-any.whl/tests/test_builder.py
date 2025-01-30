import os
import pytest
from milgeo.enum import PlatformType, ReliabilityCredibility
from milgeo.geometry import GeometriesList, Point, Line, Polygon
from milgeo.builder import CSVBuilder, FeatureBuilder, PlacemarkBuilder


@pytest.fixture
def sample_polygon_geometry():
    return Polygon(
        name="Geometry",
        coordinates=[[[10.0, 20.0], [10.0, 20.0], [10.0, 20.0], [10.0, 20.0]]],
        sidc="12345678901234567890",
        outline_color="#ff0000",
        fill_color="#00ff00",
        fill_opacity="0.5",
        comments=["Comment 1", "Comment 2"]
    )

@pytest.fixture
def sample_point_geometry():
    return Point(
        name="Point",
        coordinates=[10.0, 20.0],
        sidc="12345678901234567890",
        observation_datetime="2024-01-01T00:00:00",
        reliability_credibility=ReliabilityCredibility.A2,
        staff_comments="Staff comments",
        platform_type=PlatformType.SAT,
        direction="N",
        speed="100 km/h",
        quantity="1",
        outline_color="#ff0000",
        fill_color="#00ff00",
        fill_opacity="0.5",
        metadata={"key1": ["value1", "value2"]},
    )

def test_featurebuilder_basic_elements(sample_polygon_geometry):
    builder = FeatureBuilder(sample_polygon_geometry)
    builder.add_basic_elements()
    feature = builder.build()
    assert feature["properties"]["name"] == "Geometry"
    assert feature["properties"]["sidc"] == "12345678901234567890"
    assert feature["properties"]["comments"] == []


def test_featurebuilder_optional_properties(sample_polygon_geometry):
    sample_polygon_geometry.observation_datetime = "2024-01-01T00:00:00"
    sample_polygon_geometry.quantity = "5"
    builder = FeatureBuilder(sample_polygon_geometry)
    builder.add_optional_properties()
    feature = builder.build()
    assert feature["properties"]["observation_datetime"] == "2024-01-01T00:00:00"
    assert feature["properties"]["quantity"] == "5"
    assert feature["properties"]["comments"] == ["Comment 1", "Comment 2"]


def test_featurebuilder_geometry(sample_polygon_geometry):
    builder = FeatureBuilder(sample_polygon_geometry)
    builder.add_geometry()
    feature = builder.build()
    assert feature["geometry"]["type"] == sample_polygon_geometry.geometry_type
    assert feature["geometry"]["coordinates"] == sample_polygon_geometry.coordinates


def test_placemarkbuilder_basic_elements(sample_polygon_geometry):
    builder = PlacemarkBuilder(sample_polygon_geometry)
    builder.add_basic_elements()
    placemark_xml = builder.build()
    assert placemark_xml.find('name').text == "Geometry"


def test_placemarkbuilder_optional_properties(sample_polygon_geometry):
    builder = PlacemarkBuilder(sample_polygon_geometry)
    builder.add_optional_properties()
    placemark_xml = builder.build()
    assert placemark_xml.find('.//LineStyle/color').text == "#ff0000"
    assert placemark_xml.find('.//PolyStyle/color').text == "7f00ff00"


def test_placemarkbuilder_point_geometry(sample_polygon_geometry):
    sample_geometry = Point(
        name="Point",
        coordinates=[10.0, 20.0]
    )
    builder = PlacemarkBuilder(sample_geometry)
    builder.add_geometry()
    placemark_xml = builder.build()
    assert placemark_xml.find('.//Point/coordinates').text == "10.0,20.0"


def test_placemarkbuilder_linestring_geometry():
    sample_geometry = Line(
        name="Line",
        coordinates=[[10.0, 20.0], [30.0, 40.0]]
    )
    builder = PlacemarkBuilder(sample_geometry)
    builder.add_geometry()
    placemark_xml = builder.build()
    assert placemark_xml.find('.//LineString/coordinates').text == "10.0,20.0 30.0,40.0"


def test_placemarkbuilder_polygon_geometry():
    sample_geometry = Polygon(
        name="Polygon",
        coordinates=[[[10.0, 20.0], [30.0, 40.0], [50.0, 60.0], [10.0, 20.0]]]
    )
    builder = PlacemarkBuilder(sample_geometry)
    builder.add_geometry()
    placemark_xml = builder.build()
    assert placemark_xml.find('.//Polygon/outerBoundaryIs/LinearRing/coordinates').text == "10.0,20.0 30.0,40.0 50.0,60.0 10.0,20.0"

def test_point_builder_without_sidc():
    sample_geometry = Point(
        name="Point",
        coordinates=[10.0, 20.0]
    )    

    builder = PlacemarkBuilder(sample_geometry)
    builder.add_basic_elements()
    builder.add_optional_properties()
    builder.add_geometry()

    placemark_xml = builder.build()
    assert placemark_xml.find("name").text == "Point"
    assert placemark_xml.find("sidc").text == "10012500001313000000"


def test_point_builder_with_sidc():
    sample_geometry = Point(
        name="Other name",
        coordinates=[10.0, 20.0],
        sidc="10012500001314000000"
    )    

    builder = PlacemarkBuilder(sample_geometry)
    builder.add_basic_elements()
    builder.add_optional_properties()
    builder.add_geometry()

    placemark_xml = builder.build()
    assert placemark_xml.find("name").text == "Other name"
    assert placemark_xml.find("sidc").text == "10012500001314000000"

def test_point_builder_without_name():
    sample_geometry = Point(
        name=None,
        coordinates=[10.0, 20.0],
        sidc="10012500001314000000",
    )   
    builder = PlacemarkBuilder(sample_geometry)
    builder.add_basic_elements()
    builder.add_optional_properties()
    builder.add_geometry()

    placemark_xml = builder.build()

    assert placemark_xml.find("name").text == ''


def test_point_builder_with_comment():
    sample_geometry = Point(
        name="Other name",
        coordinates=[10.0, 20.0],
        sidc="10012500001314000000",
        comments=["Comment 1", "Comment 2"]
    )   
    builder = PlacemarkBuilder(sample_geometry)
    builder.add_basic_elements()
    builder.add_optional_properties()
    builder.add_geometry()

    placemark_xml = builder.build()

    assert placemark_xml.find("ExtendedData/Data[@name='comments']/value").text == "Comment 1\nComment 2"
 

def test_csvbuilder_point_with_all_properties(sample_point_geometry):
    builder = CSVBuilder(sample_point_geometry)
    builder.add_basic_elements()
    builder.add_optional_properties()
    builder.add_geometry()

    csv_features = builder.build()
    assert csv_features == {
        "sidc": "12345678901234567890",
        "name": "Point",
        "observation_datetime": "2024-01-01T00:00:00",
        "reliability_credibility": "A2",
        "staff_comments": "Staff comments",
        "platform_type": "SAT",
        "direction": "N",
        "speed": "100 km/h",
        "quantity": "1",
        "outline-color": "#ff0000",
        "fill-color": "#00ff00",
        "fill-opacity": "0.5",
        "coordinates": "POINT (10.0 20.0)",
        "milgeo:meta:key1": '["value1", "value2"]',
    }

def test_csvbuilder_linestring_geometry():
    sample_geometry = Line(
        name="Line",
        coordinates=[[10.0, 20.0], [30.0, 40.0]]
    )
    builder = CSVBuilder(sample_geometry)
    builder.add_basic_elements()
    builder.add_optional_properties()
    builder.add_geometry()

    csv_features = builder.build()
    assert csv_features == {
        "sidc": "10016600001100000000",
        "name": "Line",
        "coordinates": "LINESTRING (10.0 20.0, 30.0 40.0)",
    }

def test_csvbuilder_polygon_geometry(sample_polygon_geometry):
    builder = CSVBuilder(sample_polygon_geometry)
    builder.add_basic_elements()
    builder.add_optional_properties()
    builder.add_geometry()

    csv_features = builder.build()
    assert csv_features == {
        "sidc": "12345678901234567890",
        "name": "Geometry",
        "coordinates": "POLYGON ((10.0 20.0, 10.0 20.0, 10.0 20.0, 10.0 20.0))",
        "fill-color": "#00ff00",
        "fill-opacity": "0.5",
        "outline-color": "#ff0000",
        "comment 1": "Comment 1",
        "comment 2": "Comment 2",
    }

def test_csvbuilder_save_file(sample_point_geometry, sample_polygon_geometry):
    geometries = GeometriesList()
    geometries.add_geometry(sample_point_geometry)
    geometries.add_geometry(sample_polygon_geometry)

    os.makedirs("tests/output/csv", exist_ok=True)
    geometries.save_csv("tests/output/csv", "test")

    assert os.path.exists("tests/output/csv/test-part-1.csv")

    with open("tests/output/csv/test-part-1.csv", "r") as file:
        content = file.read()
    
    assert content == '''comment 1,comment 2,coordinates,direction,fill-color,fill-opacity,milgeo:meta:key1,name,observation_datetime,outline-color,platform_type,quantity,reliability_credibility,sidc,speed,staff_comments
,,POINT (10.0 20.0),N,#00ff00,0.5,"[""value1"", ""value2""]",Point,2024-01-01T00:00:00,#ff0000,SAT,1,A2,12345678901234567890,100 km/h,Staff comments
Comment 1,Comment 2,"POLYGON ((10.0 20.0, 10.0 20.0, 10.0 20.0, 10.0 20.0))",,#00ff00,0.5,,Geometry,,#ff0000,,,,12345678901234567890,,
'''