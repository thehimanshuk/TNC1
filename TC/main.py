#main.py file

import pandas as pd
import copy
import tc.config as config
# import tc.config as config
from tc.data_import import ImportData
from tc.distance_calc import DistanceCalculation
from tc.results_page import ResultCalculations, calculate_lift


#Import Page module

dataset_import = ImportData(
    file_path="TC_Data_Wide.csv",
    data_format="wide",
    date_format="yyyy-mm",
    date_col=config.date_columns,
    categorical_cols=config.categorical_columns,
    numerical_cols=config.numerical_columns,
    identifier=config.hcp_identifier,
    week=False

)
read_data = dataset_import.read_csv()


# Distance Calculation Module


dist_calc=DistanceCalculation(
data=read_data,
num_cols=config.numerical_columns,
hcp_identifier=config.hcp_identifier,
tc_identifier=config.tc_identifier,
event_identifier=config.event_identifer)

time_aligned_data=dist_calc.time_align(test_filter_value=config.test_value,post_cut_off=0)

data_conversion=dist_calc.column_conversion()

original_data_conversion = copy.deepcopy(data_conversion)
dist_calc.data_standardize()

result=dist_calc.distance_matching(
control_matches=1,
agg_matching=True,
segment_matching=False,
filter_test_val=config.test_value,
filter_control_val=config.control_value,
segment_var=config.segment_var,
batch_size=config.batch_size
)




# # #Result Page Module

result_calc=ResultCalculations(
    matching_data=result,
    time_aligned_data=time_aligned_data,
    data_conversion=original_data_conversion,
    hcp_identifier=config.hcp_identifier
)
result_calc.data_merge()
avgs_data=result_calc.avgs_calculation()
graph_data_test,graph_data_control=result_calc.graph_data_generation()

avgs_table,lift=calculate_lift(avgs_data,config.sales_var)