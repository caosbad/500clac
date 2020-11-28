import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
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
current_balance = 1000000
risk = 0.001
positions = False
companies = {}

is_double = False


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
        global init_cap
        df = self.datas
        funds = init_cap*risk
        # bid_num = funds/(df["atr20"]*100)
        # TODO
        df["bids"] = df[["trend","atr20"]].apply(lambda x: 0 if x["trend"] is 0 or x["atr20"] is 0 or isinstance(x["atr20"], str) else math.floor(funds/(x["atr20"]*100)), axis=1)
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

def get_data(df, prop, value):
    match = df[df[prop] == value]
    if len(match) < 1:
        print('data input is not in the range:' + df + prop + value)
        exit()
    return match[prop].to_list()[0]
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
    # print(zz500_df)

    writer = pd.ExcelWriter('./output.xlsx')
    writer_pos = pd.ExcelWriter('positions1.xlsx')
    for d in utils.iter_weekday(start_date, end_date):
        d = d.strftime('%Y-%m-%d') # TODO date pick
        d = datePick(d, zz500_df)
        ddf = calc_object(raw_df, d) # TODO cap and position calc
        pdf = calc_position(ddf, zz500_df, d)
        pdf.to_excel(writer_pos, d)
        ddf.to_excel(writer, d)
    writer.save()
    writer_pos.save()

def calc_cap(ddf):
    global init_cap
    for index, p in positions.iterrows():
        match = ddf[ddf['code'] == p.code]
        if len(match) >0:
            cap = match['close'].to_list()[0] * p.bids * 100
        else:
            cap = p.cap
        positions.loc[index, 'cap'] = cap
    init_cap = positions['cap'].sum() + current_balance
    return init_cap

def calc_position(ddf, zz500, date):
    global positions
    global is_double
    global init_cap
    if positions is False:
        return init_position(ddf, zz500, date)
    else:
        is_double = not is_double
    # init_cap = positions['cap'].sum() + current_balance
    caps = calc_cap(ddf)
    print(date, 'caps is ', caps)
    print(date, 'current-balance', current_balance)
    new_pos = change_position(ddf, zz500, date)
    positions = new_pos
    return new_pos

def change_position(ddf, zz500, date):
    global positions
    global is_double
    global init_cap
    global is_double
    # check position

    positions['adj1'] = positions['adj'].apply(lambda x: x)
    for index, p in positions.iterrows():
        match = ddf[ddf['code'] == p.code]

        # exclude
        if len(match) == 0 :
            sell_postion(index, p, ddf)
            break
        # trend lost
        close = match['close'].to_list()[0]
        ma100 = match['ma100'].to_list()[0]
        positions.loc[index, 'close'] = close
        positions.loc[index, 'ma100'] = ma100
        if close < ma100:
            positions.loc[index, 'trend'] = 0
            sell_postion(index, p, ddf)
            break

        # over buying
        jump90 = match['jump90'].to_list()[0]
        adjm = match['adjm'].to_list()[0]
        adjm100 = ddf.at[100, 'adjm']

        positions.loc[index, 'adjm'] = adjm
        positions.loc[index, 'jump90'] = jump90

        if adjm < adjm100 or jump90 > 0.08:
            sell_postion(index, p, ddf)
            break

        # recalc cap of position
        adj = match['adj'].to_list()[0]
        positions.loc[index, 'adj'] = adj


    positions['cap'] = positions[["bids", "close", "adj", "adj1"]].apply(lambda x: (x["bids"] * x["close"] * x["adj"] * 100)/x["adj1"], axis=1)

    if is_double:
        positions = rebalance(ddf, zz500, date)

    # print(current_balance, '====2')
    positions = buy_position(ddf, zz500, date)
    positions = positions[positions['hold'] > 0]
    init_cap = positions['cap'].sum()
    positions['sum'] = positions['cap'].cumsum()

    # positions = buy_position(ddf, zz500, date)
    return positions

def rebalance(ddf, zz500, date):
    global positions
    global current_balance
    global init_cap
    print('rebalance', date)
    funds = init_cap * risk
    repo = pd.concat([positions], axis=1)
    # repo['adj1'] = positions['adj']
    ddf['rebids'] = ddf['atr20'].apply(lambda x: 0 if x==0 else math.floor(funds/(x*100)))

    for index, p in repo.iterrows():
        match = ddf[ddf['code'] == p.code]
        if len(match) == 0:
            break

        rebids = match['rebids'].to_list()[0]
        if rebids == 0:
            break
        # TODO test rebids and pos['hold']
        diff = rebids - p.bids
        # print('====', diff, '====', 'rebids:', rebids, 'bids', p.bids, '====', p.code)
        if diff > 0:
            add_position(diff, p ,index, repo)
        elif diff < 0 :
            cut_position(diff, p, index, repo)

    # print(current_balance, '=====')
    return repo


