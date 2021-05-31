import tableauserverclient as TSC
import os
import pandas as pd
from addsslmoderequiretogreenplum import Datasource
from tableauserverclient import ConnectionCredentials, ConnectionItem


def delete_tdsx():
    directory = os.getcwd()
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".tdsx")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)

def validate_datasources(tableau_auth, output_file):
    result_df = ssl_validation(tableau_auth)
    result_df.to_excel(output_file, index = False)



def ssl_validation(tableau_auth):
    starting_df = pd.DataFrame(columns=['luid', 'ssl', 'server', 'class', 'name', 'project', 'username'])
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        for ds in TSC.Pager(server.datasources):
            server.datasources.populate_connections(ds)
            for con in ds.connections:
                if con._connection_type == 'greenplum':
                    server.datasources.download(ds.id,  include_extract = False)
                    sourceTDS = Datasource.from_file((os.getcwd()+"\\"+ds.name+'.tdsx'))
                    conn = sourceTDS.connections
                    for connection in conn:
                        new_row = {'luid' : ds.id, 'ssl': connection.sslmode, 'server': connection.server, 'class' : connection._class, 'name' : ds.name, 'project' : ds._project_name, 'username': con.username}
                        starting_df = starting_df.append(new_row, ignore_index = True)
    delete_tdsx()
    return starting_df

def parse_ssl(tdsx_to_parse):
    sourceTDS = Datasource.from_file(tdsx_to_parse)
    conn = sourceTDS.connections
    for connection in conn:
        if connection.dbclass == 'greenplum':
            connection.sslmode = 'require'
        sourceTDS.save()


def update_datasources(tableau_auth, password_file, output_file):
    password_file = pd.read_excel(password_file)
    result_df = ssl_validation(tableau_auth)
    result_df = result_df.merge(password_file, how = 'inner', right_on = 'username', left_on = 'username')
    with server.auth.sign_in_with_personal_access_token(tableau_auth):
        for i in range(len(result_df)):
            fptdsx = os.getcwd()+"\\"+result_df.loc[i,'name']+'.tdsx'
            if starting_df.loc[i, 'ssl'] != 'require' and starting_df.loc[i, 'class'] == 'greenplum':
                datasource = server.datasources.get_by_id(result_df.loc[i,'luid'])
                server.datasources.download(result_df.loc[i,'luid'], include_extract = True)
                parse_ssl(fptdsx)
                z = ConnectionCredentials(name=result_df.loc[i,'username'], password=result_df.loc[i,'username'], embed=True)
                server.datasources.publish(datasource, fptdsx, TSC.Server.PublishMode.Overwrite, connection_credentials=z)
    delete_tdsx()
    validate_datasources(tableau_auth, output_file)  




