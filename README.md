# Data Engineer Excercise

This project is an excercise about Data Engineering, focus on basic tasks of data processing, MongoDB, Beanie and using API to enrich the data.

## MongoDB & Beanie

In the folder **mongo_beanie** there is a Python file *mongo_beanie.py*, which contains the code for accessing to MongoDB using Beanie, an asynchronous Python object-document mapper (ODM) for MongoDB.
Just use ``` python3 mongo_beanie.py``` to run the file. This will initialize the Lead and Persona collection (if not exists) in the _test_db_ database. The code will also perform some basic operations such insert, update and find the relevant documents related to the search criteria.

## CSV Data Processing

The Data Processing part is included in the folder **data_processing**. 
For better demonstration, Jupyter Notebook is used to perform the data cleaning and make some statistics of the given CSV file.
Because this file is pretty much "dirty", some efforts were made to fill in the field that might need for future of ML/DS tasks using KNN.

## API

The folder **api** contains the code for using the API.
For simulation, a simple application using Flask in *mock_test_api.py* will be hosted to return the example JSON. Once the file *call_api.py* is triggered, a JSON document will be received and processed.
To run this, please run the application in *mock_test_api.py* first. Then run the file *call_api.py* to get the required JSON.

## Comparing Mongo GridFS vs S3

The choice between AWS S3 & MongoDB GridFS for JSON will depend on the specific use case, the access pattern, scalability needs and also cost considerations.
While **S3** will be a better options if you need the *durability, availability, scalability* and also easy to *integrate with cloud services*, **MongoDB GridFS** is a good idea because it is *powerful, complexible queries on documents* and *fully-integrated with MongoDB*.
In this excercise, since we are already using MongoDB and still need to do some updates on documents, MongoDB GridFS will be a better choice to mange everything in a single system.
The code demonstrate for Read and Write in GridFS is located in folder **gridfs**.