def add_position(bids, p, idx, repo):
    global init_cap
    global current_balance
    add = p.close * bids * 100
    if current_balance< add :
        return

    current_balance -= add
    # print('add position', add, current_balance)
    cap = add + p.cap

    repo.loc[idx, 'cap'] = cap
    repo.loc[idx, 'bids'] = bids + p.bids


def cut_position(bids, p, idx, repo):
    global init_cap
    global current_balance
    bids = abs(bids)
    cut = p.close * bids * 100
    current_balance += cut
    # print('cut position', cut, current_balance)
    cap = p.cap - cut

    repo.loc[idx, 'cap'] = cap
    repo.loc[idx, 'bids'] = p.bids - bids



def sell_postion(index, p, ddf):
    global current_balance
    global positions
    match = ddf[ddf['code'] == p.code]
    close = 0
    if len(match) > 1:
        close = match['close'].to_list()[0]
    else:
        close = p.close
    cap = p.bids * 100 * close
    current_balance += cap
    print('sell position', cap, current_balance)
    # update position state
    positions.loc[index, 'bids'] = 0
    positions.loc[index, 'cap'] = 0
    positions.loc[index, 'hold'] = 0
    positions.loc[index, 'close'] = close



def buy_position(ddf, zz500, date):
    global positions
    global init_cap
    global current_balance
    data_pos = ddf[ddf['bids'] > 0]
    zz500_record = zz500[zz500['date'] == date]
    # 剩余资金判断
    # if not check_balance(data_pos):
    #     return positions
    # 价格趋势判断
    close = zz500_record['close'].to_list()[0]
    ma200 = zz500_record['ma200'].to_list()[0]
    if close < ma200:
        return positions

    new_position_need = compare_col(data_pos, positions)
    for code in new_position_need:
        bid = data_pos[data_pos['code'] == code]
        close = bid['close'].to_list()[0]
        min_cap = close * 100
        if current_balance < min_cap:
            break

        ma100 = bid['ma100'].to_list()[0]
        if close < ma100:
            break

        jump90 = bid['jump90'].to_list()[0]
        if jump90 > 0.08:
            break

        bids = bid['bids'].to_list()[0]
        max_bids = math.floor(current_balance / min_cap)
        if max_bids > bids:
            current_balance -= bids*min_cap
            print('buy position 1', bids * min_cap, current_balance)
        else:
            current_balance -= max_bids * min_cap
            bids = max_bids
            positions.loc[positions['code'] == code, 'bids'] = bids
            print('buy position 2', max_bids * min_cap, current_balance)
        positions.loc[positions['code'] == code, 'close'] = close
        positions.loc[positions['code'] == code, 'hold'] = 1

        positions = positions.append(bid.to_dict(), ignore_index=True)

    # TODO
    return positions


def compare_col(dff, pos):
    pos_col = pos.to_dict(orient='list')['code']
    data_col = dff.to_dict(orient='list')['code']
    diff = list(set(data_col) - set(pos_col))
    return diff

# 初始化仓位
def init_position(ddf, zz500, date):
    global is_double
    global positions
    pos = ddf[ddf['bids'] > 0][:100]
    pos['sum'] = ddf['cap'].cumsum()
    pos['top100'] = pos["bids"].apply(lambda x : x/x)
    pos['hold'] = ddf['cap'].apply(lambda x: 0)
    # ser = pos[pos['sum'] <= init_cap]
    pos = init_buy_position(pos, zz500, date)
    # print(pos)
    positions = pos[pos['hold'] > 0]
    is_double = False
    return positions


def init_buy_position(pos, zz500, date):
    global current_balance
    zz500_record = zz500[zz500['date'] == date]
    # 剩余资金判断
    # if not check_balance(pos):
    #     return pos
    # 价格趋势判断
    close = zz500_record['close'].to_list()[0]
    ma200 = zz500_record['ma200'].to_list()[0]
    if close < ma200:
        return pos

    for index, row in pos.iterrows():
        if current_balance < row.close * 100:
            break

        if current_balance < row.cap:
            break

        if row.jump90 > 0.08:
            break
        # 最小手数
        if current_balance < row.close * 100:
            break
        # TODO 剩余不够如何处理
        current_balance = current_balance - row.cap
        pos.loc[index, 'hold'] = 1
        pos[index] = row

    return pos






def check_balance(pos):
    sum_price = pos[pos['bids'] > 0]['close'].sum()
    if(sum_price * 100 > current_balance):
        return False


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
    df_out = df_out[:150] # TODO keep the 500 list for confirm the position
    df_out = df_out.reset_index(drop=True)
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
