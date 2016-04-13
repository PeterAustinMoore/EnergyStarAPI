# EnergyStarAPI
EnergyStar API Python connector

##About
Created on 4/13/2016
Author Peter Moore

##Getting Started
The connector has two major classes:

1. Energy_Star_Test_Client
2. Energy_Star_Cleint

Both are initiated in a similar fashion:

<code>
>>> from EnergyStarAPI import Energy_Star_Test_Client, Energy_Star_Client
>>> ES_test_client = Energy_Star_Test_Client(username='myportfoliousername', password='mypassword')
</code>

_note:_ for testing, you must create a new account using
	with open('xml-templates/account.xml','rb') as new_account:
		ES_test_client.create_account(new_account)

	Once this is successfully created, use the new credentials as the authentication

	new_test_client = Energy_Star_Test_Client(
		username='new_account_Username',
		password='new_account_password'
		)

	


