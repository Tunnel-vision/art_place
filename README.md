# art_place
django-nuxtjs 搭建的基于艺术flux，来展示艺术发展趋势的web服务

### quick start
* 需要安装 django版本 为 2.0.2版本


1. 删除 flux/migrations/ *.initial.py
2. 启动 mysql后台 systemctl start mysqld
3. python manage.py makemigrations 生成迁移记录
4. python manage.py migrate 迁移数据 
5. python manage.py runserver 0:80   终端运行
6. 后台运行的话 nohup python manage.py runserver 0:80  &



### 数据导入: lx.py

1. http://127.0.0.1:80/flux/tag PUT 方法
2. http://127.0.0.1:80/flux/article