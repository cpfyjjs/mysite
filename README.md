### 个人网站建设

#### 数据库模型
用户数据
1. 电话
2. 头像
3. 创建时间
4. 博客

博客

1. 标题
2. 个人博客介绍
3. 博客主题

文章

1. 标题
2. 作者
3. 文章描述
4. 创建时间
5. 评论数
6. 点赞数
7. 踩数
8. 文章所属分类
9. 文章标签

文章详情页

1. 文章内容
2. 文章

个人博客文章分类

1. 分类标题
2. 外键博客

标签

1. 标签名
2. 外键博客

文章与标签关系表

1. 文章
2. 标签

点赞踩表

1. 用户
2. 文章

评论表

1. 用户
2. 文章
3. 父评论
4. 评论内容
5. 评论时间

#### mysql 数据库的安装

安装

1. sudo apt-get install mysql-server
2. sudo apt-get install mysql-client
3. sudo apt-get install libmysqlclient-dev

启动、关闭服务和查看运行状态

1. sudo service mysql start
2. sudo service mysql stop
3. sudo service mysql status

卸载mysql

1. sudo apt-get auto remove --pure mysql-server-5.7

2. sudo aapt-get remove mysql-server

3. sudo apt-get remove mysql-common

4. sudo rm -rf /etc/mysql   /var/lib/mysql

   清理残留数据

   ```
   dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P 
   ```

5. sudo apt autoremove 
6. sudo apt autoreclean





