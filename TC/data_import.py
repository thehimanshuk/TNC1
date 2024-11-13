import pandas as pd
from datetime import datetime
from tomlkit import date
import tc.config as config
import pdb
from tc.log_config import setup_logging
setup_logging()

import logging
# Import Module:

class ImportData:
    def __init__(
        self,
        file_path: str,
        data_format: str,
        date_format: str,
        date_col: str,
        categorical_cols: list,
        numerical_cols: list,
        hcp_identifier: str,
        tc_present: bool,
        week : bool
    ):
        self.file_path = file_path
        self.data_format = data_format
        self.date_format = date_format
        self.date_col = date_col
        self.categorical_cols = categorical_cols
        self.numerical_cols = numerical_cols
        self.hcp_identifier = hcp_identifier
        self.tc_present = tc_present
        self.week=week

    def read_csv(self):
        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            logging.error(f"File not found at {self.file_path}")
            raise FileNotFoundError(f"File not found at {self.file_path}")
        except Exception as e:
            logging.error(f"Unexpected error occurred while reading {self.file_path} - {str(e)}")
            raise Exception(f"Unexpected error occurred: {str(e)}")
        else:
            if self.tc_present == False:
                df = self.create_tc_column(df)
                
            if self.data_format == "long":
                df = self.pivot_long_to_wide(df)
                

            logging.info(f"File {self.file_path} imported successfully.")

            return df

    def date_conversion(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            data = data.sort_values(self.date_col)
            if self.date_format in config.format_mapping:
                format_string = config.format_mapping[self.date_format]
                data[self.date_col] = pd.to_datetime(
                    data[self.date_col], format=format_string
                ).dt.strftime("%b%y")
            logging.info(f"Date conversion was successfully.")
            return data
        except ValueError as e:
            logging.error(f"Date conversion error: {e}.")
            raise Exception(f"Error: {e}. Please provide correct date format")


    def pivot_long_to_wide(self, data) -> pd.DataFrame:
        try:
            # Pivot the dataframe
            data = data.filter(
                regex=f"^({self.numerical_cols}|{self.categorical_cols}|{self.date_col})",
                axis=1
            )
            data = self.date_conversion(data=data)
            unique_date_values = list(data[self.date_col].unique())
            data["Date1"] = pd.Categorical(
                data[self.date_col], categories=unique_date_values, ordered=True
            )

            pivot_df = data.pivot_table(
                index=self.hcp_identifier, columns="Date1", values=self.numerical_cols # type: ignore
            )

            # Flatten the multi-level column index
            pivot_df.columns = [
                "_".join(col).rstrip("_") for col in pivot_df.columns.values
            ]
            # Reset the index
            pivot_df = pd.DataFrame(pivot_df)
            pivot_df.reset_index(inplace=True)
            merged_data = pd.merge(
                pivot_df,
                data.drop_duplicates(subset=[self.hcp_identifier]),
                on=self.hcp_identifier,
            )
            logging.info(f"Pivoting was successfully.")
            return merged_data
        except Exception as e:
            logging.error(f"An error occurred during pivoting: {e}")
            print(f"An error occurred:Please upload long format data,Check data for long-wide conversion")
            raise Exception("Pivoting error, check data format and structure.")
            return pd.DataFrame()
        
    # define a function that creates one more column called TC where assigns if a an HCP is test or control. For that here are some rules
    # 1. if the sum value of the config.event_hcp_identifier after post start for every config.hcp_hcp_identifier > 0 then it's a test HCP else it's a control HCP
    # 2. hcps who has alerts in only post will be considered as T it should not have engagements in Pre period  
    def create_tc_column(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            data["TC"] = "Control"
            
            # Convert to datetime object
            date_obj = datetime.strptime(config.event_date, "%b-%Y")

            # Format to desired output
            event_date = date_obj.strftime("%Y-%m")
            
            # event_date = pd.to_datetime(event_date,format='%Y-%m')
            for hcp in data[self.hcp_identifier].unique():
                hcp_data = data[data[self.hcp_identifier] == hcp]
                post_data = hcp_data[hcp_data[self.date_col] > event_date]
                if post_data[config.event_identifer].sum() > 0:
                    data.loc[data[self.hcp_identifier] == hcp, "TC"] = "T"
                else:
                    data.loc[data[self.hcp_identifier] == hcp, "TC"] = "C"
            logging.info(f"TC column was created successfully.")
            return data
        except Exception as e:
            logging.error(f"An error occurred during creating TC column: {e}")
            raise Exception("TC column creation error.")


# dataset_import = ImportData(
#     file_path="TC_Data_Long.csv",
#     data_format="long",
#     date_format=config.date_format,
#     date_col=config.date_columns,
#     categorical_cols=config.categorical_columns,
#     numerical_cols=config.numerical_columns,
#     hcp_identifier=config.hcp_hcp_identifier,
#     week=False

# )
# read_data = dataset_import.read_csv()
# print(read_data)
# print(read_data["Date"])

# if read_data is not None:
#     output_path = "C:/Datazymes/Github/TestandControl-Python/apps/tc_python/TC_Data_Transformed.csv"
#     read_data.to_csv(output_path, index=False)
#     print(f"Data exported to {output_path}")
# else:
#     print("No data to export.")