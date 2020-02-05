import sqlite3 as sqlite
import datetime
conn = sqlite.connect('Northwind_small.sqlite')
cur = conn.cursor()

def extra_credit():
    statement = 'SELECT CustomerId,OrderDate '
    statement += 'FROM [Order] '
    statement += 'ORDER BY CustomerId'
    row = cur.execute(statement)
    ids = []
    print('CustomerID, '+'Order Date, '+ 'Previous Order Date, '+'Days Passed')
    for x in row:
        if x[0] not in ids:
            ids.append(x[0])
            previous_date = x[1]

            list_ = previous_date.split('-')
            year = int(list_[0])
            month = int(list_[1])
            date = int(list_[2])
            continue
        else:
            order = x[1]
            order_date_list = order.split('-')
            year_order = int(order_date_list[0])
            month_order = int(order_date_list[1])
            date_order = int(order_date_list[2])

            new_order = datetime.date(year_order, month_order, date_order)
            old_order = datetime.date(year, month, date)
            subtract = new_order - old_order
            days_passed = subtract.days

            print(x[0]+',' + str(x[1])+"," + previous_date + ","+ str(days_passed))
            previous_date = x[1]
            list_= previous_date.split('-')
            year = int(list_[0])
            month = int(list_[1])
            date = int(list_[2])
extra_credit()
