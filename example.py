from EnergyStarAPI import Energy_Star_Client

property_id = "4082666"

es_test_client = Energy_Star_Test_Client(username='username',password='password')
with open('test_account.xml','rb') as account:
	print(es_test_client.create_account(account_file=account))
