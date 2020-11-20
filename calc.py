import pandas as pd
import sys
import xlrd
import xlwt
import math
from scipy.stats import linregress
import numpy as np

from datetime import date
import utils
from datetime import date, datetime

name_slot = 7
start_index = 1
company_solt = 1
name_row_idx = 0
code_idx = 1
col_idx = 2
col_start_idx = 4
company_col_num = 8
company_num = 500
init_cap = 1000000
risk = 0.001
positions = False
companies = {}

cols_name = ['date', 'open', 'close', 'adj', 'atr', 'atr20', 'ma100']
zz_cols = ['date', 'open', 'close', 'ma200', 'ma250']

class Company:
    def __init__(self, name, code, df):
        self.name = name  # name
        self.code = code  # code
        self.datas = df  # datas
        self.mom = 0
        self.slope = 0
        self.yrr = 0
        self.adjm = 0

    def __str__(self):
        return f'company name: {self.name} ， code: {self.code}'

    def to_str(self):
        print(self.name + '' + self.code + '')

    def get_data(self, date_input, prop):
        df = self.datas
        match = df[df['date'] == date_input]
        if len(match) < 1:
            print('date input is not in the range:' + date_input)
            exit()
        return match[prop].to_list()[0]

    #
    # def get_ma100(self, date_inp):
    #     df = self.datas
    #     match = df[df['date'] == date_inp][0]
    #     if len(match) < 1:
    #         print('date input is not in the range')
    #     return match['ma100']

    def get_close(self, date):
        df = self.datas

    # calc

    # def calc_close(self):
    #     df = self.datas
    #     df["close"] = df[["close", "adj"]].apply(lambda x: x["close"] * x["adj"], axis=1)
    #     self.datas = df
    #     return df

    def calc_authd(self):
        df = self.datas
        df["authd"] = df[["close", "adj"]].apply(lambda x: x["close"] * x["adj"], axis=1)
        self.datas = df
        return df

    def calc_jump(self):
        df = self.datas
        df["jump"] = df['open'] / df['close'].shift(+1) - 1
        # df["close"] =
        self.datas = df
        return df


    def calc_log(self):
        df = self.datas
        df["log"] = df["authd"].apply(lambda x: math.log(x))
        self.datas = df
        return df

    def calc_slope(self, date_input):
        df = self.datas
        close = df[df['date'] == date_input]
        if len(close) < 1:
            print('date input is not in the range:' + date_input)
            exit()
        idx = close.index.to_list()[0]
        close_df = df.iloc[idx - 90:idx]['log'].to_list()
        arr = [i + 1 for i in range(90)]
        res = linregress(arr, close_df)
        self.slope = res.slope
        self.rsq = res.rvalue ** 2
        self.yrr = self.calc_yr()
        self.adjm = self.rsq * self.yrr
        # print(self.rsq, self.yrr, self.adjm)

    def calc_yr(self):
        yr = math.pow(math.exp(self.slope), 250) - 1
        return yr


    def calc_mom(self):
        df = self.datas
        df["log"] = df["authd"].apply(lambda x: math.log(x))
        self.datas = df
        return df

    def calc_trend(self):
        df = self.datas
        # df["trend"] = 1 if df["close"] > df["ma100"] and df["jump90"] < 0.08 else 0
        df["trend"] = df[["close", "ma100", "jump90"]].apply(lambda x: 1 if x["close"] > x["ma100"] and x["jump90"] < 0.08 else 0, axis=1)
        self.datas = df
        return df

    def calc_bid(self):
        df = self.datas
        funds = init_cap*risk
        # bid_num = funds/(df["atr20"]*100)
        # TODO
        df["bids"] = df[["trend","atr20"]].apply(lambda x: 0 if x["trend"] is 0 or x["atr20"] is 0 or isinstance(x["atr20"], str) else funds/(x["atr20"]*100), axis=1)
        self.datas = df
        return df

    def calc_cap(self):
        df = self.datas
        df["cap"] = df[["bids", "close"]].apply(lambda x: x["bids"] * x["close"] * 100, axis=1)
        self.datas = df
        return df

    # def calc_other(self):
    #     df = self.datas
    #     df["cap"] =

def datePick(d, df):
    match = df[df['date'] == d]
    if len(match) >= 1:
        return d
    else:
        return datePick(utils.addDay(d, df))


# class Data:
#     def __init__(self):
#         self.date= '' # date
#         self.open= 0  # open
#         self.close= 0 #close
#         self.adj = 0 # adj
#         self.atr = 0 # atr
#         self.atr20= 0 #atr 20
#         self.atr100 = 0 # atr 100

