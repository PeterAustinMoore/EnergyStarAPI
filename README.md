# EnergyStarAPI
EnergyStar API Python connector

##About
Created on 4/13/2016

Author Peter Moore

## Getting Started
The connector has two major classes:

1. Energy_Star_Test_Client
2. Energy_Star_Cleint

Both are initiated in a similar fashion:

	from EnergyStarAPI import Energy_Star_Test_Client, Energy_Star_Client
	ES_test_client = Energy_Star_Test_Client(username='myportfoliousername', password='mypassword')
	ES_client = Energy_Star_Client(username='myusername',password='mypassword')

_note:_ for testing, you must create a new account using
	
	with open('xml-templates/account.xml','rb') as new_account:
		ES_test_client.create_account(new_account)

Once this is successfully created, use the new credentials as the authentication

	new_test_client = Energy_Star_Test_Client(
		username='new_account_Username',
		password='new_account_password'
		)

Full documentation can be found `https://portfoliomanager.energystar.gov/webservices/home`

## Responses

Successful EnergyStar API calls return XML responses that need to be parsed.

Errors are returned, unfortunately, not uniformly returned (either as HTML or XML). Therefore the full text of error response is returned at this time.

## Functions

	get_account_info()

Test: Yes
Live: Yes

Returns: account information (XML)

