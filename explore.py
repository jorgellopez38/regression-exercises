import seaborn as sns 
import pandas as pd
import numpy as np

def plot_variable_pairs(train, cont_var, cat_var):
    # columns    
    cat_var = ['bedrooms', 'bathrooms', 'fips']
    cont_var = ['square_feet', 'tax_amount', 'tax_value', 'year_built']

    # plots
    sns.lmplot(x='tax_value', y='square_feet', data=train.sample(1000), scatter=True)
    sns.lmplot(x='tax_value', y='year_built', data=train.sample(1000), scatter=True)
    sns.lmplot(x='tax_value', y='tax_amount', data=train.sample(1000), scatter=True)


     
    return train, cont_var, cat_var

def plot_categorical_and_continuous_vars(train, cont_var, cat_var):
    
    # columns    
    cat_var = ['bedrooms', 'bathrooms', 'fips']
    cont_var = ['square_feet', 'tax_amount', 'tax_value', 'year_built']
    
    # plots
    sns.boxplot(x='bedrooms', y='tax_value', data=train.sample(1000))
    plt.show()
    sns.violinplot(x='bathrooms', y='tax_value', data=train.sample(1000))
    plt.show()
    sns.barplot(x='fips', y='tax_value', data=train.sample(1000))
    plt.show()
    
    return train, cont_var, cat_var