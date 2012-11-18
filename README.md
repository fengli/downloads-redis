downloads-redis
===============

show top downloads in a certain period of time in redis

安装
--------
* 安装pip(如果没有安装过的话)： `easy_install pip`
* 安装downloads-redis： `pip install -e git://github.com/fengli/downloads-redis.git` 

快速使用
--------

使用非常简单，当然你需要首先启动redis
```bash
redis-server
```

之后你就可以这样使用downloads模块：

```python
import downloads
md = downloads.Download ()

# 每当有一次下载的时候，你需要使用incr纪录这次下载。downloads模块会
# 自动加上下载的时间标签

md.incr ('item1')  #increase the download count for 'item1'
md.incr ('item2')  #increase the download count for 'item2'
md.incr ('item2')  #increase the download count for 'item2'

#get the top 50 most downloads today
items = md.most_downloads_tody (50)
print items
[('item2',2.0), ('item1', 1.0)]

就是这么简单!
```

详细的接口描述：
```python
def most_downloads_today (self, n=50)
```
返回今天top n的下载, default n=50
```python
def most_downloads_all_time (self, n=50):
```
返回所有时间内的top n下载, default n=50
```python
def most_downloads_in_past_week (self, n=50):
```
返回最近7天内的top n下载, default n=50
```python
def most_downloads_in_past_month (self, n=50):
返回最近31天内的top n下载，default n=50
```python
def most_downloads_in_past_week_complex (self, n=50):
```
返回最近7天内的top n下载，并且返回top n下载最近7天内每天的下载量
```python
def most_downloads_in_past_month_complex (self, n=50):
```
返回最近30天内top n下载，并且返回top n下载最近7天内每天的下载量

Bring to you by:
--------------------

* 爱看豆: http://ikandou.com
