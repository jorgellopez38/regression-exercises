import pandas as pd
import os
import numpy as np
import acquire
from sklearn.model_selection import train_test_split
from env import username, password, host 


#def delete_outliers(df):
#    '''This function deletes the outliers that are unrealistic for most of zillow customers'''
#    df = df[df.bathrooms <= 6]
    
#    df = df[df.bedrooms <= 6]

#    df = df[df.tax_value < 2_000_000]

#    df = df[df.square_feet < 10000]

#    return df


def acquire_zillow():
    '''
    This function checks to see if zillow.csv already exists, 
    if it does not, one is created
    '''
    #check to see if telco_churn.csv already exist
    if os.path.isfile('zillow.csv'):
        df = pd.read_csv('zillow.csv', index_col=0)
    
    else:

        #creates new csv if one does not already exist
        df = get_zillow_data()
        df.to_csv('zillow.csv')

    return df

def prep_zillow(df):
    '''
    This function takes in the zillow df
    then the data is cleaned and returned
    '''
    #change column names to be more readable
    df = df.rename(columns={'bedroomcnt':'bedrooms', 
                          'bathroomcnt':'bathrooms', 
                          'calculatedfinishedsquarefeet':'square_feet',
                          'taxvaluedollarcnt':'tax_value', 
                          'yearbuilt':'year_built',
                          'taxamount':'tax_amount'
                          })

    #drop null values (this is only 0.5% of df)
    df = df.dropna()

    #drop duplicates
    df.drop_duplicates(inplace=True)
    
    # convert some columns from floats to integers
    df["fips"] = df["fips"].astype(int)
    df["year_built"] = df["year_built"].astype(int)
    df["bedrooms"] = df["bedrooms"].astype(int)    
    df["tax_value"] = df["tax_value"].astype(int)
    df["square_feet"] = df["square_feet"].astype(int)
    
    # train/validate/test split
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)
    
    return train, validate, test


def wrangle_zillow():
    '''
    This function uses the acquire and prepare functions
    and returns the split/cleaned dataframe
    '''
    train, validate, test = prep_zillow(acquire_zillow())
    
    return train, validate, test

def scale_data(train, 
               validate, 
               test, 
               scale_cols=['bedrooms', 'bathrooms', 'tax_amount', 'sq_feet'],
               return_scaler=False):
    '''
    Scales the 3 data splits. 
    Takes in train, validate, and test data splits and returns them scaled.
    If return_scalar is True, the scaler object will be returned as well
    '''
    # make copies of the original data so no leakage
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    # variable 
    mm_scaler = MinMaxScaler()
    # fit it to scaler
    mm_scaler.fit(train[columns_to_scale])
    # scaling train, validate, test, and columns
    train_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(train[columns_to_scale]),
                                                  columns=train[columns_to_scale].columns.values).set_index([train.index.values])
                                                  
    validate_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(validate[columns_to_scale]),
                                                  columns=validate[columns_to_scale].columns.values).set_index([validate.index.values])
    
    test_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(test[columns_to_scale]),
                                                 columns=test[columns_to_scale].columns.values).set_index([test.index.values])
    
    if return_scaler:
        return mm_scaler, train_scaled, validate_scaled, test_scaled
    else:
        return train_scaled, validate_scaled, test_scaled