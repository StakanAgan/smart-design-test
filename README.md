# smart-design-test
API writting by Flask using MongoDB

1. Create virtual environment directory ```virtualenv -p python3.8 venv```
2. Activate venv ```source venv/bin/activate```
1. Open Terminal, input ```pip3 install -r requirements.txt```<br>
2. Set environment variable:```export MONGO_URI={MONGO_URI}```<br>
    
2. Run application by command ```python3 run.py```

3. cURL list: <br>
- create product ```curl --location --request POST 'http://localhost:5000/api/product' \
--header 'Content-Type: application/json' --data-raw '{
    "title": "Tool Kit",
    "description": "Bigger than early",
    "params": {
        "price": "200",
        "class": "A"
    }
}'``` <br> <br>
``curl --location --request POST 'http://localhost:5000/api/product' --header 'Content-Type: application/json' --data-raw '{
   "title": "Dev kit",
    "description": "Your helper in garage",
    "params": {
        "price": 250,
        "class": "D"
    }
    }'`` <br> <br>
``curl --location --request POST 'http://localhost:5000/api/product' --header 'Content-Type: application/json' --data-raw '{
    "title": "Adjustable wrench",
    "description": "Best of",
    "params": {
        "price": 250,
        "class": "A"
    }
    }'``
- get product details by ID ```curl --location --request GET 'http://localhost:5000/api/product/:product_id'```

- get product by title and/or params with pagination<br>
without query ```curl --location --request GET 'http://localhost:5000/api/product/list'``` <br>by title - 
```curl --location --request GET 'http://localhost:5000/api/product/list?title=Tool%20Kit&per_page=2&page=0'``` <br>
by params - ```curl --location --request GET 'http://localhost:5000/api/product/list?per_page=2&page=0&price=200'``` <br>
by title and params ```curl --location --request GET 'http://localhost:5000/api/product/list?title=Tool%20Kit&per_page=2&page=0&price=200'```
