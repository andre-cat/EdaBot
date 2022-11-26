import pandas as __pd # type: ignore
import sys as __sys
from eda_bot import commons as __commons
__pd.options.display.float_format = "{:.2f}".format

def __rename_survived(table):
    mapping={0:'N',1:'Y'}
    table['survived']=table['survived'].map(mapping)
    return table

def __split_name(table):
    def split_name_series(string):
        name, last_name=string.split(', ')
        return __pd.Series((name,last_name),index='firstname lastname'.split())
    sub_table=table['name'].apply(split_name_series)
    table[sub_table.columns]=sub_table
    return table

def __rename_sex(table):
    mapping={'male':'M','female':'F'}
    table['sex']=table['sex'].map(mapping)
    return table

def __rename_ticket(table):
    mapping={1:'1st',2:'2nd',3:'3rd'}
    table['pclass']=table['pclass'].map(mapping)
    return table

def __impute_age(table, age_map):
    sub_table=table.loc[table['age'].isna(),'pclass'].map(age_map)
    table.loc[table['age'].isna(),'age']=sub_table
    return table

def __group_age(table):
    bins=[0, 3, 13, 17, 29, 44, 59, __sys.maxsize]
    labels=['Baby',       #0-3
            'Child',      #4-13
            'Teen',       #14-17
            'YoungAdult', #18-29
            'Adult',      #30-44
            'MiddleAged', #45-59
            'Elder']      #60-in
    age_group=__pd.cut(table['age'], bins=bins, labels=labels,ordered=True)
    table['agegroup']=age_group
    return table

def get_data() -> __pd.DataFrame:
    try:
        data = __pd.read_csv(__commons.get_path('eda_bot\\sources\\texts','titanic.csv'))
        data = data.rename(columns=str.lower)
        data = data.pipe(__rename_survived)
        data=data.pipe(__split_name)
        data=data.pipe(__rename_sex)
        data = data.pipe(__rename_ticket)
        medians = data.groupby(['pclass'])['age'].median().to_dict()
        data=data.pipe(__impute_age, medians)
        data=data.pipe(__group_age)
        
        data['passengerid'] = data['passengerid'].astype('int')
        data['survived'] = data['survived'].astype('category')
        data['pclass'] = data['pclass'].astype('category')
        data['name'] = data['name'].astype('object')
        data['sex'] = data['sex'].astype('category')
        data['age'] = data['age'].astype('int')
        data['sibsp'] = data['sibsp'].astype('int')
        data['parch'] = data['parch'].astype('int')
        data['ticket'] = data['ticket'].astype('object')
        data['fare'] = data['fare'].astype('float')
        data['cabin'] = data['cabin'].astype('object')
        data['embarked'] = data['embarked'].astype('category')
        data['firstname'] = data['firstname'].astype('object')
        data['lastname'] = data['lastname'].astype('object')
        data['agegroup'] = data['agegroup'].astype('category')
    
        return data 
    except Exception as e:
        raise(e.with_traceback())