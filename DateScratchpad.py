import time
import json
from datetime import date, timedelta, datetime, tzinfo

def main():
    strJavaDate="2016-06-09T23:42:12Z"

    print("This is a Java date string: " + strJavaDate)

    datePythonDate=datetime.strptime(strJavaDate, "%y-%m-%d %H:%M:%SZ")

    print datePythonDate


main()