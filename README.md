# weatherPredict
Python application to predict weather based on windowing technique
The paper on which the algorithm is based is : https://www.hindawi.com/journals/isrn/2013/156540/

I tested the applications's outputs with weather predictions as given in websites like accuweather.com and weather underground and found the results to be over 90% correct. The accuracy is reduced due to variations in seasonal change. I have tested also with predictions using neural networks, but there was no dramatic change in the predictions. 

The beauty of this algorithm is that it lends itself to scale, parallelism in processing and aggregation and distributed structure to predict using simple devices. Also as the processing, storage and other requirements are low, this can be used directly on low power devices like the raspberry pi.


Usage :
Currently the application uses Python 2.7, Pandas, numpy and Scipy. The tests use matplotlib and seaborn, but these are optional.
Install Python2.7, pandas, numpy and scipy.
Copy all files of this application into a folder.
Create a folder called weatherData and move the weather20042013.csv to it.
From commandline run :
    python weatherHelper.py --> to predict weather parameters for a given date
