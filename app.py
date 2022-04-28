import sqlite3
import pandas as pd
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
    df = pd.read_sql_query("""SELECT
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
""", conn)
    print(df.head())
    conn.close()
    temp = {}
    res = []
    for index, row in df.iterrows():
        temp["date"] = row['date']
        temp["product_id"] = row['product_id']
        temp["branch_id"] = row['branch_id']
        temp["price"] = row['price']
        temp["quantity"] = row['quantity']
        temp["product_name"] = row['product_name']
        temp["category"] = row['category']
        temp["branch_name"] = row['branch_name']
        temp["branch_city"] = row['branch_city']
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
        return jsonify({"error": "Operations Falied"})


@app.route("/leadTime")
def calcLeadTime():
    conn = db_connection()
    df = pd.read_sql_query("""Select * from PurchaseOrders""", conn)
    df[['ReceivedDate', 'OrderedDate']] = df[[
        'ReceivedDate', 'OrderedDate']].apply(pd.to_datetime)
    df['leadTime'] = (df['ReceivedDate'] - df['OrderedDate']).dt.days
    print(df)
    df['ReceivedDate'] = (df['ReceivedDate']
                          .astype(str)  # <- cast to string to simplify
                          #    .replace() in newer versions
                          .replace({'NaT': None}  # <- replace with None
                                   ))
    df['leadTime'] = (df['leadTime']
                      .astype(str)  # <- cast to string to simplify
                      #    .replace() in newer versions
                      .replace({'NaT': None}  # <- replace with None
                               ))
    df['ReceivedQuantity'] = (df['ReceivedQuantity']
                              .astype(str)  # <- cast to string to simplify
                              #    .replace() in newer versions
                              .replace({'NaN': None}  # <- replace with None
                                       ))
    conn.close()
    temp = {}
    res = []
    for index, row in df.iterrows():
        temp["purchaseOrderId"] = row['PurchaseOrderId']
        temp["date"] = row['date']
        temp["product_id"] = row['product_id']
        temp["branch_id"] = row['branch_id']
        temp["supplier_id"] = row['supplier_id']
        temp["OrderedQuantity"] = row['OrderedQuantity']
        temp["ReceivedQuantity"] = row['ReceivedQuantity']
        temp["OrderedDate"] = row['OrderedDate']
        temp["ReceivedDate"] = row['ReceivedDate']
        temp["leadTime"] = row['leadTime']
        res.append(temp)
        temp = {}
    print(res)

    return jsonify(res)


@app.route("/averageLeadTime")
def calcAverageLeadTime():
    conn = db_connection()
    df = pd.read_sql_query("""Select * from PurchaseOrders""", conn)
    df[['ReceivedDate', 'OrderedDate']] = df[[
        'ReceivedDate', 'OrderedDate']].apply(pd.to_datetime)
    df['leadTime'] = (df['ReceivedDate'] - df['OrderedDate']).dt.days
    grouped_multiple = df.groupby(['product_id', 'branch_id', 'supplier_id']).agg(
        {'leadTime': ['mean']})
    grouped_multiple.columns = ['averageLeadTime']
    grouped_multiple = grouped_multiple.reset_index()
    print(grouped_multiple)
    df = grouped_multiple
    print(df)
    conn.close()
    temp = {}
    res = []
    for index, row in df.iterrows():
        temp["product_id"] = row['product_id']
        temp["branch_id"] = row['branch_id']
        temp["supplier_id"] = row['supplier_id']
        temp["averageLeadTime"] = row['averageLeadTime']
        res.append(temp)
        temp = {}
    # print(res)

    return jsonify(res)


@app.route("/variance")
def calcVariance():
    conn = db_connection()
    df = pd.read_sql_query("""Select * from PurchaseOrders""", conn)
    df[['ReceivedDate', 'OrderedDate']] = df[[
        'ReceivedDate', 'OrderedDate']].apply(pd.to_datetime)
    df['leadTime'] = (df['ReceivedDate'] - df['OrderedDate']).dt.days
    grouped_multiple = df.groupby(['product_id', 'branch_id', 'supplier_id']).agg(
        {'leadTime': ['var']})
    grouped_multiple.columns = ['leadTimeVariance']
    grouped_multiple = grouped_multiple.reset_index()
    print(grouped_multiple)
    df = grouped_multiple
    print(df)
    conn.close()
    temp = {}
    res = []
    for index, row in df.iterrows():
        temp["product_id"] = row['product_id']
        temp["branch_id"] = row['branch_id']
        temp["supplier_id"] = row['supplier_id']
        temp["leadTimeVariance"] = row['leadTimeVariance']
        res.append(temp)
        temp = {}
    print(res)

    return jsonify(res)
