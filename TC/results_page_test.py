
import pandas as pd
import numpy as np
import pdb
from tc.distance_calc import DistanceCalculation
import tc.config as config
from tc.analysis_months_calculation import analyis_initial_months
from tc.table_creation import generate_variables
from tc.time_align_var_func import increment_numbers_in_list



# Results Page Functions:TBI

# Based on the matching file of T-C Pairs Calculate averages

#1.Function to calculate parameter table:Pre-Post averages breakup
#2.Function to calculate lift and double differences
#3.Function to calculate data points for the graphs




data=pd.read_csv("TC_Data_Wide.csv")


dist_calc=DistanceCalculation(
data=data,
num_cols=config.numerical_columns,
hcp_identifier=config.hcp_identifier,
tc_identifier=config.tc_identifier,
event_identifier=config.event_identifer)

time_aligned_data=dist_calc.time_align(value=config.test_value)

data_conversion=dist_calc.column_conversion()

# dist_calc.data_standardize()

result=dist_calc.distance_matching(
control_matches=1,
agg_matching=True,
segment_matching=False,
filter_test_val=config.test_value,
filter_control_val=config.control_value,
segment_var=config.segment_var
)


#result



# function for calculation of lift

def data_merge(matching_data,time_aligned_data,data_conversion,hcp_identifier):
    merged_data=pd.merge(matching_data,time_aligned_data,left_on="Test_ID",right_on=hcp_identifier)
    test_data=pd.merge(merged_data,data_conversion,on=hcp_identifier)
    control_data=pd.merge(merged_data,data_conversion,left_on="Control_ID",right_on=hcp_identifier)
    return test_data,control_data

test_data,control_data=data_merge(result,time_aligned_data,data_conversion,config.hcp_identifier)


def filter_columns_by_prefix(columns_list, prefix):
    return [col for col in columns_list if col.startswith(prefix)]

def avgs_calculation(test_data,control_data,time_aligned_data):
        pre_post_calc=analyis_initial_months(event_date=config.event_date,pre_start=config.pre_start,post_end= config.post_end)       
        variables,table = generate_variables(config.event_vars, pre_period=6,post_period=6,pre_wts=[3,3],post_wts=[1,1])
        variables1=increment_numbers_in_list(variables,times=time_aligned_data['Pre_Start'].nunique()-1)
        uni_combo=time_aligned_data['Pre_Start'].unique()
        result_dfs = []  # List to store results from each iteration
        for i in range(len(variables1)):
            combined_data1 = pd.DataFrame()
            for var_index in config.event_vars:
                  print(var_index)
                  print(i)
                  test_data1 = test_data[test_data['Pre_Start'] == uni_combo[i]]
                  control_data1 = control_data[control_data['Pre_Start'] == uni_combo[i]]
                  pre_columns = filter_columns_by_prefix(variables1[i], var_index)[:6]
                  post_columns = filter_columns_by_prefix(variables1[i], var_index)[6:]
                  test_data1[f'{var_index}_Pre_Average'] = test_data1[pre_columns].sum(axis=1) / 6
                  test_data1[f'{var_index}_Post_Average'] = test_data1[post_columns].sum(axis=1) / 6
                  control_data1[f'{var_index}_Pre_Control_Average'] = control_data1[pre_columns].sum(axis=1) / 6
                  control_data1[f'{var_index}_Post_Control_Average'] = control_data1[post_columns].sum(axis=1) / 6
                  # Concatenate test_data1 and control_data1
                  combined_data = pd.concat([test_data1, control_data1], axis=1)
                  combined_data = combined_data.filter(regex='Test|Average|Control')
                  combined_data1 = pd.concat([combined_data1, combined_data], axis=1)
            result_dfs.append(combined_data1) 

        result_df = pd.concat(result_dfs, axis=0)
        return result_df

avgs_data=avgs_calculation(test_data=test_data,control_data=control_data,time_aligned_data=time_aligned_data)



def calculate_lift(avgs_data,sales_col):
     #caclulate lift select sales for lift
     lift_num=(np.mean(avgs_data[f'''{sales_col}''''_Post_Average'])-np.mean(avgs_data[f'''{sales_col}''''_Pre_Average']))-(np.mean(avgs_data[f'''{sales_col}''''_Post_Control_Average'])-np.mean(avgs_data[f'''{sales_col}''''_Pre_Control_Average']))
     lift_denom=(np.mean(avgs_data[f'''{sales_col}''''_Pre_Average'])+np.mean(avgs_data[f'''{sales_col}''''_Pre_Control_Average']))/2
     lift=(lift_num/lift_denom)*100
     return lift

calculate_lift(avgs_data=avgs_data,sales_col="Brand_Sales")



#graphs logic to be implemened



