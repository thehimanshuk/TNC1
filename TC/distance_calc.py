


#Time Alignment Code
#importing required libraries


from logging import config
import pandas as pd
import numpy as np
import re
from tc.analysis_months_calculation import analyis_initial_months
import tc.config as config
from tc.table_creation import generate_variables
from tc.multipliers import apply_multipliers_table
from tc.time_align_var_func import increment_numbers_in_list
from tc.agg_logic import calculate_sum_last_n_columns,standardize_columns
from scipy.spatial.distance import cdist
import pdb
from itertools import product


class DistanceCalculation:
    def __init__(self,data,num_cols,hcp_identifier,tc_identifier,event_identifier):
        self.data = data
        self.num_cols=num_cols
        self.date_length=None
        self.hcp_identifier=hcp_identifier
        self.tc_identifier=tc_identifier
        self.event_identifier=event_identifier

    def time_align(self,test_filter_value,post_cut_off)-> pd.DataFrame:
        selected_data = self.data.filter(regex=f'^({self.hcp_identifier}|{self.event_identifier}|{self.tc_identifier})', axis=1)
        selected_data=selected_data[selected_data[self.tc_identifier] == test_filter_value]
        selected_columns=list(selected_data)
        selected_columns.remove(self.hcp_identifier)
        selected_columns.remove(self.tc_identifier)
        num_months=len(selected_columns)
        self.date_length=num_months
        mapping_dict={'Months':selected_columns,'Index': list(range(1,num_months+1))}
        selected_data.drop([self.tc_identifier],inplace=True,axis=1)
        pre_post_calc=analyis_initial_months(event_date=config.event_date,pre_start=config.pre_start,post_end= config.post_end,pre_end=config.pre_end)
        self.mapping_month=mapping_dict['Index'][mapping_dict['Months'].index(f"{self.event_identifier}_{pre_post_calc['event_date']}")]
        first_exposure=selected_data.loc[:,  f"{self.event_identifier}_{pre_post_calc['event_date']}":].gt(0).idxmax(axis=1).apply(lambda x:str(x))
        # Create a mapping dictionary using zip
        mapping_dict = dict(zip(mapping_dict['Months'], mapping_dict['Index']))
        # Replace values in the "Post_Start" column based on the mapping dictionary
        time_align=pd.DataFrame({self.hcp_identifier: selected_data[self.hcp_identifier], 'Post_Start': first_exposure})
        time_align['Post_Start'] = time_align['Post_Start'].replace(mapping_dict)
        time_align['Post_End']=time_align['Post_Start']+pre_post_calc['total_months_post']-1
        time_align['Pre_End']=time_align['Post_Start']-1
        time_align['Pre_Start']=time_align['Post_Start']-pre_post_calc['total_months_pre']
        #condition for boundary cases
        time_align['Post_End'] = time_align['Post_End'].apply(lambda x: x if x <= num_months else num_months)
        
        # 3 months post period cut off condition
        post_start_check = sorted(time_align['Post_Start'].unique())
        post_end_check = sorted(time_align['Post_End'].unique())
        result = []
        for i in range(len(post_start_check)):
            if i < len(post_end_check) and abs(post_end_check[i] - post_start_check[i]) <= post_cut_off:
                result.append(post_start_check[i])
        if len(result)>=0:
             time_align=time_align[~time_align['Post_Start'].isin(result)]
        self.time_aligned_data=time_align
        return time_align
    

    def column_conversion(self):
        date_length=self.date_length
        categ_values = [f"{col}_{i}" for col in self.num_cols for i in range(1, date_length + 1)]

        # Define a pattern using regular expression
        pattern = re.compile(r'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec',re.IGNORECASE)

        # Filter columns based on the pattern
        selected_columns = list(filter(lambda col: pattern.search(col), self.data.columns))

        for col in selected_columns:
            if col in config.segment_var:
                selected_columns.remove(col)
        # selected_columns.remove("Decile")

        remaining_columns = [col for col in self.data.columns if col not in selected_columns]

        # Rename columns
        # Define the desired order of columns
        desired_colums=remaining_columns+selected_columns
        # Reorder the columns
        data = self.data.reindex(columns=desired_colums)

        new_column_names = remaining_columns + categ_values
        data.rename(columns=dict(zip(data.columns, new_column_names)), inplace=True)
        self.data=data
        self.agg_data=data.copy()
        return data

    def data_standardize(self):
    # Assuming 'data' is your DataFrame with both numerical and non-numerical columns
    # Select only the numerical columns
        numerical_columns = self.data.select_dtypes(include=['float64', 'int64']).columns
        numerical_columns=numerical_columns.delete(numerical_columns.get_loc(self.hcp_identifier))
    # Create a StandardScaler object
        #scaler = StandardScaler()
        # Fit the scaler on the selected numerical columns and transform the data
        #self.data[numerical_columns] = scaler.fit_transform(self.data[numerical_columns])
        #self.data[numerical_columns] = preprocessing.scale(self.data[numerical_columns])
         # Calculate mean and standard deviation with ddof=1
        column_means = self.data[numerical_columns].mean()
        column_stds = self.data[numerical_columns].std(ddof=1)

        # Standardize the data using mean and standard deviation with ddof=1
        standardized_data = (self.data[numerical_columns] - column_means) / column_stds

        # Update the original DataFrame with standardized values
        self.data[numerical_columns] = standardized_data
        return self.data
    
    
    

    def distance_matching(self,control_matches,agg_matching,segment_matching,filter_test_val,filter_control_val,segment_var,batch_size):
        if segment_matching==True:
            self.data['segment_var'] = self.data[segment_var].astype(str).apply(lambda x: "_".join(x), axis=1)
            self.agg_data['segment_var'] = self.agg_data[segment_var].astype(str).apply(lambda x: "_".join(x), axis=1)
        else:
            self.data['segment_var']="National"
            self.agg_data['segment_var']="National"
        uni_combo=sorted(self.time_aligned_data['Pre_Start'].unique())
        pre_post_calc=analyis_initial_months(event_date=config.event_date,pre_start=config.pre_start,post_end= config.post_end,pre_end=config.pre_end)
        mom_variables_to_match,table = generate_variables(self.time_aligned_data,config.event_vars,pre_wts=config.mom_pre_wts,post_wts=config.mom_post_wts,pre_match=config.mom_pre_match,post_match=config.mom_post_match)
        mom_variables_to_match.append(self.hcp_identifier)
        mom_match=increment_numbers_in_list(mom_variables_to_match,times=self.time_aligned_data['Pre_Start'].nunique()-1)
        # Create a mapping of Pre_Start to index
        pre_start_index_mapping = {value: index for index, value in enumerate(uni_combo)}
        uni_combo1 = [(pre_start, segment, pre_start_index_mapping[pre_start])
                for pre_start, segment in product(uni_combo, self.data['segment_var'].unique())]
        
        test_df=self.data[self.data[self.tc_identifier] == filter_test_val]
        control_df=self.data[self.data[self.tc_identifier] == filter_control_val]
        test_df=pd.merge(test_df,self.time_aligned_data,on=self.hcp_identifier)
        result_df = pd.DataFrame(columns=['Test_ID', 'Control_ID', 'Euclidean Distance']) 


        for pre_start,segment,index in uni_combo1:
            test_df_segmented = test_df[(test_df['Pre_Start'] == pre_start) & (test_df['segment_var'] == segment)]
            for start_idx in range(0, test_df_segmented.shape[0], batch_size):
                end_idx = min(start_idx + batch_size, test_df_segmented.shape[0])
                test_df_batch = test_df_segmented.iloc[start_idx:end_idx]
                test_df1=test_df_batch[(test_df_batch['Pre_Start'] == pre_start) & (test_df_batch['segment_var'] == segment)]
                mom_vec_filter=[x for x in mom_match[index] if x in self.data.columns]
                test_df1=pd.DataFrame(test_df1[mom_vec_filter])
                control_df1=control_df[control_df['segment_var'] == segment]
                control_df1=pd.DataFrame(control_df1[mom_vec_filter])
                apply_multipliers_table(self.time_aligned_data,test_df1, table,pre_post_calc)
                apply_multipliers_table(self.time_aligned_data,control_df1, table,pre_post_calc)
                if agg_matching==True:
                    agg_variables_to_match,table1 = generate_variables(self.time_aligned_data,config.agg_vars,pre_wts=config.agg_pre_wts,post_wts=config.agg_post_wts,pre_match=config.agg_pre_match,post_match=config.agg_post_match)
                    agg_variables_to_match.append(self.hcp_identifier)
                    agg_match=increment_numbers_in_list(agg_variables_to_match,times=self.time_aligned_data['Pre_Start'].nunique()-1)
                    test_df_agg=pd.merge(self.agg_data,self.time_aligned_data,on=self.hcp_identifier)
                    agg_vec_filter=[x for x in agg_match[index] if x in self.data.columns]
                    test_df_agg=test_df_agg[test_df_agg['Pre_Start'] == pre_start]
                    test_df_agg1=calculate_sum_last_n_columns(test_df_agg,pre_post_calc,config.cases,agg_vec_filter,self.mapping_month)
                    control_df_agg1=calculate_sum_last_n_columns(self.agg_data[self.agg_data[self.tc_identifier] == filter_control_val],pre_post_calc,config.cases,agg_vec_filter,self.mapping_month)
                    agg_data=pd.concat([test_df_agg1,control_df_agg1])
                    subset_columns_agg = [col for col in agg_data.columns if col.startswith("Sum_")]
                    standardize_columns(agg_data,subset_columns_agg)
                    agg_data=agg_data[agg_data['segment_var'] == segment]
                    apply_multipliers_table(self.time_aligned_data,agg_data,table1,pre_post_calc)
                    test_df1=pd.merge(test_df1,agg_data,on=self.hcp_identifier)
                    control_df1=pd.merge(control_df1,agg_data,on=self.hcp_identifier)
                    #test_df1 = test_df1.iloc[start_idx:end_idx]
                    new_list=mom_vec_filter
                    new_list+=subset_columns_agg
                else:
                    new_list=mom_vec_filter
                new_list = [x for x in new_list if x != self.hcp_identifier]
                distances = cdist(test_df1[new_list].values, control_df1[new_list].values)
                batch_top_n_indices = np.argsort(distances, axis=1)[:, :control_matches]
                batch_top_n_control_ids = control_df1[self.hcp_identifier].values[batch_top_n_indices]
                batch_top_n_distances = np.take_along_axis(distances, batch_top_n_indices, axis=1)
                if control_df1.shape[0]!=0:
                    col_result_df = pd.DataFrame({'Test_ID': np.repeat(test_df1[self.hcp_identifier], control_matches),
                                  'Control_ID': batch_top_n_control_ids.flatten(),
                                  'Euclidean Distance': batch_top_n_distances.flatten()})
                    result_df = pd.concat([result_df, col_result_df], ignore_index=True)
            
                
        return result_df
    

    





