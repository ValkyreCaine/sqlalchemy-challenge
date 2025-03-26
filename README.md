# sqlalchemy-challenge

Hello and welcome to my SQLAlchemy Challenge! 

Here you will find a whole host of goodies, the most important being the climate.ipynb which houses all of my code for the data transforamtions to get to the juicy parts of Honolulu's climate for this vacation. Another key player to look out for is the app.py, this hosts my climate app! Like any new apps there can always be bugs and spcefic way's to use it so further in I will give you some hints and nuance to consider! 

In the roesources folder, you will find the csv's used in this analysis both for the 9 stations and their measurements. The SQL database is also included in this folder as well. 

On to the nitty gritty:
You should have no issues running the climate file, but in the app, here are some things to consider. 

When using the start directory, the first date included is January 1st of 2010, consider adding "/api/v1.0/2010-01-01" to the end of the web address to specify this end point. 
Additionally, if you want to look at the most recent data points over a year consider adding "/api/v1.0/2017-08-23/2017-01-01" as the endpoint of the web address to look at the start and end of the data readings of the most recent recordings. 

As always, please let me know if you run into any issues with my submission. All code was written by me using class materials and the class AI tool for troubleshooting. 

Thank you! 
