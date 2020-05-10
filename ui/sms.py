from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

#accessKeyId = ''
#accessSecret = ''

def SendSms(pnum, vcode):
    '''client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', pnum)
    request.add_query_param('SignName', "")
    request.add_query_param('TemplateCode', "")
    request.add_query_param('TemplateParam', "{\"code\":\""+ vcode +"\"}")

    response = client.do_action(request)'''
    pass