def graph_data_generation(test_data,control_data,time_aligned_data):
        pre_post_calc=analyis_initial_months(event_date=config.event_date,pre_start=config.pre_start,post_end= config.post_end)       
        variables,table = generate_variables(config.event_vars, pre_period=6,post_period=6,pre_wts=[3,3],post_wts=[1,1])
        variables1=increment_numbers_in_list(variables,times=time_aligned_data['Pre_Start'].nunique()-1)
        uni_combo=time_aligned_data['Pre_Start'].unique()
        test_result_dfs = []  # List to store results from each iteration
        control_results_dfs=[]
        for i in range(len(variables1)):
            combined_data1 = pd.DataFrame()
            for var_index in config.event_vars:
                  print(var_index)
                  print(i)
                  # In the provided code snippet, `test_data1` is being used to filter the `test_data`
                  # DataFrame based on the value of the 'Pre_Start' column. Specifically, it is
                  # filtering the rows where the 'Pre_Start' column matches the value in
                  # `uni_combo[i]` within the loop iteration.
                  test_data1 = test_data[test_data['Pre_Start'] == uni_combo[i]]
                  control_data1 = control_data[control_data['Pre_Start'] == uni_combo[i]]
                  pre_columns = filter_columns_by_prefix(variables1[i], var_index)[:pre_post_calc['total_months_pre']]
                  post_columns = filter_columns_by_prefix(variables1[i], var_index)[pre_post_calc['total_months_post']:]
                  columns_to_convert=pre_columns+post_columns
                  test_grouped_data=pd.melt(test_data1, id_vars=['Test_ID'], value_vars=columns_to_convert, var_name='Month', value_name='Value')
                  test_grouped_data['rowno'] = test_grouped_data.groupby('Test_ID').cumcount() + 1
                  test_grouped_data=pd.DataFrame(test_grouped_data.groupby('rowno')['Value'].mean()).reset_index()
                  test_grouped_data['variable']=var_index
                  control_grouped_data=pd.melt(control_data1, id_vars=['Test_ID'], value_vars=columns_to_convert, var_name='Month', value_name='Value')
                  control_grouped_data['rowno'] = control_grouped_data.groupby('Test_ID').cumcount() + 1
                  control_grouped_data=pd.DataFrame(control_grouped_data.groupby('rowno')['Value'].mean()).reset_index()
                  control_grouped_data['variable']=var_index
                  test_result_dfs.append(test_grouped_data)
                  control_results_dfs.append(control_grouped_data)
        return test_result_dfs,control_results_dfs



r1,r2=graph_data_generation(test_data=test_data,
                      control_data=control_data,
                      time_aligned_data=time_aligned_data)

result_df = pd.concat(r1, axis=0)
result_df1= pd.concat(r2, axis=0)

def graph_filter(data,filter_val):
     data=data[data['variable']==filter_val]
     data=pd.DataFrame(data.groupby('rowno')['Value'].mean()).reset_index()
     return data


aa=graph_filter(result_df,"Brand_Sales")

plt.plot(aa['rowno'], aa['Value'], marker='o')
plt.show()
















# import time
# import numpy as np
# import pandas as pd
# from scipy.spatial.distance import cdist
# import sys
# # Generate example datasets with test IDs and control IDs
# np.random.seed(0)

# # Example test IDs
# test_ids = np.arange(10000)

# # Example control IDs
# control_ids = np.arange(150000)

# # Example test features
# tests_features = np.random.rand(10000, 50)  # 10,000 tests, each with 10 features

# # Example control features
# controls_features = np.random.rand(150000, 50)  # 150,000 controls, each with 10 features

# # Define batch size
# batch_size = 1000

# # Calculate number of batches
# num_batches = len(test_ids) // batch_size + (1 if len(test_ids) % batch_size != 0 else 0)

# # Initialize an empty array to store top 5 control IDs for each test ID
# result_df = pd.DataFrame(columns=['ID1', 'ID2', 'Euclidean Distance'])
# # Loop through test data in batches
# for i in range(2):
#     start_time=time.time()
#     print(i)
#     start_idx = i * batch_size
#     end_idx = min((i + 1) * batch_size, len(test_ids))
#     batch_test_ids = test_ids[start_idx:end_idx]
#     batch_tests_features = tests_features[start_idx:end_idx]

#     # Calculate Euclidean distances for the current batch of tests
#     distances = cdist(batch_tests_features, controls_features)
#     batch_top_5_indices = np.argsort(distances, axis=1)[:, :5]
#     batch_top_5_control_ids = control_ids[batch_top_5_indices]
#     batch_top_5_distances = np.take_along_axis(distances, batch_top_5_indices, axis=1)

#     col_result_df = pd.DataFrame({'ID1': np.repeat(batch_test_ids, 5),
#                                   'ID2': batch_top_5_control_ids.flatten(),
#                                   'Euclidean Distance': batch_top_5_distances.flatten()})
    
#     # Convert indices to control IDs
#     result_df = pd.concat([result_df, col_result_df], ignore_index=True)
#     end_time=time.time()
#     print("Time taken",end_time-start_time)


# # Example data
# data = [[0, 1], [2, 3], [4, 5], [6, 7]]

# from sklearn.preprocessing import Normalizer
# norm = Normalizer()
# X_norm = norm.fit_transform(data)


# from sklearn.preprocessing import StandardScaler


# # Initialize the StandardScaler with precision=8
# scaler = StandardScaler()

# # Fit the scaler to your data
# scaler.fit(data)

# # Transform the data
# scaled_data = scaler.transform(data)

# print("Original data:")
# print(data)
# print("\nScaled data with 8 decimals:")
# print(scaled_data)
