#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 10:59:57 2022

@author: krish
"""

import os
from nowcast_helper import get_nowcast_data, run_model, writeDataToCloud
import dateutil.parser
import datetime

# Use the following for testing nowcast(lat=37.318363, lon=-84.224203, radius=100, time_utc='2019-06-02 18:33:00', model_type='gan',closest_radius=True)
def nowcast(lat, lon, radius, time_utc, model_type, closest_radius=False, force_refresh=False):
    Error = None
    # Parse time
    try:
        user_time = dateutil.parser.parse(time_utc)
    except Exception:
        Error = 'Invalid date time format. Please provide a valid format (refer to https://dateutil.readthedocs.io/en/stable/parser.html)'
        return {'Error': Error}
    # Data cannot be older than 2019 June 1st (As per paper)
    if user_time.month < 6:
        if user_time.year < 2019:
           Error = 'Request date is too old! Try dates after 2019, June 1st'
           return {'Error': Error}
    
    
    try:
        # Filter to get data
        exists, data, filename = get_nowcast_data(lat = lat, lon = lon, radius = radius, time_utc = time_utc, catalog_path = 'sevir-vil/CATALOG.csv', data_path = 'sevir-vil', closest_radius = closest_radius, force_refresh = force_refresh)
        if exists:
            return {'display':filename}
        # Run model
        output = run_model(data, 'sevir-vil/models/nowcast/', scale = True, model_type = model_type)
        # Timestamp when API is called and GIF is built
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Output GIF
        display_path = writeDataToCloud(data = output, file_path = os.path.join('sevir-vil/output',f'Predicted{filename}_{timestamp}.gif'), file_type='gif',time_utc=time_utc)

    except Exception as e:
        return {'Error': str(e)}
    
    # Return path for output
    return {'display':display_path}
