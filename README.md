# sqlonline
# 安装
### 1.安装依赖
``` bash
pip install -r requirements.txt
```

### 2.初始化数据库
``` bash
python manage.py makemigrations
python manage.py migrate
```

### 3.创建管理员账号
``` bash
python manage.py createsuperuser
```

### 4.启动
``` bash
python manage.py runserver
```

如果想使用uwsgi+nginx，也是可行的，可以参考uwsgi-sql.ini的配置。安装就不多说了。



# License
MIT
