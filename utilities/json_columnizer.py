import pandas as pd
import ast


def jcolumnize(df, column, prop, prefix, castlimit=False):
    # Set all null values in the selected column to a string representation of an empty list
    df.loc[df[column].isnull(), column] = '[]'
    # Do an evaluation of the selected column to convert all strings to lists
    try:
        df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x: ast.literal_eval(x))
    except:
        print("Exception doing literal eval on {}".format(column))
        
    # Replace the lists in the column with a new list of the values for the specified prop
    # Limit the number of items added to the list if castlimit = True (reduce number of cast members
    # to most significant in each movie)
    if not castlimit:
        df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x : [y[prop] for y in x])
    else:
        df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x : [y[prop] for y in x if y['order'] < 6])
    
    # Iterate over all rows to read the column lists and one-hot encode the values
    for index, row in df.iterrows():
        x = row[column]
        for y in x:
            columnName = prefix + '_' + str(y)
            df[columnName] = 1
            
    print("Columnized {} shape: {}".format(column, df.shape))
    
    return df

def collection_columnize(df, column):
    # Transform the values in the specified column to indicate whether the movie is part
    # of a collection or not, discarding the original data for which collection it is
    # part of
    df.loc[df[column].notnull(), column] = 1
    df.loc[df[column].isnull(), column] = 0
    
    print("Columnized {} shape: {}".format(column, df.shape))
    
    return df

def crew_columnize(df, column, prop, crew_type, prefix):
    # Set all null values in the selected column to a string representation of an empty list
    df.loc[df[column].isnull(), column] = '[]'
    # Do an evaluation of the selected column to convert all strings to lists
    try:
        df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x: ast.literal_eval(x))
    except:
        print("Exception doing literal eval on {}".format(column))
        
    # Create new column for pulling crew type
    df[crew_type] = [[] for i in range(df.shape[0])]
    
    # Set the crew type values in the column
    df[crew_type] = df.loc[df[column].notnull(), column].apply(lambda x : [y[prop] for y in x if y['job']==crew_type])
    
    df = jcolumnize(df, column, prop, prefix)
    
    return df
