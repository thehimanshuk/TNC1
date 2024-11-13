
import numpy as np

def filter_columns_by_prefix(columns_list, prefix):
    return [col for col in columns_list if col.startswith(prefix)]





def calculate_lift(avgs_data,sales_col):
     #caclulate lift select sales for lift
     lift_num=(np.mean(avgs_data[f'''{sales_col}''''_Post_Average'])-np.mean(avgs_data[f'''{sales_col}''''_Pre_Average']))-(np.mean(avgs_data[f'''{sales_col}''''_Post_Control_Average'])-np.mean(avgs_data[f'''{sales_col}''''_Pre_Control_Average']))
     lift_denom=(np.mean(avgs_data[f'''{sales_col}''''_Pre_Average'])+np.mean(avgs_data[f'''{sales_col}''''_Pre_Control_Average']))/2
     lift=(lift_num/lift_denom)*100
     return lift