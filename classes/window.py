import datetime as dt



class TimeWindow:
    def __init__(self, date_start: dt.datetime, date_end: dt.datetime):
        if date_start > date_end:
            raise ValueError("date_start must be less than or equal to date_end")
        self._date_start = date_start
        self._date_end = date_end

    @property
    def date_start(self):
        return self._date_start
    
    @date_start.setter
    def date_start(self, value):
        if not isinstance(value, dt.datetime):
            raise TypeError("date_start must be a datetime object")
        if value > self._date_end:
            raise ValueError("date_start must be less than or equal to date_end")
        self._date_start = value

    @property
    def date_end(self):
        return self._date_end
    
    @date_end.setter
    def date_end(self, value):
        if not isinstance(value, dt.datetime):
            raise TypeError("date_end must be a datetime object")
        if value < self._date_start:
            raise ValueError("date_end must be greater than or equal to date_start")
        self._date_end = value

  

    def __str__(self):
        return f"TimeWindow({self.date_start}, {self.date_end})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, TimeWindow):
            return self.date_start == other.date_start and self.date_end == other.date_end

    def __ne__(self, other):
        return not (self == other)

    def __contains__(self, time):
        return self.date_start <= time <= self.date_end

    def __len__(self):
        return self.date_end - self.date_start

    