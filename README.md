# add-sslmode-require-to-greenplum

## Installation

Tool can be installed with pip install -e 'download location'

## Running the tool

Sample.py shows commands which should be executed in Python console

## Config

site_id, token_name and personal_access_token can be specified in config.ini

## Functions

### validate_datasources function

validates sslmode status and outputs excel file

### update_datasources function

both validates and updates sslmode where applicable
Credentials should be provided in excel for republishing


## Warning

Tool only works with data source names without special characters


