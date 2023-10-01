import pandas as pd
import datetime


def results_to_df(results, total_pages):
    '''
    Save the json results as a dataframe and return the resulting dataframe
    '''

    df = pd.DataFrame.from_dict(results['elementList'])

    return df


def df_to_file(df):
    '''
    Stores pd.DataFrame as Excel file.
    '''

    date = str(datetime.date.today())
    file_path = f'idealista_{date}.xlsx'

    df = df.reset_index()
    df.to_excel(file_path, index=False)
