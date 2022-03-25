Hosting SEVIR Nowcast API using Streamlit and Heroku
==============================

Report link (GoogleDoc): https://docs.google.com/document/d/1c7gdJsKIgaiENgDLAJ5hapSaJWJ9BEk5nKN7KPAmXxY/edit?usp=sharing

============================================================================================

Weather briefing is a vital part of any flight preparation. The National Weather Service (NWS), Federal Aviation Administration (FAA), Department of Defense and other aviation groups are responsible for coherent and accurate weather reporting. The combined efforts of thorough scientific study and modeling techniques are able to predict the weather patterns with increasing accuracy. These weather forecasts enable pilots to make informed decisions regarding weather and flight safety.

### Weather Radar Observations
The weather radar data is provided by the national network of WSR-88D (NEXRAD) radars. This data is the major source of weather sensing used for Nowcasting. The WSR-88D (NEXRAD), also known as the Doppler Radar has two operational modes- clear air and precipitation. The mode is changed based on the weather condition. 

The NEXRAD radar image is not real time and can be upto 5 minutes old. If these images are older than it can lead to fatal accidents, as they have in the past. They are displayed as mosaic images that have some latency in creation, and in some cases the age of the oldest NEXRAD data in the mosaic can exceed the age indication in the cockpit by 15 to 20 minutes. Even small-time differences between age-indicator and actual conditions can be important for safety of flight. 
A better approach to solving this problem is by using the SEVIR Nowcast model which predicts a sequence of 12 images corresponding to the next hour of weather, based on the previously captured 13 images sampled at 5 minute intervals. 

#### Objective

The goal of the project is to implement a REST API to execute the GAN model, which takes a sequence of 13 images as input and generates 12 images as output. The end users, who are a bunch of developers who want to integrate our API with their system, pass a JSON file as a blueprint with all required parameters through CURL, POSTMAN, or a Python-Client to execute the model. 

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
#### Streamlit

- Run the streamlit app using command 
```
streamlit run app.py
```
- You can access the app from your browser on https://localhost:8501

#### Heroku 

Heroku is a container-based cloud Platform as a Service (PaaS). Developers use Heroku to deploy, manage, and scale modern apps. Our platform is elegant, flexible, and easy to use, offering developers the simplest path to getting their apps to market. Heroku has a size limitation of 500MBs, due to which it was not possible to host the SEVIR Nowcast API on the server. This slugsize includes all the dependencies and the build of the API, which exceeds 500MBs under all circumstances.

#### Deta

Deta — “the cloud for doers and dreamers” as mentioned on its home page — is a relatively new and fully free cloud service provider. It offers a developer-friendly interface that allows you to deploy your program to the cloud in a matter of seconds. 

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
