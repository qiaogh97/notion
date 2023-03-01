# 用notion实战柳比歇夫时间统计法
## 代码说明
python调用了notion-sdk-py库
直接pip install就行
notion-sdk-py库链接：
https://github.com/ramnes/notion-sdk-py
## Time统计表形式
一共五列，
Number是主键，必须是日期-编号的形式，方便代码读取
Content是选择项，可以任意指定
Cost是文本项，必须是1h3m这样的形式，方便代码读取
Cost(h)是数字项，与代码无关，随意指定，删了也行
Cost(m)是数字项，与代码无关，随意指定，删了也行
![time notion](https://github.com/qiao1025566574/notion/raw/main/time_notion.png)
## Money统计表形式
一共五列，
Number是主键，必须是日期-编号的形式，方便代码读取
Content是选择项，可以任意指定
Cost是数字项，必须是数字
![money notion](https://github.com/qiao1025566574/notion/raw/main/money_notion.png)