
# Order Management System

## Installation

Install the dependencies and devDependencies and start the server.

```sh
pip install -r requirements.txt
or 
pip3 install -r requirements.txt
```

Apply the migrations 
```sh
python manage.py migrate
or 
python3 manage.py migrate
```

Create super user to access admin pannel
```sh
python manage.py createsuperuser
or 
python3 manage.py createsuperuser
```

To run server follow below command
```sh
python manage.py runserver
or 
python3 manage.py runserver
```
After triggering the above command you will see 
```sh
Starting development server at http://127.0.0.1:8000/
```
To Test the unit test fire the below command 
```sh
python manage.py test
or 
python3 manage.py test
```

## API Reference

Create user api with the default type consume

```sh
curl --location --request POST 'http://127.0.0.1:8000/api/v1/create_consumer/' \
--form 'username="test12"' \
--form 'password="test@123"' \
--form 'email="testl@gmail.com"'
```

Create Order api with multiple product

To create the product pass product_id as key and quantity as a value in product dictionary.
```sh
curl --location --request POST 'http://127.0.0.1:8000/api/v1/order/' \
--header 'Authorization: Token ad7707a6eb1c2b5d44194a3daafd91ce5bf82f62' \
--header 'Content-Type: application/json' \
--data-raw '{
   "product":{
       "1":3,
       "2":4
   }
}'
```

API to fetch all the order of the user 
 
```sh
curl --location --request GET 'http://127.0.0.1:8000/api/v1/myorder/' \
--header 'Authorization: Token ad7707a6eb1c2b5d44194a3daafd91ce5bf82f62' \
--data-raw ''
```




