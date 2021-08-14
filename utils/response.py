from rest_framework.response import Response

def rest_resp(code=200, msg='OK', results={}):
    return Response(data={
        'code': code,
        'msg': msg,
        'results': results,
        'count': len(results),
    })


class StockStdResp:
    NotFound = rest_resp(code=404, msg='Stock Not Found')
    Bad = rest_resp(code=502, msg='Bad Stock API')
    TimeOut = rest_resp(code=504, msg='Stock API Time-out')
