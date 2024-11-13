# Testing weekly Data sample
# Run weekly analysis only id date format is dd-mm-yyyy or yyyy-mm-dd
# and if weekly is selected as True by the user
# Weekly Data-Need to be summed up if dates occur in same week
import pandas as pd

# Example DataFrame
data = {"date": ["15-02-2024", "20-03-2024", "10-05-2024"]}
df = pd.DataFrame(data)

# Provided code with slight modification
format_mapping = {
    "yyyy-mm": "%Y-%m",
    "yyyymm": "%Y%m",
    "dd-mm-yyyy": "%d-%m-%Y",
    "mm-yyyy": "%m-%Y",
    "yyyy-mm-dd": "%Y-%m-%d",
}

df=pd.read_csv("TC_Data_Weekly.csv")

date_format = "yyyy-mm-dd"
date_col = "Date"

if date_format in format_mapping:
    format_string = format_mapping[date_format]
    df[date_col] = pd.to_datetime(df[date_col], format=format_string)

    # Fetch week data
    df["week"] = df[date_col].dt.strftime("%V") + "-" + df[date_col].dt.strftime("%b")
else:
    print("Unsupported date format")

print(df)

d2=df.pivot_table(
                index="Zip_cd", columns="week", values='Emails'
            )
d2.columns = [
                "_".join(col).rstrip("_") for col in d2.columns.values
            ]




import re

second_list = ["E_1", "E_2", "E_3", "C_1", "C_2", "C_2", "C_3", "B_1", "B_2", "B_3"]

result = ''.join(str(i) for i in range(1, 2))
result1 = rf'_[{result}]$'
filtered_second_list = [item for item in second_list if not re.search(result1, item)]

print(filtered_second_list)




import re

# Sample column names
columns = ["January", "February", "March", "Apricot", "May", "Juniper", "July", "August", "September", "Decile", "December"]

# Define the regular expression pattern with word boundaries
pattern = re.compile(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b', re.IGNORECASE)

# Filter columns based on the pattern
selected_columns = list(filter(lambda col: pattern.search(col), columns))

print(selected_columns)








columns = ['Competitor_Detailing_2', 'Competitor_Detailing_3',
           'Competitor_Detailing_4', 'Competitor_Detailing_5',
           'Competitor_Detailing_6', 'Competitor_Detailing_7',
           'Competitor_Detailing_8', 'Competitor_Detailing_9',
           'Competitor_Detailing_10', 'Competitor_Detailing_11',
           'Competitor_Detailing_12', 'Competitor_Detailing_13',
           'Competitor_Detailing_14', 'Competitor_Detailing_15']

search_term = '_10'
pre = 5
post = 5

# Find the index of the search term
index = columns.index([col for col in columns if search_term in col][0])

# Select elements before and after the search term
pre_elements = columns[max(0, index - pre):index]
post_elements = columns[index + 1:index + 1 + post]

print("Elements before:", pre_elements)
print("Elements after:", post_elements)



a = [7, 8, 9, 10, 11, 12, 13, 14]
b = [12, 13, 14, 15, 15, 15, 15, 15]
result = []

for i in range(len(a)):
    if i < len(b) and abs(b[i] - a[i]) >= 3:
        result.append(a[i])







def calculate_sum_last_n_columns(df, cases,mapping_month,variables,index_track):
    new_columns = []  # To store the names of the new columns

    for prefix, values in cases.items():
        for value, positions in values.items():
            for position in positions:
                column_name = f'Sum_last_{value}_{prefix}_{position}'
                relevant_columns = [var for var in variables if prefix in var]
                pdb.set_trace()
                if index_track>=1:
                    if mapping_month>=len(relevant_columns):
                        index1=mapping_month-1
                    else:
                        index1 = relevant_columns.index([col for col in relevant_columns if f'_{mapping_month}' in col][0])+index_track
                else:
                    if mapping_month>=len(relevant_columns):
                        index1=mapping_month-1
                    else:
                        index1 = relevant_columns.index([col for col in relevant_columns if f'_{mapping_month}' in col][0])
                #pdb.set_trace()
                if position == 'pre':
                    # relevant_columns = relevant_columns[max(0, index1 - value):index1]
                      relevant_columns=relevant_columns
                elif position == 'post':
                   relevant_columns= relevant_columns[index1:index1+ value]  # Select columns from the end
                else:
                    raise ValueError("Position must be either 'pre' or 'post'")
                
                # Exclude the Sum_ columns from relevant_columns
                relevant_columns = [col for col in relevant_columns if not col.startswith('Sum_')]
                print(relevant_columns)
                df[column_name] = df[relevant_columns].sum(axis=1)  # Calculate sum along rows
                new_columns.append(column_name)

    # Creating a new DataFrame with only the required columns
    result_df = pd.concat([df['HCP_ID']] + [df[new_col] for new_col in new_columns], axis=1)
    result_df['segment_var']=df['segment_var']
    return result_df
