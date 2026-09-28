# Python Music

基于 Python 的桌面音乐软件，集成爬虫、GUI 界面、数据可视化和数据库存储，支持音乐搜索、在线播放、下载收藏、热门歌曲查看和数据分析。

## 功能特性

- **音乐搜索**：通过爬虫实时搜索歌手或歌曲
- **在线播放**：点击歌名即可播放，支持上一首/下一首、播放/暂停、自动连播
- **下载与收藏**：歌曲下载到本地，收藏记录保存到数据库
- **歌词下载**：获取并保存歌词文件
- **热门排行**：查看当前热门歌曲和热门歌手
- **数据分析**：爬虫数据可视化展示（饼图等图表）
- **账号系统**：注册/登录，用户数据持久化到 MySQL

## 界面预览

**登录页**

![登录页](https://img-blog.csdnimg.cn/dafbf7008d364c5393064751f6012afa.png)

![登录注册](https://img-blog.csdnimg.cn/aa48c0704abb4c87955601287f70b82a.png)

**主界面**

![主界面](https://img-blog.csdnimg.cn/af83fc99068a4940bef91e4c1bc8b136.png)

**爬虫数据展示**

![爬虫数据展示](https://img-blog.csdnimg.cn/e2e162ed20b34bcc9d234f024a610f1e.png)

**数据分析展示**

![数据分析](https://img-blog.csdnimg.cn/a44d346dccbe482bbfb3947d73f9a97b.png)

![热门歌手歌曲量占比饼图](https://img-blog.csdnimg.cn/7ae6a729860d426cbe56f95684c326b1.jpg)

**数据库展示**

![数据库](https://img-blog.csdnimg.cn/7d5838b18073444bab0bfa6987faa9a2.png)

## 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.9 | 运行环境 |
| Tkinter | GUI 界面 |
| Requests / BeautifulSoup | 爬虫数据抓取 |
| Matplotlib | 数据可视化 |
| PyMySQL | 数据库操作 |
| MySQL | 数据持久化 |

## 快速开始

**环境准备**

```bash
# 1. 安装依赖
pip install pymysql matplotlib requests beautifulsoup4

# 2. 初始化数据库
mysql -u root -p < python大作业数据库.sql
```

**数据库配置**

在代码中修改数据库连接信息以匹配你的本地环境：

```python
host='localhost', user='root', password='your_password', db='pyhomework'
```

**启动运行**

```bash
python "python's homwork.py"
```

注册账号并登录，进入主界面后即可搜索、播放、下载和收藏音乐。

> **注意**：启动前请确保网络连接正常，程序进入主界面时会自动触发爬虫搜索。
