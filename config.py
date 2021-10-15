''' 配置MySQL数据库
    DB_HOST: 服务器地址（IP地址或主机名）
    DB_USER: 用户名
    DB_PASSWD: 用户密码
    DB_NAME: 数据库名（系统会自动创建数据库）
'''
DB_HOST = 'localhost'
DB_USER = ''
DB_PASSWD = ''
DB_NAME = 'stockvisualization'


''' 配置缺省股票代码 
'''
DEFAULT_STOCK = '000001.SZ'

DEFAULT_PERIOD = 365 * 2

''' 其他
    TUSHARE_TOKEN: Tushare接口密钥
'''
TUSHARE_TOKEN = '28f87746bb4a4ba473955c650ce102cea7e5d07affc5a18266a12a1a'

