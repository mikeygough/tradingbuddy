### About:
**finnews** is my final project for [Harvard CS50P](https://www.edx.org/course/cs50s-introduction-to-programming-with-python).

given list of symbols, download 3 months of historical closes, generate .pdf with...

* X current price relative to 3-month high and low
* X daily move standard deviations
* X 5-day forecast
* X 3-month percent return
* ... pairs trading ratios?
* ... hedge ratios?

#### currently supports:
* data download from databento
* statistical calculations

#### in development:
1. databento data pulls
    * product_id is set by the publisher? [can be matched](https://bit.ly/3jTtQsB)
2. pandas statistcal analysis
    * roll these into class attributes
3. matplotlib / plotly visualizations
4. pypdf report generation
5. ... aws pdf hosting & mailchimp automations?

#### notes:
* [databento docs](https://docs.databento.com/)
* [databento python wrapper](https://bit.ly/3Iu88pi)
* [databento smart symbology](https://bit.ly/3ilxrza)

***
### Reference:

#### Virtual Environments
Create a Python3 Virtual Environment: 
```python3 -m venv env```

Activate the Virtual Environment:
```source env/bin/activate```

Deactivate the Virtual Environment:
```deactivate```

To Remove a Virtual Environment:
```sudo em -rf venv```

***
#### Requirements.txt
Automagically create a requirements.txt file:
```pip3 freeze > requirements.txt```

Start the Flask Server:
```flask run```

Run the Flask Server in Debug Mode:
```flask --app app.py --debug run```
