import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
import tc.config as config

def standardize_columns(df, columns_to_standardize):
     scaler = StandardScaler()
     #df[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])
     #df[columns_to_standardize] = preprocessing.scale(df[columns_to_standardize])
     column_means =df[columns_to_standardize].mean()
     column_stds = df[columns_to_standardize].std(ddof=1)

        # Update the original DataFrame with standardized values
     df[columns_to_standardize] = (df[columns_to_standardize] - column_means) / column_stds
     return df








# def calculate_sum_last_n_columns(df, cases):
#     new_columns = []  # To store the names of the new columns

#     for prefix, values in cases.items():
#         for value in values:
#             column_name = f'Sum_last_{value}_{prefix}'
#             relevant_columns = df.filter(like=prefix).columns[-value:]  # Get relevant columns
#             df[column_name] = df[relevant_columns].sum(axis=1)  # Calculate sum along rows
#             new_columns.append(column_name)

#     # Creating a new DataFrame with only the required columns
#     result_df = pd.concat([df['HCP_ID']] + [df[new_col] for new_col in new_columns], axis=1)
#     return result_df

import pdb

import pandas as pd

def calculate_sum_last_n_columns(df,pre_post_df,cases,variables,mapping_month):
    new_columns = []  # To store the names of the new columns

    for prefix, values in cases.items():
        for value, positions in values.items():
            for position in positions:
                column_name = f'Sum_last_{value}_{prefix}_{position}'
                relevant_columns = [var for var in variables if prefix in var]
                if position == 'pre':
                   relevant_columns=relevant_columns[:pre_post_df['total_months_pre']]
                elif position == 'post':
                   index=relevant_columns.index([col for col in relevant_columns if f'_{mapping_month}' in col][0])
                   relevant_columns=relevant_columns[index:len(relevant_columns)]
                else:
                    raise ValueError("Position must be either 'pre' or 'post'")
                
                # Exclude the Sum_ columns from relevant_columns
                relevant_columns = [col for col in relevant_columns if not col.startswith('Sum_')]
                print(relevant_columns)
                df[column_name] = df[relevant_columns].sum(axis=1)  # Calculate sum along rows
                new_columns.append(column_name)

    # Creating a new DataFrame with only the required columns
    result_df = pd.concat([df[config.hcp_identifier]] + [df[new_col] for new_col in new_columns], axis=1)
    result_df['segment_var']=df['segment_var']
    return result_df




