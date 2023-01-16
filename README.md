### about:
**finnews** is my final project for [Harvard CS50P](https://www.edx.org/course/cs50s-introduction-to-programming-with-python).
going to rebrand as **tradingbuddy**

given list of symbols, download 3 months of historical closes, generate .pdf with...

* X current price relative to 3-month high and low
* X daily move standard deviations
* X 5-day forecast
    * chart with price cone?
* X 3-month percent return
* ... pairs trading ratios?
* ... hedge ratios?

broken up into five main asset classes
* ***equities:*** /MES, /MNQ, /MYM, /M2K
* ***interest rates:*** /2YY, /5YY, /10Y, /30Y
* ***cryptos:*** /MBT, /MET
* ***foreign exchange:*** /M6E, /M6A, /M6B
* ***commodities:*** /MGC, /SIL, /MHG, /MCL

### schema (draft)
![alt text](static/schema.png)

#### currently supports:
* data download from databento
* statistical calculations
* preliminary, hard-coded .pdf generation

#### in development:
1. databento data pulls
    * product_id is set by the publisher? [can be matched](https://bit.ly/3jTtQsB)
2. pandas statistcal analysis
    * roll these into class attributes
3. matplotlib / plotly visualizations
4. pyfpdf report generation
5. ... aws pdf hosting & mailchimp automations?

#### notes:
* [databento docs](https://docs.databento.com/)
* [databento python wrapper](https://bit.ly/3Iu88pi)
* [databento smart symbology](https://bit.ly/3ilxrza)

***
### reference:

#### virtual environments
Create a Python3 Virtual Environment: 
```python3 -m venv env```

Activate the Virtual Environment:
```source env/bin/activate```

Deactivate the Virtual Environment:
```deactivate```

To Remove a Virtual Environment:
```sudo em -rf venv```

***
#### requirements.txt
Automagically create a requirements.txt file:
```pip3 freeze > requirements.txt```

Start the Flask Server:
```flask run```

Run the Flask Server in Debug Mode:
```flask --app app.py --debug run```
