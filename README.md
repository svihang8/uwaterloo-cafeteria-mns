# UWaterloo Cafeteria MNS

UWaterloo Cafeteria MNS is an attempt to automate and remove the stress of detection of allergens with regards to the menu at the University of Waterloo Cafeteria. Inspired by an incident that could have proven dangerous and harmed the health of my peers, this project sources data from the University of Waterloo Website and sends realtime notifications to clients to food that contains any allergens client may have, using SMS.

Frontend (client-facing) application of code can be found at ...
Backend application is made serverless using AWS Lambda and AWS EventBridge.

## Note
Due to unforeseen circumstances, AWS cost services have hampered the ability to deploy the program. However, under information regarding deployment, screenshots and the process has been described.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
You will need python installed on your local environment.
You will need MySQL installed on your local environment.
You will require API keys from Twilio.
You will need to setup a local database.

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be
Clone repository.
```
git clone https://github.com/svihang8/food-app-frontend
```

Use python environment from git repository directory cafeteria-env.
```
source cafeteria-env/bin/activate
```
Install required packages.
```
pip3 install -r requirements.txt
```

Add env file with required variables.

## Deployment
Following project was deployed using following methodology.
Currently, project is not deployed.

Database
Database was hosted using AWS RDS services.
Following tutorial can be referred to. https://aws.amazon.com/getting-started/hands-on/create-mysql-db/

Pipeline
lambda function was created to host function.
lambda function code can be found in repository directory /lambda.
AWS layers were used from https://github.com/keithrozario/Klayers

Notification
lambda function was created to host function.
lambda function code can be found in repository directory /lambda.
AWS layers were used from https://github.com/keithrozario/Klayers.

Backend API Functions
api functions to manage registration were hosted using lambda functions,
and API Gateway triggers.
lambda function code can be found in repository directory /lambda.

## Built With

* [Python](https://docs.python.org/3/) - programming language.
* [AWS-Lambda](https://docs.aws.amazon.com/lambda/) - serverless computing platform.
* [Beautiful-Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML parser.
* [Pandas](https://pandas.pydata.org/docs/) - data mannipulation library.
* [Twilio](https://www.twilio.com/docs) - programmable communication service.
* [my-sql-connector](https://dev.mysql.com/doc/connector-python/en/)  - object-relational mapping.

## Contributing
To contribute, open issue on GitHub.
Current features working on include CRUD web application to handle data management.
Detecting potential ingredients using sourced data in database and other sources.

## Authors
* **Vihang Shah** - https://github.com/svihang8 - *end to end application* - [svihang8](https://github.com/svihang8)
