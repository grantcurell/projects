import csv, json
import logging
from geojson import Feature, FeatureCollection, Point

features = []
with open('conflict_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    logging.info("Reading in data.")
    try:
        for data_id, iso, event_id_cnty, event_id_no_cnty, event_date, year, time_precision, event_type, sub_event_type, actor1, assoc_actor_1, inter1, actor2, assoc_actor_2, inter2, interaction, region, country, admin1, admin2, admin3, location, latitude, longitude, geo_precision, source, source_scale, notes, fatalities, timestamp, iso3 in reader:
            try:
                latitude = float(latitude)
                longitude = float(longitude)
                logging.error("Processing " + str(data_id))
                features.append(
                    Feature(
                        geometry=Point((longitude, latitude)),
                        properties={
                            'data_id': data_id,
                            'iso': iso,
                            'event_id_cnty': event_id_cnty,
                            'event_id_no_cnty': event_id_no_cnty,
                            'event_date': event_date,
                            'year': year,
                            'time_precision': time_precision,
                            'event_type': event_type,
                            'sub_event_type': sub_event_type,
                            'actor1': actor1,
                            'assoc_actor_1': assoc_actor_1,
                            'inter1': inter1,
                            'actor2': actor2,
                            'assoc_actor_2': assoc_actor_2,
                            'inter2': inter2,
                            'interaction': interaction,
                            'region': region,
                            'country': country,
                            'admin1': admin1,
                            'admin2': admin2,
                            'admin3': admin3,
                            'location': location,
                            'latitude': latitude,
                            'longitude': longitude,
                            'geo_precision': geo_precision,
                            'source': source,
                            'source_scale': source_scale,
                            'notes': notes,
                            'fatalities': fatalities,
                            'timestamp': timestamp,
                            'iso3': iso3
                        }
                    )
                )
            except ValueError:
                logging.error("Got invalid data. Skipping.")
    except UnicodeDecodeError as e:
        logging.error("Error is {0}".format(e))
        exit(1)

logging.info("Finished reading in the data.")

collection = FeatureCollection(features)
logging.info("Beginning data write.")
with open("GeoObs.json", "w") as f:
    f.write('%s' % collection)
