#!/usr/bin/env python3

import logging
import os
import random

from Country import Country
from dbutils import Database
from sample_utils import get_uniq_names

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

SAMPLES_DIR = './samples'
BY_CITIES_FILE = os.path.join(SAMPLES_DIR, 'by.json')
PL_CITIES_FILE = os.path.join(SAMPLES_DIR, 'pl.json')
LV_CITIES_FILE = os.path.join(SAMPLES_DIR, 'lv.json')
LT_CITIES_FILE = os.path.join(SAMPLES_DIR, 'lt.json')
UA_CITIES_FILE = os.path.join(SAMPLES_DIR, 'ua.json')
NAMES_FILE = os.path.join(SAMPLES_DIR, 'namelist.json')

NATIONALITIES = ['Belarusian', 'Polish', 'Latvian',
                 'Lithuanian', 'Ukrainian']


by_coordinates = Country(BY_CITIES_FILE)
pl_coordinates = Country(PL_CITIES_FILE)
lv_coordinates = Country(LV_CITIES_FILE)
lt_coordinates = Country(LT_CITIES_FILE)
ua_coordinates = Country(UA_CITIES_FILE)

NATIONAL_COORDINATES = {
    NATIONALITIES[0]: by_coordinates,
    NATIONALITIES[1]: pl_coordinates,
    NATIONALITIES[2]: lv_coordinates,
    NATIONALITIES[3]: lt_coordinates,
    NATIONALITIES[4]: ua_coordinates
}

uniq_names = get_uniq_names(NAMES_FILE)

logging.debug('by max_latitude: %s', by_coordinates.max_latitude())
logging.debug("by min_latitude: %s", by_coordinates.min_latitude())
logging.debug("by max_longitude: %s", by_coordinates.max_longitude())
logging.debug("by min_longitude: %s", by_coordinates.max_longitude())

logging.info('Creating the database connection')
try:
    db = Database()
    cursor = db.cursor()
    db.create_tables()
except Exception as e:
    logging.CRITICAL("Unable to create the database: %s", e)


for nationality in NATIONALITIES:
    for i in range(1000):
        name = random.choice(uniq_names)
        random_lat = random.uniform(
            NATIONAL_COORDINATES[nationality].min_latitude(),
            NATIONAL_COORDINATES[nationality].max_latitude()
            )
        random_long = random.uniform(
            NATIONAL_COORDINATES[nationality].min_longitude(),
            NATIONAL_COORDINATES[nationality].max_longitude()
            )

        cursor.execute(
            'INSERT INTO users(\
                name, nationality, latitude, longitude)\
                    VALUES(%s, %s, %s, %s) ', (
                        name, nationality, random_lat, random_long))

db.commit()
db.close()
logging.info('Exiting')
