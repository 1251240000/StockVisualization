import re
import datetime


class Fdate:
    def __init__(self, raw=datetime.date.min):
        if isinstance(raw, str):
            if re.match(r'^\d{4}[01]\d[0123]\d$', raw):
                self._date = datetime.datetime.strptime(raw, r'%Y%m%d').date()
            elif re.match(r'^\d{4}-[01]\d-[0123]\d$', raw):
                self._date = datetime.datetime.strptime(raw, r'%Y-%m-%d').date()
        elif isinstance(raw, datetime.date):
            self._date = raw
        elif isinstance(raw, datetime.datetime):
            self._date = raw.date()

        if not hasattr(self, '_date'):
            raise ValueError(f'Cannot recognize {raw} as a date.')

    def __str__(self, ):
        return self._date.strftime(r'%Y-%m-%d')
        
    def __repr__(self, ):
        return f'<Fdate {self.__str__()}>'

    @property
    def Y_m_d(self, ):
        return str(self._date)

    @property
    def Ymd(self, ):
        return self._date.strftime(r'%Y%m%d')

    @property
    def date(self, ):
        return self._date
    