

#loading the initial data from the user

# data_wide=pd.read_csv("TC_Data_Wide.csv")
# data_long=pd.read_csv("TC_Data_Long.csv")

import pandas as pd


# Segregating Columns
numerical_columns = ['Emails', 'Calls','Brand_Sales','Speaker_Program','Mobile_Alerts','Competitor_Detailing']
categorical_columns=['Zip_cd','TC','HCP_ID']
date_columns='Date'
date_format='yyyymm'
format = ['long']
hcp_identifier='HCP_ID'
tc_identifier='TC'
event_identifer='Speaker_Program'
test_value='T'
control_value='C'
segment_var=['Decile','Segment']


format_mapping = {
    "yyyy-mm": "%Y-%m",
    "yyyymm": "%Y%m",
    "dd-mm-yyyy": "%d-%m-%Y",
    "mm-yyyy": "%m-%Y",
    "yyyy-mm-dd": "%Y-%m-%d",
    
}




event_date='Jan-2023'
pre_start='Jan-2022'
pre_end='Oct-2018'  
post_end='Dec-2023'


# For aggregration variable specification
#cases = {'Emails': [5],'Calls':[5],'Brand_Sales':[5]}

# Define cases specifying positions for each prefix
cases = {
    'Emails': {8: ['pre']},   
    'Calls': {8: ['pre']},
    'Brand_Sales': {8: ['pre']}
    #'Mobile_Alerts': {8: ['pre']}
                  # For prefix 'B', select columns from the end
           # For prefix 'B', select columns from the beginning
}

# The `cases` dictionary is used to specify how to aggregate data columns based on prefixes and
# positions within the column names.
# For prefix 'A', select columns from both beginning and end
# cases = {  
#     'Emails': {6:['post'],6: ['pre']},
#     'Calls': {6: ['pre'],6: ['post']},
#     'Brand_Sales':{6: ['pre'],6: ['post']}         
# }
# {'Emails': {6: ['pre']}, 'Calls': {6: ['post']}, 'Brand_Sales': {6: ['post']}}
#     # For prefix 'B', select columns from the beginning





# The `cases` dictionary is being used to specify how to aggregate data columns based on prefixes and
# positions within the column names. In this specific case, it seems like there might be a mistake in
# the dictionary structure.



# cases = {
#     'Emails': {5: [ 'pre']},
#     'Calls': {5: ['pre']},
#     'Mobile_Alerts': {5: ['pre']}
# }


event_vars =['Emails','Calls','Brand_Sales']
agg_vars=['Emails','Calls','Brand_Sales']
sales_var='Brand_Sales'


mom_pre_wts=[1,1,1]
mom_post_wts=[1,1,1]

agg_pre_wts=[1,1,1]
agg_post_wts=[1,1,1]

mom_pre_match=True
mom_post_match=False

agg_pre_match=True
agg_post_match=False


#Defining batch size

batch_size = 50
result_df = pd.DataFrame(columns=['Test_ID', 'Control_ID', 'Euclidean Distance'])




#Iteration page task list

#1.Function to filter data:Filter tests/control hcps-use it in data standardization etc.
#2.Function to standardize the filter data
#3.Based on the user inputs caclulate pre-post period durations and prest/preend-postst/postend
#4.Function to aggregate sum of column based on indexes
#For example 1_5_7 then sum of theose columns based on the particular variables
#5.Distance Caclulation
#6.Create dynamic dataframes whcih can include variables,pre/post weights etc
#7.Function for segmentation in both iterations and results page
#8.Filter for different functions-matching,repeetiotion matching etc


#Note
#All the above function approaches can change
#All the functions shoulod be dynamic No hardcoding values
#All the functions should follow  proper coding standards


#SAVE
#results page function overview
#1.Find the averages pre/post for each test/control hcp pair from the matching file
#2.Calculate the following metrics(lift,double difference)etc
#3.Geneate all the data from the T-C pairs for avoiding repetitions