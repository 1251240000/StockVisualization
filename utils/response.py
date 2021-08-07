from django.http import JsonResponse


def rest_resp(code=200, msg='OK', results={}):
    return JsonResponse({
        'code': code,
        'msg': msg,
        'results': results,
    })


class StockStdResp:
    NotFound = rest_resp(code=404, msg='Stock Not Found')
    Bad = rest_resp(code=502, msg='Bad Stock API')
    TimeOut = rest_resp(code=504, msg='Stock API Time-out')
