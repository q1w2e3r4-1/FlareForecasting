# FlareForecasting
## 爬虫部分
在这里列举一些你可能会遇到的问题。

#### 1.报错data/xxx.csv不存在。
说明你现在所在的目录级和我的不一样，这个很可能是由于IDE不同所导致(我用的Pycharm)
你只需要试试其他层级的路径，例如改成```"spider/data/xxx.csv"```或者```"FlareForecasting/spider/data/xxx.csv"```

#### 2.关于爬取耀斑类别信息
程序写在spider.py中，如果你用的不是pycharm，可能要去掉```if __name__ == '__main__'```才可以运行。
此程序允许你自行设置爬取的起止时间，然后最终得到的结果就是data目录下的对应时间的那个csv文件。(eg.20180101-20181231.csv)

此程序会输出某一时间段内的所有耀斑类别信息(**包括N类**)，所以可能需要做进一步处理

#### 3.关于耀斑类别信息的进一步处理
我们在data_processer.py对耀斑信息进行处理，目前进行的处理为去除N类 + 去重，当然你也可自行修改（应该不难）
最终将结果输出到output.csv中

**注意：运行前请确认csv_url中的文件为你想要处理的文件**

**注意，此操作会覆盖之前的output.csv文件，注意保存**

如果你对python比较熟悉的话，建议你将几十年的数据全部爬到一个文件里，然后需要的时候只需要用data_processer选取某一时间段即可，这样就避免重复爬取了