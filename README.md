# 用notion实战柳比歇夫法
# 先跑个demo试试？
## 1.在notion中新建一个数据库，随便填点数据，如下图
一共三列，

Number是主键，必须是日期-编号的形式，方便代码读取

Content是选择项，可以任意指定

Cost是文本项，必须是1h3m这样的形式，方便代码读取

![demo notion](https://github.com/qiao1025566574/notion/blob/main/demo_table.png)
## 2.新建一个Intergration
在[https://notion.so/my-integrations](https://notion.so/my-integrations)中新建一个intergration，新建完成之后即可获取到该intergration的Token，一般是以'secret_'开头的字符串，后面有用。
## 3.在notion数据库中添加Connection
进入数据库页面，一定不能是数据库的父页面，点击右上角三个点，即可出现Add connections选项

![demo connection](https://github.com/qiao1025566574/notion/blob/main/demo_connection.png)

官方文档：
https://developers.notion.com/docs/authorization
## 4.安装python库notion_client
```
pip install notion_client
```
notion-sdk-py库链接：
https://github.com/ramnes/notion-sdk-py
## 5.获取datasetbase_id
一定要进入数据库页面，不能是数据库的父页面当中，获取数据库的网址，例如，我的数据库页面网址是：
```
https://www.notion.so/qiaogh/8d19ff252abf43969d12ab1b9d99b137?v=c2d791468afa406c8bdd4213fc05666d
```
这里datasetbse_id就是8d19ff252abf43969d12ab1b9d99b137，即斜杠最后一项，问号之前的字符串。
如果你获取的网址形式和我不一样，没有问号，说明不是数据库页面，很可能进入了数据库的父页面。如果是这样的情况，点击数据库右上角的箭头进入数据库页面，如下图：

![](https://github.com/qiao1025566574/notion/blob/main/demo_database.png)

## 6.配置代码超参数
### 6.1 配置TOKEN
例如stat_day_time.py，在第44行
```
notion = Client(auth=os.environ["NOTION_TOKEN"])
```
替换为
```
#填入自己Intergration的token
notion = Client(auth='自己的token')
```
如果是linux系统，在bashrc里面写
```
export NOTION_TOKEN='自己的TOKEN'
```
就不用替换了
## 6.2 配置datasetbase_id
例如stat_day_time.py，在第178行，替换为自己的database_id
## 6.3 配置日期
例如stat_day_time.py，在第177行，设置year, month, day，均为int型，要保证数据库里面有这一天的数据
## 7.运行代码
```
mkdir time
#生成某一天的统计数据，统计结果在命令行显示，图表在time文件夹中
python stat_day_time.py
```


# 其他说明
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