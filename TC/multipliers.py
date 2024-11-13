
#Weights table processing
import pandas as pd
import pdb


def apply_multipliers_table(time_aligned_df,df, multipliers_table,month_data):
    for index, row in multipliers_table.iterrows():
        variable = row['Variables']
        pre_multiplier = row['pre_wt']
        post_multiplier = row['post_wt']
        # Filter columns based on the current variable
        variable_columns = [col for col in df.columns if variable in col]
        pre_columns_to_multiply = variable_columns[0:month_data['total_months_pre']]
        post_columns_to_multiply = variable_columns[month_data['total_months_pre']:]
        if pre_columns_to_multiply:
            df[pre_columns_to_multiply] = (df[pre_columns_to_multiply] * pre_multiplier) 

        if post_columns_to_multiply:
            df[post_columns_to_multiply] = (df[post_columns_to_multiply] * post_multiplier ) 

    return df















