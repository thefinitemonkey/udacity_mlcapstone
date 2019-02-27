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
        df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x :\
           [y[prop] for y in x if y['order'] < 6])
        
    # Create a new dataframe to hold all the arrays in the given column and put the values
    # from the column into a list
    tf = df.loc[df[column].notnull(), column]
    tl = []
    for x in tf:
        for y in x:
            tl.append(y)
            
    # Dedup the items in the list
    tl = list(dict.fromkeys(tl))
    
    # Create columns from the list items in the source dataframe and set to default of 0
    for item in tl:
        df[prefix + str(item)] = [0 for i in range(df.shape[0])]
    
    # Iterate over all rows to read the column lists and one-hot encode the values
    for index, row in df.iterrows():
        x = row[column]
        for y in x:
            columnName = prefix + str(y)
            df.at[index, columnName] = 1
            
    print("Columnized {} shape: {}".format(column, df.shape))
    
    return df

def originalLanguage(df, column, prefix):
    # Create a new dataframe to hold all the values from the column
    tf = df.loc[df[column].notnull(), column]
    tl = []
    for x in tf:
        tl.append(x)
    
    #Dedup the list
    tl = list(dict.fromkeys(tl))
    
    # Create columns from the list items in teh source dataframe and set to default of 0
    for item in tl:
        df[prefix + str(item)] = [0 for i in range(df.shape[0])]
        
    # Iterate over all rows to read the column values and one-hot encode them
    for index, row in df.iterrows():
        x = row[column]
        columnName = prefix + str(x)
        df.at[index, columnName] = 1
        
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
    
    # Create a new dataframe to hold all the arrays in the given column and put the values
    # from the column into a list
    tf = df.loc[df[crew_type].notnull(), crew_type]
    tl = []
    for x in tf:
        for y in x:
            tl.append(y)
            
    # Dedup the items in the list
    tl = list(dict.fromkeys(tl))
    
    # Create columns from the list items in the source dataframe and set the default to 0
    for item in tl:
        df[prefix + str(item)] = [0 for i in range(df.shape[0])]
    
    # Iterate over all rows to read the column lists and one-hot encode the values
    for index, row in df.iterrows():
        x = row[crew_type]
        for y in x:
            columnName = prefix + str(y)
            df.at[index, columnName] = 1
            
    print("Columnized {} shape: {}".format(column, df.shape))
    
    return df

def columnBooleanize(df, column):
    df.loc[df[column].notnull(), column] = 1
    df.loc[df[column].isnull(), column] = 0
    
    return df
