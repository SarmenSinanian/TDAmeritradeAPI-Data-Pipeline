# TDAmeritradeAPI-Data-Pipeline
This is a robust data pipeline project that leverages the TDAmeritrade API to create an automated daily downloader for all expiry dates of QQQ option chains. The pipeline involves several key stages:

Data Ingestion: Data is fetched daily from the TDAmeritrade API. Automated downloads are scheduled via the Windows Task Scheduler and a batch file targeting the appropriate script.

Data Preprocessing: The fetched data is then converted into a more accessible JSON format, and further normalized into a pandas DataFrame for convenient manipulation and analysis.

Data Transformation: A series of transformations are performed on the data, including selecting relevant categories and splitting the data into individual pandas DataFrames for each unique expiry date.

Data Storage: The transformed data is stored locally in a pickle file for easy retrieval. Each day's data is stored under a key corresponding to the date of retrieval, ensuring historical data is retained for trend analysis.

The objective is to run machine learning models on Open Interest and other 'Greek' metrics after accumulating sufficient data over a period of 2-3 months (Data collection began on 05-05-2022). This will help in deriving valuable insights from the options market, and informing strategic trading decisions.
