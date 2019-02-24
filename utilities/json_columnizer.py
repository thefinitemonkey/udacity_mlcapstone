import pandas as pd
import ast


def jcolumnize(df, column, prop, prefix, castlimit=False):
    df.loc[df[column].isnull(), column] = "[]"
    df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x: ast.literal_eval(x))
    if not castlimit:
        df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x : [y[prop] for y in x])
    else:
        df.loc[df[column].notnull(), column] = df.loc[df[column].notnull(), column].apply(lambda x : [y[prop] for y in x if y["order"] < 6])
    
    for index, row in df.iterrows():
        x = row[column]
        for y in x:
            columnName = prefix + "_" + str(y)
            df[columnName] = 1
            
    print("jcolumnize shape: {}".format(df.shape))
    return df

def collection_columnize(df, column):
    df.loc[df[column].notnull(), column] = 1
    df.loc[df[column].isnull(), column] = 0
    return df