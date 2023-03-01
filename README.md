# 用notion实战柳比歇夫时间统计法
## python调用notion-API接口准备工作
首先需要在[https://notion.so/my-integrations](https://notion.so/my-integrations)中新建一个intergration，新建完成之后即可获取到该intergration的Token，一般是以secret_开头的字符串，后面有用。

然后在要访问的数据库里面，添加一个connection，这里我的intergration叫Counter
![count_notion](https://github.com/qiao1025566574/notion/blob/main/count_notion.png)

官方文档：
https://developers.notion.com/docs/authorization
## 代码说明
python调用了notion-sdk-py库, 代码中的token获取方式为：可以在这里写字符串，但不安全
```
notion = Client(auth = os.environ['NOTION_TOKEN'])
```
## Install
```python
pip install notion_client
```
notion-sdk-py库链接：
https://github.com/ramnes/notion-sdk-py
## Run
```shell
mkdir time
mkdir money
#生成某一天的统计数据，统计结果在命令行显示，图表在time文件夹中
python stat_day_time.py
#生成某一月的统计数据，统计在命令行显示，图表在time文件夹中
python stat_month_time.py
#生成某一月的统计数据，统计结果在命令行显示，图表在money文件夹中
python stat_money.py
```
## Time统计表形式
一共五列，
Number是主键，必须是日期-编号的形式，方便代码读取
Content是选择项，可以任意指定
Cost是文本项，必须是1h3m这样的形式，方便代码读取
Cost(h)是数字项，与代码无关，随意指定，删了也行
Cost(m)是数字项，与代码无关，随意指定，删了也行
![time notion](https://github.com/qiao1025566574/notion/blob/main/time_notion.png)
## Money统计表形式
一共五列，
Number是主键，必须是日期-编号的形式，方便代码读取
Content是选择项，可以任意指定
Cost是数字项，必须是数字
![money notion](https://github.com/qiao1025566574/notion/blob/main/money_notion.png)
