1. Create a table in the Database

```
CREATE TABLE table_name (
    field_name dataType "optionalFeatures like NOT NULL",
    field_name dataType,
    field_name dataType,
    "PRIMARY KEY (field_name)"
    "FOREIGN KEY (field_name) REFERENCES table_name(this.field_name)"
)
```

2. Insertion command(Pass data inside the brackets as we do in positional parameters)

```
INSERT INTO table_name VALUES ("value for field1", "value for field2", ....)
```

3. Selection from table where a condition matches

```
SELECT * FROM table_name WHERE condition
```

4. Adding new column in table

```
ALTER TABLE table_name ADD column_name datatype_of_that_column
```

5.  Updating any field inside a table

```
UPDATE table_name SET field_name=value WHERE condition
```

6. Deletion command

```
DELETE FROM table_name WHERE condition
```

7. Inner Join command

```
eg -:
SELECT orders.id, orders.order_number, customers.id, customers.name, customers.email
FROM orders
INNER JOIN customers on orders.customer_id = customers.id
```
