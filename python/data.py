import pandas as pd

class Data():

    def get_data(self):
        self.law_data = pd.read_csv('./application/static/SturmData.csv')

        self.clean_data()

        self.year_columns = ['debtfree','effectivemwpa','earnings','wills','soletrader']
        self.year_column_labels = ['Debt Free','Effective MWPA','Earnings','Wills','Sole Trader']
        self.law_dict = {key:value for (key,value) in list(zip(self.year_columns,self.year_column_labels))}

        debtfree_desc = "Year of passage of state law protecting married women's separate property from her husband's debts"
        effectivemwpa_desc = "Year of passage of state law granting married women control and management rights over their separate property"
        earnings_desc = "Year of passage of state law granting married women ownership of their wages or earnings on par with other separate property"
        wills_desc = "Year of passage of state law granting married women the ability to write wills without their husband's consent or other restrictions"
        soletrader_desc = "Year of passage of state law granting married women as a class the right to sign contracts and engage in business without consent of husband"
        desc_list = [debtfree_desc,effectivemwpa_desc,earnings_desc,wills_desc,soletrader_desc]

        self.desc_dict = {key:value for (key,value) in list(zip(self.year_columns,desc_list))}

    def clean_data(self):
        # convert all numeric columns to a nullable Int64 dtype
        self.law_data[self.law_data.select_dtypes(include=['int64','float64']).columns.to_list()] = self.law_data[self.law_data.select_dtypes(include=['int64','float64']).columns.to_list()].astype('Int64')

        # convert all dates past 1920 to NA's per the Codebooks note
        date_columns = ['debtfree','effectivemwpa','earnings','wills','soletrader']
        # self.law_data[date_columns] = self.law_data[date_columns].mask(self.law_data[date_columns] > 1920, pd.NA)
        for column in date_columns:
            self.law_data[column].mask(self.law_data[column] > 1920, pd.NA, inplace=True)