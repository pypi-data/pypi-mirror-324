#!/usr/bin/env python

def from_date(date, format="%Y-%m-%d"):
    return date.strftime(format)


def to_date(date_string,format="%Y-%m-%d" ):
    import datetime
    return datetime.datetime.strptime(date_string, format)

