# AlgR
Script to simulate and translate relational algebra expressions to SQL queries.

# Requirements
Python 3

# Usage
> The script will run queries within the 'registros.db' database.
> Currently this database contains two tables, Produtos and Usuarios, used for testing purposes only.
 
 
Produtos:

| codigo | nome               | preco |
|--------|--------------------|-------|
| 1      | Royale with Cheese | 10.99 |
| 2      | Keyboard           | 8     |
| 3      | Life is Strange    | 36.99 |
 
Usuarios:

| Codigo | Nome | Idade  | Endereco | 
| ---- |:-------:| -----:|:-------------:|
| 1 | Joao | 21 | Rua dos Invalidos |
| 2 | Fernanda | 32 | Av Silva e Moura |
| 3 | Leticia | 19 | Rua Martin |

To start, run the script inside your operating system's terminal:  
```python main.py```

Run a selection operation using the 'SIG' keyword which is the representation for the lowercase sigma character (σ).  
e.g: To run a expression that shows whichever tuple has the 'idade' attribute greater than 10, we can do as following:  
```SIG idade > 10 (Usuarios)```

To execute a projection operation, use the 'PI' keyword which is the representation for the lowercase pi character (π).  
e.g: ```PI preco (Produtos) ``` will show all elements from 'preco' column inside the table 'Produtos'.

In case you want to use the selection's result as a projection argument, run the selection first, then run the projection adding the keyword 'SIG' between braces.  
e.g:
```
SIG idade > 10 (Usuarios)
PI nome (SIG)
```

And you can use cartesian product aswell simply adding '*' between the desired tables.
e.g: SIG Usuarios.idade > 10 AND Produtos.preco < 100 (Usuarios * Produtos)

# More commands
* __db_set__: Change the current database.
* __help__: Show an in-depth documentation.

# Future plans
* Support a wider range of dbms.
* JOIN operations.
* Redo the code.
* One line ```Projection (Selection)``` operations.
