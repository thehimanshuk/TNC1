import pandas as pd
import numpy as np
from tc.distance_calc import DistanceCalculation
import tc.config as config
from tc.analysis_months_calculation import analyis_initial_months
from tc.table_creation import generate_variables
from tc.time_align_var_func import increment_numbers_in_list
from tc.results_page_utils import filter_columns_by_prefix,calculate_lift
import pdb


class ResultCalculations:
       def __init__(self,matching_data,time_aligned_data,data_conversion,hcp_identifier):
           self.matching_data=matching_data
           self.time_aligned_data=time_aligned_data
           self.data_conversion=data_conversion
           self.hcp_identifier=hcp_identifier
            

       def data_merge(self):
        merged_data=pd.merge(self.matching_data,self.time_aligned_data,left_on="Test_ID",right_on=self.hcp_identifier)
        test_data=pd.merge(merged_data,self.data_conversion,on=self.hcp_identifier)
        control_data=pd.merge(merged_data,self.data_conversion,left_on="Control_ID",right_on=self.hcp_identifier)
        self.test_data=test_data
        self.control_data=control_data
        return test_data,control_data
       
       def avgs_calculation(self):
        pre_post_calc=analyis_initial_months(event_date=config.event_date,pre_start=config.pre_start,post_end= config.post_end,pre_end=config.pre_end)       
        variables,table = generate_variables(self.time_aligned_data,config.event_vars,pre_wts=config.mom_pre_wts,post_wts=config.mom_post_wts,pre_match=True,post_match=True)
        variables1=increment_numbers_in_list(variables,times=self.time_aligned_data['Pre_Start'].nunique()-1)
        uni_combo=self.time_aligned_data['Pre_Start'].unique()
        result_dfs = []  # List to store results from each iteration
        for i in range(len(variables1)):
            combined_data1 = pd.DataFrame()
            for var_index in config.event_vars:
                  print(var_index)
                  print(i)
                  test_data1 = self.test_data[self.test_data['Pre_Start'] == uni_combo[i]]
                  control_data1 = self.control_data[self.control_data['Pre_Start'] == uni_combo[i]]
                  variables_filter=[x for x in variables1[i] if x in self.test_data.columns]
                  pre_columns  =  filter_columns_by_prefix(variables_filter, var_index)[:pre_post_calc['total_months_pre']]
                  post_columns = [x for x in filter_columns_by_prefix(variables_filter, var_index) if x not in pre_columns][:pre_post_calc['total_months_post']]
                  print(pre_columns)
                  print(post_columns)
                  test_data1[f'{var_index}_Pre_Average'] = round(test_data1[pre_columns].sum(axis=1) / len(pre_columns),2)
                  test_data1[f'{var_index}_Post_Average'] = round(test_data1[post_columns].sum(axis=1) / len(post_columns),2)
                  control_data1[f'{var_index}_Pre_Control_Average'] =round(control_data1[pre_columns].sum(axis=1) / len(pre_columns),2)
                  control_data1[f'{var_index}_Post_Control_Average'] =round(control_data1[post_columns].sum(axis=1) / len(post_columns),2)
                  # Concatenate test_data1 and control_data1
                  combined_data = pd.concat([test_data1, control_data1], axis=1)
                  combined_data = combined_data.filter(regex='Test|Average|Control')
                  combined_data1 = pd.concat([combined_data1, combined_data], axis=1)
            result_dfs.append(combined_data1) 

        result_df = pd.concat(result_dfs, axis=0)
        return result_df
       
       def graph_data_generation(self):
        pre_post_calc=analyis_initial_months(event_date=config.event_date,pre_start=config.pre_start,post_end= config.post_end,pre_end=config.pre_end)       
        variables,table = generate_variables(self.time_aligned_data,config.event_vars,pre_wts=config.mom_pre_wts,post_wts=config.mom_post_wts,pre_match=True,post_match=True)
        variables1=increment_numbers_in_list(variables,times=self.time_aligned_data['Pre_Start'].nunique()-1)
        uni_combo=self.time_aligned_data['Pre_Start'].unique()
        uni_combo=sorted(uni_combo)
        test_result_dfs = []  # List to store results from each iteration
        control_results_dfs=[]
        for i in range(len(variables1)):
            for var_index in config.event_vars:
                  # In the provided code snippet, `test_data1` is being used to filter the `test_data`
                  # DataFrame based on the value of the 'Pre_Start' column. Specifically, it is
                  # filtering the rows where the 'Pre_Start' column matches the value in
                  # `uni_combo[i]` within the loop iteration.
                  test_data1 = self.test_data[self.test_data['Pre_Start'] == uni_combo[i]]
                  control_data1 = self.control_data[self.control_data['Pre_Start'] == uni_combo[i]]
                  variables_filter=[x for x in variables1[i] if x in self.test_data.columns]
                  pre_columns = filter_columns_by_prefix(variables_filter, var_index)[:pre_post_calc['total_months_pre']]
                  post_columns = filter_columns_by_prefix(variables_filter, var_index)[pre_post_calc['total_months_post']:]
                  columns_to_convert=variables_filter
                  month_mapping=dict(zip(columns_to_convert, range(1,len(columns_to_convert)+1)))
                  test_grouped_data=pd.melt(test_data1, id_vars=['Test_ID'], value_vars=columns_to_convert, var_name='Month', value_name='Value')
                  test_grouped_data['rowno'] =test_grouped_data['Month'].map(month_mapping)
                  test_grouped_data=test_grouped_data.drop_duplicates(subset=['Test_ID', 'rowno']).reset_index(drop=True)
                  test_grouped_data=pd.DataFrame(test_grouped_data.groupby('rowno')['Value'].mean()).reset_index()
                  test_grouped_data['variable']=var_index
                  control_grouped_data=pd.melt(control_data1, id_vars=['Test_ID'], value_vars=columns_to_convert, var_name='Month', value_name='Value')
                  control_grouped_data['rowno'] = control_grouped_data['Month'].map(month_mapping)
                  control_grouped_data=pd.DataFrame(control_grouped_data.groupby('rowno')['Value'].mean()).reset_index()
                  control_grouped_data['variable']=var_index
                  test_result_dfs.append(test_grouped_data)
                  control_results_dfs.append(control_grouped_data)
        result_df = pd.concat(test_result_dfs, axis=0)
        result_df1= pd.concat(control_results_dfs, axis=0)
        return result_df,result_df1
       