def main():
    origin_file = sys.argv[1]
    zz500_file = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]


    content = xlrd.open_workbook(filename=origin_file, encoding_override='gbk')
    zz500_content = xlrd.open_workbook(filename=zz500_file, encoding_override='gbk')
    # get sheets in file
    file = pd.ExcelFile(origin_file)
    zz500_file = pd.ExcelFile(zz500_file)
    sheets = file.sheet_names
    zz500_sheets = zz500_file.sheet_names
    # print(sheets)

    # get the last sheet by default
    raw_df = pd.read_excel(content, sheet_name=sheets[1])
    zz500_df = pd.read_excel(zz500_content, sheet_name=zz500_sheets[0])
    zz500_df.columns = zz_cols
    zz500_df = pd.concat([zz500_df.iloc[:, [0]], zz500_df.iloc[:, 1:5]], axis=1)
    zz500_df = zz500_df.drop([0, 1, 2])
    zz500_df = zz500_df.reset_index(drop=True)
    zz500_df['date'] = zz500_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    zz500_df.set_index('date')
    print(zz500_df)

    writer = pd.ExcelWriter('./output.xlsx')
    writer_pos = pd.ExcelWriter('./positions.xlsx')
    for d in utils.iter_weekday(start_date, end_date):
        d = d.strftime('%Y-%m-%d') # TODO date pick
        d = datePick(d, zz500_df)
        ddf = calc_object(raw_df, d) # TODO cap and position calc
        pdf = calc_position(ddf, zz500_df, d)
        pdf.to_excel(writer_pos, d)
        ddf.to_excel(writer, d)
    writer.save()
    writer_pos.save()


def calc_position(ddf, zz500, date):
    if positions is False:
        init_position(ddf, zz500, date)
    # positions



def init_position(ddf, zz500, date):
    pos = ddf[ddf['bids'] > 0]
    # TODO add adj


def calc_object(raw_df, date_input):

    for idx in range(0, company_num):
        date_df = raw_df.iloc[:, [0]]
        rang_df = raw_df.iloc[:, idx * company_col_num + 1:idx * company_col_num + 7]
        df = pd.concat([date_df, rang_df], axis=1)
        name = df.columns[1]
        df.columns = cols_name
        code = df.iat[0, 1]
        df = df.drop([0, 1, 2])
        df = df.reset_index(drop=True)
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        company = Company(name, code, df)
        df = company.calc_authd()
        df = company.calc_log()
        df = company.calc_jump()


        # df = company.calc_jump_90()

        def rowFumc(row):
            idx = row.name
            if idx < 90:
                return 0
            else:
                res = np.max(df.iloc[idx - 90:idx, [9]])
                return res['jump']
            # print(idx)

        df["jump90"] = df.apply(rowFumc, axis=1)
        df = company.calc_trend()
        df = company.calc_bid()
        df = company.calc_cap()
        company.calc_slope(date_input)
        companies[code] = company

    # print(companies)
    df_out = pd.DataFrame([], columns=('name', 'code', 'adjm', 'atr20', 'ma100', 'jump90','close', 'trend', 'bids', 'cap', 'adj'))
    for i in companies:
        com = companies[i]
        size = df_out.index.size
        row = [com.name, com.code, com.adjm, com.get_data(date_input, 'atr20'),
               com.get_data(date_input, 'ma100'), com.get_data(date_input, 'jump90'),com.get_data(date_input, 'close'),com.get_data(date_input, 'trend'),com.get_data(date_input, 'bids'),com.get_data(date_input, 'cap'), com.get_data(date_input, 'adj')]
        df_out.loc[size] = row
        # df_out.append([{'name': com.name, 'code': com.code, 'adjm': com.adjm, 'atr20':company.get_data(date_input,'atr20'), "ma100":company.get_data(date_input,'ma100'),'jump90':company.get_data(date_input,'jump90') }], ignore_index=True)
        # print(df_out)

    # print(df_out)
    df_out = df_out.sort_values(by=['adjm'], ascending=False)
    df_out = df_out[:100]
    df_out.reset_index(drop=True)
    return df_out
    # df_out.to_excel('./output-'+date_input+'.xls')


# map = {}
# for ind, row in df.iterrows():
#     print(ind)
#     # print(row[0], row[1], row[2])
#     code = row[1]
#     change_date = row[3]
#     if str(code) == 'NaT':
#         break
#     if utils.compare_time(str(date_time), str(change_date)) > 0:
#         if row[4] == u'纳入':
#             # print('纳入')
#             map[code] = row
#         else:
#             # print('剔除')
#             map.pop(code)
#     else:
#         print(123)
# # print(len(map))
#
# my_df = pd.DataFrame.from_dict(map, orient='index')
#
# # print(my_df)
# my_df.to_excel('./output'+date_time+'.xls')


if __name__ == "__main__":
    main()
