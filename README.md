# 500clac

中证 500 成分股动量指标计算，获得指定日期中证 500 的动量与跳空指标。

安装依赖
`pip install -r requirements.txt`

运行
`python calc.py ./data.xlsx ./zz500.xlsx 2007-05-06 2007-05-31`

- ./data.xlsx 基础数据
- ./zz500.xlsx 是上证 500 的价格导出数据
- 日期第一个是开始日期，第二个为结束日期
- 输出文件包含了 output.xlsx 和 position.xlsx
    - output.xlsx 是按照日期为区分的股票统计数据，按照动量排名
    - position.xlsx 是根据日期 rebalance 和调整仓位过后的输出文件
    
日期参数可以按照 yyyy-mm-dd 的格式替换

脚本输出 output-yyyy-mm-dd.xlsx 文件

