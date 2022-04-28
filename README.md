# Sales-API

<br>

# Project Setup Instructions

1. Clone this repository:

```bash
    git clone https://github.com/prasadnitesh202/Sales-API-Pandas.git
```

2. Install virtualenv(Optional)

```bash
   pip install virtualenv
```

3. Activate the virtual environment(Optional)

```
  https://docs.python.org/3/tutorial/venv.html
```

4. Install the requirements from requirements.txt

```bash
    pip install -r requirements.txt
```

5. Run the application from project directory

```
    flask run
```

- ## It will start the application at port 5000

<br>

# API Endpoints

- GET /joinTables

```
    Joins Sales, Product Master, and Branch Master tables to get the accumulated result
```

- POST /addSales

```
    Adds records into Sales table
```

## Sample Request

```bash
    curl -X POST http://localhost:5000/addSales
   -H "Content-Type: application/json"
   -d '{
        "sales_id" : 305,
        "date" : "2021-11-01",
        "product_id" : 1,
        "branch_id": 100,
        "price":30000,
        "quantity": 14000
       }'

```

- GET /leadTime

```
    Adds a column ‘lead time’:  Lead time is the difference between the received date and the ordered date in days.

```

- GET /averageLeadTime

```
    Calculates lead time average for each Product ID-Branch ID-Supplier ID combination.

```

- GET /variance

```
    Calculates lead time variance for each Product ID-Branch ID-Supplier ID combination.
```
