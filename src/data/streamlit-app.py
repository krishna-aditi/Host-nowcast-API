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

def main():
    st.title("API for Federal Avaiation Administration")
    html_temp = """
        <div style="background-color:steelblue;padding:10px">
        <h2 style="color:white;text-align:center;">SEVIR Nowcasting</h2>
        </div>
        """
    st.markdown(html_temp, unsafe_allow_html=True)
    lat = st.number_input("Latitude:", format="%.6f")
    lon = st.number_input("Longitude:", format="%.6f")
    radius = st.number_input("Radius:")
    time_utc = st.text_input("Time UTC:")
    model_type = st.text_input("Model Type:")
    closest_radius = st.radio("Would you like to get the closest point, if location not found in chosen radius?", ("True", "False"))
    forced_refresh = st.radio("Would you like to get a fresh generation of output?", ("True", "False"))
    
    # Parameters as JSON
    params_test = {"lat": lat, "lon": lon, "radius": radius, "time_utc": time_utc, "model_type": model_type, "closest_radius": closest_radius, "forced_refresh": forced_refresh}
    
    if st.button("Predict"):
        nowcast_test = requests.post("http://127.0.0.1:8000/nowcast/", json = params_test)      
        sevir_output_test = nowcast_test.json()
        if 'nowcast_error' in sevir_output_test.keys():
            st.error({'nowcast_error': sevir_output_test['nowcast_error']})
        else:
            st.success('Nowcasted GIF for the requested inputs: ')
            decoded = unquote(sevir_output_test['gif_path'])
            path = ''
            append=False
            for a in decoded.split('/'):
                if append and a!='o':
                    path+='/'+a.split('?')[0]
                if a=='sevir-vil':
                    path+=a
                    append=True
            project_name = 'Assignment-4'
            credentials = "cred.json"
            FS = gcsfs.GCSFileSystem(project=project_name, token=credentials)
            with FS.open(path, 'rb') as data_file:                
                gif_content = data_file.read()
            data_url = base64.b64encode(gif_content).decode("utf-8")
            st.markdown(f'<p align="center"><img src="data:image/gif;base64,{data_url}" alt="Nowcasted GIF"></p>', unsafe_allow_html=True)
if __name__ == '__main__':
    main()