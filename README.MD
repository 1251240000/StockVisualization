# Tushare股票数据可视化平台

基于`python3.8.0`和`Django2.1.8` 实现Tushare股票数据可视化平台（毕业设计）。

[一个示例](http://hrlu.me:8000/)

## 主要功能：
- 股票代码搜索
- K线图、平均线绘制
- 模拟股票交易
- 时间序列预测

## 安装

克隆项目至本地：`git clone https://github.com/1251240000/sdcs.git`

pip安装环境： `pip install -Ur requirements.txt`

### 配置
#### 迁移数据库
执行：` python3 manage.py makemigrations `
之后执行：` python3 manage.py migrate `

#### 创建超级用户
执行：` python3 manage.py createsuperuser `

##### 配置验证码
如果需要使用验证码模块，你需要申请[阿里云](https://dysms.console.aliyun.com/)短信签名及模版，并修改` ui/sms.py `：
```python
accessKeyId = '你的AccessKey ID'
accessSecret = '你的AccessKey Secret'

def SendSms(pnum, vcode):

    # ··· ···
    request.add_query_param('SignName', "签名名称")
    request.add_query_param('TemplateCode', "模版CODE")
    # ··· ···
```

##### 配置wsgi + Nginx
如果需要配置wsgi+Nginx ，你需要：
- 配置Nginx支持uwsgi及虚拟目录：
```bash
server {
    listen       8000;

    location / {
    include uwsgi_params;
    uwsgi_pass 0.0.0.0:8001;
    }

    location /static {
        alias 静态文件目录;
    }
}
```
- 收集静态文件：` python3 manage.py collectstatic `

- 配置uwsgi.ini：
```bash
[uwsgi]
socket = 0.0.0.0:8000
chdir = 目录
wsgi-file = 目录/wsgi.py
processes = 4
threads = 2
master = True
pidfile = uwsgi.pid
daemonize = uwsgi.log
```

## 运行

执行： ` python3 manage.py runserver 0.0.0.0:8000 ` 或 ` uwsgi uwsgi.ini `

浏览器打开: http://127.0.0.1:8000/ 
