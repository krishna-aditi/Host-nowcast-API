# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:31:40 2022

@author: krish
"""
import streamlit as st
import requests
import base64
import gcsfs
from urllib.parse import unquote
import pathlib
import os
abspath = pathlib.Path(__file__).parent.resolve()
def main():
    st.title("API for Federal Avaiation Administration")
    html_temp = """
        <div style="background-color:steelblue;padding:10px">
        <h2 style="color:white;text-align:center;">SEVIR Nowcasting</h2>
        </div>
        """
    st.markdown(html_temp, unsafe_allow_html=True)
    username = st.text_input("User Name: ")
    password = st.text_input("Password: ", type="password")
    
    authjson = { "username": f"{username}", "password": f"{password}"}

    s = st.session_state
    if not s:
        s.authenticated = False
    col1, col2 = st.columns([0.2,1])
    if col1.button("Login")  or s.authenticated:
        s.authenticated = True
        token = requests.post("https://nowcast-api-test-345519.ue.r.appspot.com/token", data = authjson)
        if col2.button("Log Out"):
            s.authenticated = False
            token = None
            jwttoken = None
            st.markdown(f"Log Out Successful")
            return None
        
        # Login successful        
        if token.status_code == 200: 
            # Headers
            jwttoken = token.json()['access_token']
            headers = {"Authorization": f"Bearer {jwttoken}"}
            # Params by user
            lat = st.number_input("Latitude:", format="%.6f")
            lon = st.number_input("Longitude:", format="%.6f")
            radius = st.number_input("Radius:")
            time_utc = st.text_input("Time in UTC:")
            model_type = st.text_input("Model Type:")
            threshold_time_minutes = st.number_input("Threshold Time in Minutes:", format="%.2f")
            closest_radius = st.radio("Would you like to get the closest point, if location not found in chosen radius?", (True, False))
            forced_refresh = st.radio("Would you like to get a fresh generation of output?", (True, False))
            
            # Parameters as JSON
            params_test = {"lat": lat, "lon": lon, "radius": radius, "time_utc": time_utc, "model_type": model_type, "threshold_time_minutes": threshold_time_minutes, "closest_radius": bool(closest_radius), "forced_refresh": bool(forced_refresh)}
            
            # Perform nowcast
            if st.button("Predict"):
                nowcast_test = requests.post("https://nowcast-api-test-345519.ue.r.appspot.com/nowcast/predict", headers=headers, json = params_test)      
                sevir_output_test = nowcast_test.json()
                # Check for error, if any
                if 'nowcast_error' in sevir_output_test.keys():
                    st.error({'nowcast_error': sevir_output_test['nowcast_error']})
                else:
                    # Read output from bucket
                    st.success('Nowcasted GIF for the requested inputs: ')
                    # Path handling with regex
                    decoded = unquote(sevir_output_test['gif_path'])
                    path = ''
                    append=False
                    for a in decoded.split('/'):
                        if append and a!='o':
                            path+='/'+a.split('?')[0]
                        if a=='sevir-vil':
                            path+=a
                            append=True
                    # Connect to bucket        
                    project_name = 'Assignment-4'
                    credentials = os.path.join(abspath,"cred.json")
                    FS = gcsfs.GCSFileSystem(project=project_name, token=credentials)
                    with FS.open(path, 'rb') as data_file:                
                        gif_content = data_file.read()
                    data_url = base64.b64encode(gif_content).decode("utf-8")
                    st.markdown(f'<p align="center"><img src="data:image/gif;base64,{data_url}" alt="Nowcasted GIF"></p>', unsafe_allow_html=True)
       # Login failed
        else:
            st.markdown(f"Login Failure. {token.json()['detail']}")
    return None
        
    
if __name__ == '__main__':
    main()