def calculate_lift(avgs_data,sales_col):
     #caclulate lift select sales for lift
     lift_num=(np.mean(avgs_data[f'''{sales_col}''''_Post_Average'])-np.mean(avgs_data[f'''{sales_col}''''_Pre_Average']))-(np.mean(avgs_data[f'''{sales_col}''''_Post_Control_Average'])-np.mean(avgs_data[f'''{sales_col}''''_Pre_Control_Average']))
     lift_denom=(np.mean(avgs_data[f'''{sales_col}''''_Pre_Average'])+np.mean(avgs_data[f'''{sales_col}''''_Pre_Control_Average']))/2
     lift=(lift_num/lift_denom)*100
     metric_table={'pre_test_avg':np.mean(avgs_data[f'''{sales_col}''''_Pre_Average']),
                   'post_test_avg':np.mean(avgs_data[f'''{sales_col}''''_Post_Average']),
                   'pre_control_avg':np.mean(avgs_data[f'''{sales_col}''''_Pre_Control_Average']),
                   'post_control_avg':np.mean(avgs_data[f'''{sales_col}''''_Post_Control_Average'])}
     return metric_table,lift
       
# def calculate_lift(avgs_data, sales_cols):
#     lift_results = {}
#     for col in sales_cols:
#         # Calculate lift for each variable
#         lift_num = (np.mean(avgs_data[f'{col}_Post_Average']) - np.mean(avgs_data[f'{col}_Pre_Average'])) - \
#                    (np.mean(avgs_data[f'{col}_Post_Control_Average']) - np.mean(avgs_data[f'{col}_Pre_Control_Average']))
#         lift_denom = (np.mean(avgs_data[f'{col}_Pre_Average']) + np.mean(avgs_data[f'{col}_Pre_Control_Average'])) / 2
#         lift = (lift_num / lift_denom) * 100
        
#         # Store the lift and metric table for each variable
#         metric_table = {
#             'pre_test_avg': np.mean(avgs_data[f'{col}_Pre_Average']),
#             'post_test_avg': np.mean(avgs_data[f'{col}_Post_Average']),
#             'pre_control_avg': np.mean(avgs_data[f'{col}_Pre_Control_Average']),
#             'post_control_avg': np.mean(avgs_data[f'{col}_Post_Control_Average'])
#         }
#         lift_results[col] = (metric_table, lift)
    
#     return lift_results

