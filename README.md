# HCSS text analysis: discussions of AI in Defense in Dutch Parliament

This project examines discussions held by Dutch politicians in both the Lower and Upper Houses on key topics highlighted at the REAIM summit, including artificial intelligence, machine learning, and other advanced military technologies. By analyzing a large dataset of speeches and associated metadata, the study explores not only the overall sentiment but also the underlying trends in support and opposition. The analysis further investigates how factors such as gender, political orientation, and age correlate with attitudes toward these emerging technologies, offering a deeper insight into the topic. Only the data from 2022 was taken for this analysis, since the topic of military technologies got significantly more discussed after the Russian invasion in Ukraine in 2022, and hardly brought up earlier.

The usage of this project consists with two parts - front end and back end

### Back end

Firstly, please run the following script to get all the necessary dependencies for this project -pip install -r requirements. txt.
After the installation is successful, please navigate towards the create_data.py. By default, this project already has the
csv file with necessary data in the data folder for the fast work with it, however, in case you want to get the
dataframe with sentiment analysis and additional features locally or save the new csv with new key words, please make use of the function `get_data`.

### Front end

The web version of this app is already deployed and could be found by link `https://bohdan-markiv-hcss-assessment-front-end-front-end-hy23wp.streamlit.app/` .
For the local development you need to run in the terminal command `streamlit run front_end.py`, as all the graphs
are currently saved in the file `front_end.py`. Currently, the data is taken from the saved csv file, as it allows for a fast load
of data for the app, but in the future the whole pipeline could be combined - from getting the data, to showing it in the app.\
The app includes:

- Topic filtering and keyword search
- Correlation & sentiment analysis
- Frequency trends over time
- Speaker-level and party-based visual insights
