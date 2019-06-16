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
