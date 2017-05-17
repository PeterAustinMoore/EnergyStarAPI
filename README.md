# EnergyStarAPI
EnergyStar API Python connector

## About
Created on 4/13/2016

Author Peter Moore

## Getting Started
The connector has two major classes:

1. EnergyStarTestClient
2. EnergyStarClient

Both are initiated in a similar fashion:
```python
from EnergyStarAPI import EnergyStarTestClient, EnergyStarClient
ES_test_client = EnergyStarTestClient(username='myportfoliousername', password='mypassword')
ES_client = EnergyStarClient(username='myusername',password='mypassword')
```
_note:_ for testing, you must create a new account by first updating your email address in [test_account.xml](xml-templates/test_account.xml) and then running:
```python
with open('xml-templates/account.xml','rb') as new_account:
	ES_test_client.create_account(new_account)
```
Once this is successfully created, use the new credentials as the authentication
```python
new_test_client = EnergyStarTestClient(
	username='new_account_Username',
	password='new_account_password'
	)
```
Full documentation can be found `https://portfoliomanager.energystar.gov/webservices/home`

## Responses

Successful EnergyStar API calls return XML responses that need to be parsed.

Errors are, unfortunately, not uniformly returned (either as HTML or XML). Therefore the full text of error response is returned at this time.

## Functions

	get_account_info()

Returns: account information (XML)
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<account>
	<id>12341</id>
	<username>joebobonejob</username>
	<password>*********</password>
	<webserviceUser>true</webserviceUser>
	<searchable>true</searchable>
	<includeTestPropertiesInGraphics>true</includeTestPropertiesInGraphics>
	<contact>
		<address address1="2412 First St" address2="Apt 222" city="St Petersburg" state="FL" postalCode="61234" country="US"/>
		<email>temp@aol.com</email>
		<firstName>Joe</firstName>
		<phone>1234123412</phone>
		<lastName>Bob</lastName>
		<jobTitle>Data Analyst</jobTitle>
	</contact>
	<organization name="FirstAnalytics">
		<primaryBusiness>Data Center</primaryBusiness>
		<energyStarPartner>false</energyStarPartner>
	</organization>
	<securityAnswers/>
</account>```


```python
get_building_info(prop_id)```

Returns: building information (XML)
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<building>
	<name>1234 ABC Building</name>
	<address address1="1234 ABC St." city="Newark" state="NJ" postalCode="09231" county="Newark" country="US"/>
	<constructionStatus>Existing</constructionStatus>
	<primaryFunction>Data Center</primaryFunction>
	<yearBuilt>1910</yearBuilt>
	<grossFloorArea units="Square Feet" temporary="false" default="N/A"><value>4800</value></grossFloorArea>
	<occupancyPercentage>25</occupancyPercentage>
	<isFederalProperty>false</isFederalProperty>
	<accessLevel>Read</accessLevel>
	<audit>
		<createdBy>Joe</createdBy>
		<createdByAccountId>11111</createdByAccountId>
		<createdDate>2014-06-18T12:27:24.000-04:00</createdDate>
		<lastUpdatedBy>Joe</lastUpdatedBy>
		<lastUpdatedByAccountId>11111</lastUpdatedByAccountId>
		<lastUpdatedDate>2016-03-18T14:25:57.000-04:00</lastUpdatedDate>
	</audit>
</building>
```

```python
get_meter_list(prop_id)
```

Returns a dictionary of meters and their types associated with the property

```json
{123456:'Electric',4401234:'Natural Gas',1350101:'Municipally Supplied Potable Water - Mixed Indoor/Outdoor'}
```
```python
get_meter_type(meter_id)
```
Returns the type of meter

	'Electric' 'Natural Gas' 'Municipally Supplied Potable Water - Mixed Indoor/Outdoor' etc

```python
get_usage(meter_id, months_ago)
```
Returns an array of monthly usage for the meter from the specified months ago

```json
[{'2016-03-31':102},{'2016-04-30':94.5}]
```
```python
get_cost(meter_id, months_ago)
```
Returns an array monthly cost for the meter from the specified months ago

```json
[{'2016-03-31':23.5},{'2016-04-30':20.9}]
```
```python
get_usage_and_cost(meter_id, months_ago)
```

Returns an array of monthly usage and cost from the specified months ago
```json
[{'2016-03-31':[102,23.5]},{'2016-04-30':[94.5,20.9]}]
```
