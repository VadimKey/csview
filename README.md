# csview
# Simple CSV viewer

```
usage: csview.py [-h] [csvfile] [-f [FILTERS [FILTERS ...]]]
                 [-c [COLUMNS [COLUMNS ...]]] [-n]
                 

csview.py is a simple tool to work with csv files

positional arguments:
  csvfile               CSV file to view, if omited use stdin

optional arguments:
  -h, --help            show this help message and exit
  -f [FILTERS [FILTERS ...]], --filters [FILTERS [FILTERS ...]]
                        show only header and lines matching to these regular
                        expressions
  -c [COLUMNS [COLUMNS ...]], --columns [COLUMNS [COLUMNS ...]]
                        show only given columns
  -n, --numerate        enumerate columns (useful when you have too many
                        columns)
```

## Examples
```
 $ ./csview 1.csv -n
 $ ./csview 2.csv -f Ford -n
 $ cat 2.csv | ./csview -c Make Model Price -f Chevy
 $ ./csview 1c.csv -c Make Year Price -f 1.*6 Ford
 ```
 
 ## Tutorial
 
 Original csv file
 ```
 # from wikipedia
Year,Make,Model,Description,Price

1997,Ford,E350,ac; abs; moon,3000.00
# Chevrolet
# 123
1999,Chevy,Venture Extended Edition,,4900.00 # empty cell
1999,Chevy,Venture Extended Edition Very Large,,5000.00
1996,Jeep,Grand Cherokee,MUST SELL! air; moon roof; loaded,4799.00
```

result of command: `$ python3 ./csview.py 1c.csv`:
```
# from wikipedia
Year | Make  | Model                               | Description                       | Price

1997 | Ford  | E350                                | ac; abs; moon                     | 3000.00
# Chevrolet
# 123
1999 | Chevy | Venture Extended Edition            |                                   | 4900.00 # empty cell
1999 | Chevy | Venture Extended Edition Very Large |                                   | 5000.00
1996 | Jeep  | Grand Cherokee                      | MUST SELL! air; moon roof; loaded | 4799.00
```

Now let's show only column Make, Model, Price, Year (in this order)

$ python3 ./csview.py 1c.csv --columns Price Make Model Year

```
# from wikipedia
Price   | Make  | Model                               | Year

3000.00 | Ford  | E350                                | 1997
# Chevrolet
# 123
4900.00 | Chevy | Venture Extended Edition            | 1999 # empty cell
5000.00 | Chevy | Venture Extended Edition Very Large | 1999
4799.00 | Jeep  | Grand Cherokee                      | 1996
```

Notice that comments and the empty line are preserved. That's nice!

Now let's show only rows which contains years 1996 and 1997 or "Very Large":

$ python3 ./csview.py 1c.csv --columns Price Make Model Year --filter "199[6,7]" "Very Large"

```
# from wikipedia
Price   | Make  | Model                               | Year

3000.00 | Ford  | E350                                | 1997
5000.00 | Chevy | Venture Extended Edition Very Large | 1999
4799.00 | Jeep  | Grand Cherokee                      | 1996
```

Notice that comment disappeared because it was linked with the line "1999,Chevy,Venture Extended Edition,,4900.00 # empty cell".
