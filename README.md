Hosting SEVIR Nowcast API using Google Cloud Platform and Streamlit
=================================

Report link (GoogleDoc): https://docs.google.com/document/d/1c7gdJsKIgaiENgDLAJ5hapSaJWJ9BEk5nKN7KPAmXxY/edit?usp=sharing

GCP host link for FastAPI - Swagger UI: https://nowcast-api-test-345519.ue.r.appspot.com/docs

Streamlit Cloud link: https://share.streamlit.io/krishna-aditi/host-nowcast-api/main/src/data/streamlit-app.py

==========================================================================

Weather briefing is a vital part of any flight preparation. The National Weather Service (NWS), Federal Aviation Administration (FAA), Department of Defense and other aviation groups are responsible for coherent and accurate weather reporting. The combined efforts of thorough scientific study and modeling techniques are able to predict the weather patterns with increasing accuracy. These weather forecasts enable pilots to make informed decisions regarding weather and flight safety.

### Weather Radar Observations
The weather radar data is provided by the national network of WSR-88D (NEXRAD) radars. This data is the major source of weather sensing used for Nowcasting. The WSR-88D (NEXRAD), also known as the Doppler Radar has two operational modes- clear air and precipitation. The mode is changed based on the weather condition. 

The NEXRAD radar image is not real time and can be upto 5 minutes old. If these images are older than it can lead to fatal accidents, as they have in the past. They are displayed as mosaic images that have some latency in creation, and in some cases the age of the oldest NEXRAD data in the mosaic can exceed the age indication in the cockpit by 15 to 20 minutes. Even small-time differences between age-indicator and actual conditions can be important for safety of flight. 
A better approach to solving this problem is by using the SEVIR Nowcast model which predicts a sequence of 12 images corresponding to the next hour of weather, based on the previously captured 13 images sampled at 5 minute intervals. 

#### Objective

The goal of the project is to implement a REST API to execute the GAN model, which takes a sequence of 13 images as input and generates 12 images as output. In this assignment we enable a User Interface on Streamlit. The module includes an API key authentication, only after which the user has access to the interface. All operations are enabled on Google Cloud Services. The final output is returned in the form of a GIF to the user. To overcome latency, the project also includes an Airflow module which will enable scheduling of the API run, so that the user can make use of cached images for closest location, instead of calling the model every single time. The list of inputs ingested by Airflow is supposed to be updated in a timely fashion.

##### JSON blueprint
```
{
 "lat":37.318363,
 "lon":-84.224203, 
 "radius":200,
 "time_utc":"2019-06-02 18:33:00",
 "model_type":"gan",
 "threshold_time_minutes":30,
 "closest_radius":true,
 "force_refresh":false
}
```

#### Requirements

To test pretrained models and train API requires 
```
- Python 3.7
- tensorflow 2.1.0
- pandas
- numpy
- Heroku
- Deta
- Streamlit
```
To visualize the outputs basemap library is required, which needs to following libraries
```
- h5py 2.8.0
- matplotlib 3.2.0
```

#### Workflow architecture

![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/Workflow.png)

#### FastAPI web-framework

![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/fastapidocs.png)

#### Streamlit

- Run the streamlit app using command on local
```
streamlit run app.py
```
- You can access the app from your browser on https://localhost:8501

- Alternatively, since the application is already hosted on Streamlit cloud, it can be accessed using the following link
    - Streamlit Cloud link: https://share.streamlit.io/krishna-aditi/host-nowcast-api/main/src/data/streamlit-app.py

- NOTE: You must provide the API key to be able to access the streamlit interface. 

![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/streamlit-1.png)
![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/streamlit-2.png)
![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/streamlit-3.png)
![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/streamlit-4.png)

#### Airflow

Apache Airflow is a workflow engine that will easily schedule and run your complex data pipelines. It will make sure that each task of your data pipeline will get executed in the correct order and each task gets the required resources. It provides amazing user interface to monitor and fix any issues that may arise.

For our project, it ingests batchInputs.txt file from the Google Cloud Storage which contains a list of JSON inputs. It processes these requests in an hourly basis and stores the outcome in a cache directory in the Cloud Storage Bucket.
```
# Switch to your airflow directory and inititalize the database
$ airflow db init

# Create a user account for Airflow
$ airflow users create --username admin --firstname <firstname> --lastname <lastname> --role Admin --email your@email.com

# Start webserver at port of choice
$ airflow webserver -p 8080
 
# Run the scheduler which runs as timed, and helps monitor the workflow 
$ airflow scheduler
```
![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/dags-list.png)
![image](https://github.com/krishna-aditi/Host-nowcast-API/blob/main/reports/figures/nowcast-dag.png)

#### References

- First Steps - FastAPI (https://fastapi.tiangolo.com/tutorial/first-steps/)
- Talks # 8: Sebastián Ramírez; Build a machine learning API  from scratch  with FastAPI (https://www.youtube.com/watch?v=1zMQBe0l1bM&ab_channel=AbhishekThakur)
- making gif from images using imageio in python - Stack Overflow (https://stackoverflow.com/questions/41228209/making-gif-from-images-using-imageio-in-python)
- Testing - FastAPI (https://fastapi.tiangolo.com/tutorial/testing/)
- https://www.youtube.com/watch?v=L0aXq0BEjbI&ab_channel=MarceloTrylesinski
- https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app
- https://www.youtube.com/watch?v=QdhwYWwYfc0&ab_channel=rithmic
- https://devcenter.heroku.com/articles/reducing-the-slug-size-of-play-2-x-applications
- https://fastapi.tiangolo.com/deployment/deta/
- https://devcenter.heroku.com/articles/error-codes#h10-app-crashed
- https://www.youtube.com/watch?v=XD7euLOzKbs&ab_channel=SFPython
- https://medium.com/google-cloud/set-up-anaconda-under-google-cloud-vm-on-windows-f71fc1064bd7
- https://medium.com/apache-airflow/a-simple-guide-to-start-using-apache-airflow-2-on-google-cloud-1811c2127445
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- https://www.analyticsvidhya.com/blog/2020/11/getting-started-with-apache-airflow/
- https://www.tutlinks.com/deploy-fastapi-app-on-google-cloud-platform/
- https://cloud.google.com/appengine/docs/standard#instance_classes


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Download all pre-trained Nowcast models
    │   ├── download_models.py
    |   └── model_urls
    |
    ├── notebooks          <- Jupyter notebook to invoke API
    │   └── invoke-api
    │
    ├── reports            <- Screenshots
    │   ├── figures
    |       ├── Curl-1.png
    |       ├── response.png
    │       └── Uvicorn.png
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   ├── nowcast_api.py
    │   │   ├── nowcast_helper.py
    │   │   ├── nowcast_main.py
    │   │   ├── nowcast_utils.py
    │   │   └── streamlit-app.py
    │   │
    │   ├── features       
    │   │   └── build_features.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io
 

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

--------

#### Submitted by:

![image](https://user-images.githubusercontent.com/37017771/153502035-dde7b1ec-5020-4505-954a-2e67528366e7.png)

#### **Contribution:**

#### **Attestation:**

WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.
