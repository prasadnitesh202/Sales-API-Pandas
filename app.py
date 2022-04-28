import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("fountain9.db")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/")
def home():
    return jsonify("FOUNTAIN9 ASSIGNMENT - NITESH PRASAD")


@app.route("/joinTables")
def join():
    conn = db_connection()
    cursor = conn.execute("""SELECT
date,
s.product_id,
s.branch_id,
price,
quantity,
product_name,
category,
branch_name,
branch_city
FROM
Sales AS s
JOIN
PRODUCTMASTER AS p
ON
s.product_id = p.product_id
JOIN BRANCHMASTER AS b
ON
s.branch_id = b.branch_id
""")
    result = cursor.fetchall()
    conn.close()
    temp = {}
    res = []
    for row in result:
        temp["date"] = row[0]
        temp["product_id"] = row[1]
        temp["branch_id"] = row[2]
        temp["price"] = row[3]
        temp["quantity"] = row[4]
        temp["product_name"] = row[5]
        temp["category"] = row[6]
        temp["branch_name"] = row[7]
        temp["branch_city"] = row[8]
        res.append(temp)
        temp = {}
    print(res)

    return jsonify(res)


@app.route("/addSales", methods=['POST'])
def addSalesData():
    try:
        data = request.json
        sales_id = data["sales_id"]
        date = data["date"]
        product_id = data["product_id"]
        branch_id = data["branch_id"]
        price = data["price"]
        quantity = data["quantity"]
        conn = db_connection()
        sql = """INSERT INTO Sales(sales_id,date,product_id,branch_id,price,quantity) VALUES (?,?,?,?,?,?)"""
        cursor = conn.execute(
            sql, (sales_id, date, product_id, branch_id, price, quantity))
        conn.commit()
        conn.close()
        return jsonify("Rows Added")
    except:
        return jsonify({"error":"Operations Falied"})


@app.route("/leadTime")
def calcLeadTime():
    conn = db_connection()
    cursor = conn.execute("""Select *,Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer) AS leadTime
from
PurchaseOrders""")
    result = cursor.fetchall()
    conn.close()
    temp = {}
    res = []
    for row in result:
        temp["purchaseOrderId"] = row[0]
        temp["date"] = row[1]
        temp["product_id"] = row[2]
        temp["branch_id"] = row[3]
        temp["supplier_id"] = row[4]
        temp["OrderedQuantity"] = row[5]
        temp["ReceivedQuantity"] = row[6]
        temp["OrderedDate"] = row[7]
        temp["ReceivedDate"] = row[8]
        temp["leadTime"] = row[9]
        res.append(temp)
        temp = {}
    print(res)

    return jsonify(res)


@app.route("/averageLeadTime")
def calcAverageLeadTime():
    conn = db_connection()
    cursor = conn.execute("""Select *,Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer) AS leadTime, AVG(Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer))
from
PurchaseOrders
Group By product_id,branch_id,supplier_id""")
    result = cursor.fetchall()
    conn.close()
    temp = {}
    res = []
    for row in result:
        temp["purchaseOrderId"] = row[0]
        temp["date"] = row[1]
        temp["product_id"] = row[2]
        temp["branch_id"] = row[3]
        temp["supplier_id"] = row[4]
        temp["OrderedQuantity"] = row[5]
        temp["ReceivedQuantity"] = row[6]
        temp["OrderedDate"] = row[7]
        temp["ReceivedDate"] = row[8]
        temp["leadTime"] = row[9]
        temp["averageLeadTime"] = row[10]
        res.append(temp)
        temp = {}
    print(res)

    return jsonify(res)
    
@app.route("/variance")
def calcVariance():
    conn = db_connection()
    cursor = conn.execute("""Select *,Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer) AS leadTime,SUM((Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer)-(SELECT AVG(Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer)) FROM PurchaseOrders))*
           (Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer)-(SELECT AVG(Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer)) FROM PurchaseOrders)) ) / (COUNT(Cast ((
    JulianDay(ReceivedDate) - JulianDay(OrderedDate)
) As Integer))-1) AS Variance
from
PurchaseOrders
Group By product_id,branch_id,supplier_id""")
    result = cursor.fetchall()
    conn.close()
    temp = {}
    res = []
    for row in result:
        temp["purchaseOrderId"] = row[0]
        temp["date"] = row[1]
        temp["product_id"] = row[2]
        temp["branch_id"] = row[3]
        temp["supplier_id"] = row[4]
        temp["OrderedQuantity"] = row[5]
        temp["ReceivedQuantity"] = row[6]
        temp["OrderedDate"] = row[7]
        temp["ReceivedDate"] = row[8]
        temp["leadTime"] = row[9]
        temp["variance"] = row[10]
        res.append(temp)
        temp = {}
    print(res)

    return jsonify(res)
