from addsslmoderequiretogreenplum import AddSsl as asr

import os

change working directory to C:\Sari\min\hachathon\workingdir

os.chdir('C:\\workingdir')



import configparser
config = configparser.ConfigParser()
config.read('config.ini')


tokenName = config['sara']['tokenName']
tokenCode = config['sara']['tokenCode']
site_id = config['sara']['site_id']


import tableauserverclient as TSC
server = TSC.Server('https://10ax.online.tableau.com/', use_server_version = True)

tableau_auth = TSC.PersonalAccessTokenAuth(token_name = tokenName, personal_access_token = tokenCode, site_id = site_id)
 
 
asr.validate_datasources(tableau_auth, 'results1.xlsx', server)



asr.update_datasources(tableau_auth, "credentials.xlsx", "results2.xlsx", server)

show results2.xlsx