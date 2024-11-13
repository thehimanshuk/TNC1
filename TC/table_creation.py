
#creation of table for month-month and aggregate matching


#table generation code
#currently use this for both MOM and aggregate
import pandas as pd
import pdb



def generate_variables(data,event_vars,pre_wts,post_wts,pre_match,post_match):
    pre_variables = [f'{event_var}_{i}' for event_var in event_vars for i in range(sorted(data['Pre_Start'].unique())[0],sorted(data['Post_Start'].unique())[0])]
    post_variables = [f'{event_var}_{i}' for event_var in event_vars for i in range(sorted(data['Post_Start'].unique())[0],sorted(data['Post_End'].unique())[0]+1)]
    if pre_match==True and post_match==True:
        variables_to_match=pre_variables+post_variables
    elif pre_match==True:
        variables_to_match=pre_variables
    elif post_match==True:
        variables_to_match=post_variables

    # Creating a DataFrame to display the table
    table_df = pd.DataFrame({
        'Variables': event_vars,
        'pre_wt': pre_wts,
        'post_wt':post_wts
    })

    return variables_to_match, table_df




