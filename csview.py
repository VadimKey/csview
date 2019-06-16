import sys
from collections import namedtuple

def cmdlineArgs():
    import argparse
    parser = argparse.ArgumentParser(description="csview.py is a simple tool to work with csv files")
    parser.add_argument("csvfile", nargs="?", help="CSV file to view, if omited use stdin")
    parser.add_argument("-f", "--filters", nargs="*", help="show only header and lines matching to these regular expressions")
    parser.add_argument("-c", "--columns", nargs="*", help="show only given columns")
    parser.add_argument("-n", "--numerate", default=False, action="store_true", help="enumerate columns (useful when you have too many columns)")
    return parser.parse_args()

def getDataComment(line):
    dc = line.split('#', maxsplit=1)
    data = dc[0].strip() if dc else None
    if data == '':
        data = None
    comment = None if len(dc) == 1 else dc[1].rstrip()
    return data, comment

def parseFields(row, sep):
    if row:
        return [s.strip() for s in row.split(sep)]
    else:
        return []

def parseHeader(headerline):
    commas = headerline.count(',')
    pipes = headerline.count('|')
    if commas or pipes:
        sep = ',' if commas > pipes else '|'
        return parseFields(headerline, sep), sep
    raise RuntimeError("No header (not CSV?)")

def getColumnIndices(header, columns):
    if not columns:
        return list(range(0, len(header))) # use all columns
    return [header.index(c) for c in columns if c in header]

def makeReFilters(filters):
    import re
    return [re.compile(f) for f in filters]

CsvRow = namedtuple('CsvRow', ['data', 'comment'])

class CSV:
    def __init__(self, filters, columns, numerate):
        self.rowFilters = makeReFilters(filters) if filters else []
        self.showColumns = columns
        self.cols = None
        self.widths = []
        self.rows = [] # CsvRow
        self.sep = None
        self.numerate = numerate

    def setHeader(self, header, comment):
        hdr, self.sep = parseHeader(header)
        self.cols = getColumnIndices(hdr, self.showColumns)
        self.widths = [0 for _ in self.cols]
        self.add(hdr, comment, header = True)

    def addComment(self, comment):
        self.rows.append(CsvRow(data=None, comment=comment))

    def filterColumns(self, row):
        maxRow = len(row)
        data = [row[i] if i < maxRow else '' for i in self.cols]
        return data if any(data) else []

    def add(self, row, comment, header = False):
        fields = self.filterColumns(row)
        if row and not fields:
            return # all filtered out
        if self.filterFields(fields) or header:
            row = CsvRow(data=self.filterColumns(row), comment=comment)
            self.updateWidths(row.data)
            self.rows.append(row)
        else:
            self.discardComments()

    def filterFields(self, fields):
        if not self.rowFilters or not fields:
            return True
        for regexp in self.rowFilters:
            for field in fields:
                if regexp.search(field):
                    return True
        return False

    def discardComments(self):
        for nrow in reversed(list(enumerate(self.rows))):
            if not nrow[1].data:
                del self.rows[nrow[0]]
            else:
                return

    def addLine(self, line):
        data, comment = getDataComment(line)
        fields = parseFields(data, self.sep)
        self.add(fields, comment)

    def updateWidths(self, data):
        for index, value in enumerate(data):
            self.widths[index] = max(self.widths[index], len(value))

    def renderData(self, rowdata):
        if not self.numerate:
            return ' | '.join(v.ljust(self.widths[i]) for i, v in enumerate(rowdata))
        else:
            return ' | '.join("{}:{}".format(i, v.ljust(self.widths[i])) for i, v in enumerate(rowdata))

    def display(self):
        for row in self.rows:
            s = self.renderData(row.data) if row.data else ''
            if row.comment:
                s += " #" if s else "#"
                s += row.comment
            print(s)

def display(csvfile, filters, columns, numerate):
    csv = CSV(filters, columns, numerate)
    # we don't use standard csv module as we need more flexibility
    for line in csvfile:
        header, comment = getDataComment(line)
        if header:
            break
        csv.addComment(comment)

    if not header:
        raise RuntimeError("CSV doesn't have header")
    csv.setHeader(header, comment)
    for line in csvfile:
        csv.addLine(line)
    csv.display()

def main():
    cmd = cmdlineArgs()
    if cmd.csvfile:
        with open(cmd.csvfile) as f:
            display(f, cmd.filters, cmd.columns, cmd.numerate)
    else:
        display(sys.stdin, cmd.filters, cmd.columns, cmd.numerate)
    return 0

if __name__ == "__main__":
    exit( main() )
