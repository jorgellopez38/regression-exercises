import pandas as pd
import numpy as np
import os
from env import get_connection


def new_zillow_data():
    '''
    This function reads the zillow data from the Codeup db into a df.
    '''
    # Create SQL query.
    sql_query =  '''SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, 
                    yearbuilt, taxamount, fips FROM properties_2017 JOIN propertylandusetype USING(propertylandusetypeid) 
                    WHERE propertylandusedesc = "Single Family Residential";'''
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df

def get_zillow_data():
    '''
    This function reads in zillow data from Codeup db, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('zillow_df.csv'):
        
        # If csv file exists, read in data from csv file.
        df = pd.read_csv('zillow_df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame.
        df = new_zillow_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('zillow_df.csv')
        
    return df

