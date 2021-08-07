# Tushare股票数据可视化平台

基于`python3.9.5`和`Django3.1.12` 实现Tushare股票数据可视化平台。
*距离上次编辑次项目已经时隔一年多了，自认为这一年在水平上还是有不小提升的，遂决定将此项目重构，同时也能梳理下所学知识点。*
[示例](http://sv.hrlu.cn/)

## 主要功能：
- 股票代码搜索
- K线图、平均线绘制
- 模拟股票交易
- 时间序列预测

## 安装

克隆项目至本地：`git clone https://github.com/1251240000/StcokVisualization.git`
pip安装环境： `pip3 install -r requirements.txt`

### 配置
#### 迁移数据库
执行：` python3 manage.py makemigrations `
之后执行：` python3 manage.py migrate `

#### 生成/刷新测试数据
执行：` python3 manage.py refresh_data `

#### 创建超级用户
执行：` python3 manage.py createsuperuser `

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
