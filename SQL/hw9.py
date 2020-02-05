'''
HW09: Basic SQL statements
'''

import sqlite3 as sqlite
conn = sqlite.connect('Northwind_small.sqlite')
cur = conn.cursor()
#QUESTIONS TO ASK TOMORROW:
#ASK ABOUT #10: See if this is the correct answer


#----- Q1. Show all rows from the Region table
def get_regions():
    statement = 'SELECT * '
    statement += 'FROM Region '
    cur.execute(statement)
    for regions in cur:
        print(str(regions[0]) + ' ' + regions[1])
print('QUESTION 1: ')
get_regions()
print('--'*20)

#----- Q2. How many customers are there?
def get_number_of_customers():
    statement = 'SELECT count(*) '
    #statement = 'SELECT Id '
    statement += 'From Customer '
    cur.execute(statement)
    for customer in cur:
        print(customer[0])
    #c = []
    #for customer in cur:
        #if customer not in c:
            #c.append(customer)
    #print(len(c))
print('QUESTION 2: ')
get_number_of_customers()
print('--'*20)

#----- Q3. How many orders have been made?
def get_number_of_orders():
    #statement = 'SELECT Id '
    statement = 'SELECT count(*) '
    statement += 'From [Order] '
    cur.execute(statement)
    for x in cur:
        print(x[0])
    #o= []
    # for order in cur:
    #     if order not in o:
    #         o.append(order)
    # print(len(o))
print('QUESTION 3: ')
get_number_of_orders()
print('--'*20)

#----- Q4. Show the first five rows from the Product table
def get_first_five():
    statement = 'SELECT * '
    statement += 'From Product '
    statement += 'WHERE Id BETWEEN 1 AND 5'
    cur.execute(statement)
    for x in cur:
        print(str(x[0]) + ' ' + str(x[1]) + ' ' + str(x[2]) + ' ' + str(x[3])+ ' ' + str(x[4]) + ' ' + str(x[5]) + ' ' + str(x[6])+ ' ' + str(x[7]) + ' ' + str(x[8]) + ' ' + str(x[9]))
print('QUESTION 4: ')
get_first_five()
print('--'*20)

#----- Q5. Show all available categories
def get_categories():
    statement = 'SELECT CategoryName '
    statement += 'FROM Category'
    cur.execute(statement)
    for x in cur:
        print(x[0])
print('QUESTION 5: ')
get_categories()
print('--'*20)

#----- Q6. Show the five cheapest products
def get_five_cheapest():
    statement = 'SELECT ProductName '
    statement += 'From Product '
    statement += 'ORDER BY UnitPrice ' #ascending -- lowest price to highest
    statement += 'LIMIT 5'
    answer = cur.execute(statement)
    for x in cur:
        print(x[0])
    # for x in range(5):
    #     print(answer[x][0])
    # statement = 'SELECT ProductName,UnitPrice '
    # statement += 'From Product '
    # cur.execute(statement)
    # L = []
    # for x in cur:
    #     L.append([x[0],x[1]])
    # new_l = [x[0] for x in sorted(L, key= lambda x: x[1])]
    # cheapest_five = new_l[:5]
    # for x in cheapest_five:
    #     print(str(x))
print('QUESTION 6: ')
get_five_cheapest()
print('--'*20)

#----- Q7. Show all products that have more than 100 units in stock
def get_more_than_100():
    statement = 'SELECT ProductName '
    statement += 'FROM Product '
    statement += 'WHERE UnitsInStock > 100'
    cur.execute(statement)
    for x in cur:
        print(x[0])
print('QUESTION 7: ')
get_more_than_100()
print('--'*20)


#----- Q8. Show all columns in the Order table
def get_show_all_columns_in_order():
    statement = 'SELECT * '
    statement += 'FROM [Order]'
    descriptions = cur.execute(statement).description
    #decriptions returns tuples and the first element of those tuples will be the column names , will give you an outline of the table
    for x in descriptions:
        print(str(x[0]))
print('QUESTION 8: ')
get_show_all_columns_in_order()
print('--'*20)
#----- Q9. Identify each employee's first name and the number of order each employee has made. Sort them by the total number of orders in decreasing order
def get_employee_name_and_number_ordered():
    #count will will return the number of orders matching your criteria
    #.fetchall(): returns all the result rows in python
    #group by: aggregating all of them; selecting from multiple things help you determine what you are going to order by in row response
    statement = 'SELECT Employee.FirstName, count(*) '
    statement += 'FROM [Order] '
    statement += 'JOIN Employee '
    statement += 'ON Employee.Id = [Order].EmployeeId '
    statement += 'GROUP BY Employee.ID '
    statement += 'ORDER BY count(*) DESC'
    employees = cur.execute(statement).fetchall()
    for x in employees:
        print(x[0] + ', ' + str(x[1]))
    # d = {}
    # for x in cur:
    #     name = str(x[0])
    #     if name not in d:
    #         d[name] = 1
    #     else:
    #         d[name] += 1
    # d_sorted = sorted(d, key= lambda x: d[x], reverse = True)
    # for x in d_sorted:
    #     print(x + ' ' + str(d[x]))
print('QUESTION 9: ')
get_employee_name_and_number_ordered()
print('--'*20)
#----- Q10. Identify the products and the corresponding supply companies in Ann Arbor
def get_products_and_supply_in_AA():
    statement = 'SELECT Product.ProductName,Supplier.CompanyName '
    statement += 'FROM Supplier '
    statement += 'JOIN Product '
    statement += 'ON Product.SupplierId = Supplier.Id '
    statement += 'WHERE Supplier.City = "Ann Arbor"'
    cur.execute(statement)
    for x in cur:
        print(x[0]+ ', ' + x[1])
print('QUESTION 10: ')
get_products_and_supply_in_AA()
print('--'*20)
