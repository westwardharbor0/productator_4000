### `GET: /product/<pid>`
```
- Loads product from DB and returns it
- example:
    request:  GET: /product/1
    response:
        {
          "code": 200,
          "message": "",
          "result": {
            "description": "<product_description>",
            "id": <pid>,
            "name": "<product_name>"
          }
        }
```

### `GET: /products`
```
- Loads all products from DB and returns it
- example:
    request:  GET: /products
    response:
        {
          "code": 200,
          "message": "",
          "result": [
            {
              "description": "<product_description>",
              "id": <pid>,
              "name":  "<product_name>"
            },
            {
              "description": "<product_description>",
              "id": <pid>,
              "name":  "<product_name>"
            }
          ]
        }
```

### `PUT: /product`
```
- Creates product in DB and in a external API to create offers
- example:
    request:  PUT: /product
    body: 
        {
            "name": "<product_name>",
            "description": "<product_description>"
        }
    response:
        {
          "code": 200,
          "message": "Product was created",
          "result": {}
        }
```

### `POST: /product/<pid>`
```
- Updates properties of product
- example:
    request:  POST: /product/1
    body: 
        {
            "name": "<product_name>",
            "description": "<product_description>"
        }
    response:
        {
          "code": 200,
          "message": "Product was updated",
          "result": {}
        }
```

### `DELETE: /product/<pid>`
```
- Removes a product
- example:
    request:  DELETE: /product/1
    response:
        {
          "code": 200,
      "message": "Product was removed",
          "result": {}
        }
```

### `GET: /offers/<pid>`
```
- Loads offers (updated every minute by refresher) for a product
- example:
    request:  GET: /offers/1
    response:
        {
          "code": 200,
          "message": "",
          "result": [
            {
              "id": <offer_id>,
              "items_in_stock": <int>,
              "price": <int>,
              "product_id": <pid>
            },
            {
              "id": <offer_id>,
              "items_in_stock": <int>,
              "price": <int>,
              "product_id": <pid>
            }
            ...
          ]
        }
```

