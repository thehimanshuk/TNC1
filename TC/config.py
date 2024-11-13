import pandas as pd
# Segregating Columns

categorical_columns = ['Zip','ID','TC']
numerical_columns = ['NRx','PDE','Copay',
                     'Delivered_Doximity','Delivered_Epocrates','Engaged_Doximity',
                     'Engaged_Epocrates','Delivered_Medscape','Engaged_Medscape',
                     'Delivered_Nexgen','Engaged_Nexgen','SpeakerEvent']
hcp_identifier = 'ID'


date_columns='Month'
date_format='yyyymm'
format = ['long']
tc_identifier='TC'
event_identifer='SpeakerEvent'
test_value='T'
control_value='C'
segment_var=[]


format_mapping = {
    "yyyy-mm": "%Y-%m",
    "yyyymm": "%Y%m",
    "dd-mm-yyyy": "%d-%m-%Y",
    "mm-yyyy": "%m-%Y",
    "yyyy-mm-dd": "%Y-%m-%d",
    
}




pre_start='Jul-2019'
pre_end='Dec-2019'  
event_date='Jan-2020'
post_end='Jun-2020'

# For aggregration variable specification
#cases = {'Emails': [5],'Calls':[5],'Brand_Sales':[5]}

# Define cases specifying positions for each prefix
cases = {
    'NRx': {6: ['pre']},   
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


event_vars =['NRx']
agg_vars=['NRx']
sales_var='NRx'


mom_pre_wts=[1]
mom_post_wts=[1]

agg_pre_wts=[1]
agg_post_wts=[1]

mom_pre_match=True
mom_post_match=False

agg_pre_match=True
agg_post_match=False


#Defining batch size

batch_size = 50
result_df = pd.DataFrame(columns=['Test_ID', 'Control_ID', 'Euclidean Distance'])