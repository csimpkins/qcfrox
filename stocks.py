import csv
import sys

class Company:
    def __init__(self, symbol, name=None, sector=None):
        self.symbol = symbol;
        self.name = name;
        self.sector = sector;
        self.stock_data = {};

    def __str__(self):
        # return name + "(" + symbol + ")"
        return "%s (%s)" % (self.name, self.symbol)

    def __repr__(self):
        return "<Company: name=%s, symbol=%s, sector=%s>" % (self.name,
                                                             self.symbol,
                                                             self.sector)
    def performance(self, start=None, end=None):
        start = self.find_start(start) if start else min(self.stock_data.keys())
        end = self.find_end(end) if end else max(self.stock_data.keys())
        start_price = self.stock_data[start].open_price
        end_price = self.stock_data[end].adj_close
        return (end_price - start_price) / start_price

    def find_start(self, date):
        for d in sorted(self.stock_data.keys()):
            if d >= date:
                return d

    def find_end(self, date):
        for d in sorted(self.stock_data.keys(), reverse=True):
            if d <= date:
                return d


class StockData:
    def __init__(self, stock_dict):
        # Date,Open,High,Low,Close,Adj Close,Volume
        self.open_price = float(stock_dict['Open'])
        self.high = float(stock_dict['High'])
        self.low = float(stock_dict['Low'])
        self.close = float(stock_dict['Close'])
        self.adj_close = float(stock_dict['Adj Close'])
        self.volume = int(stock_dict['Volume'])

if __name__=='__main__':
    symbol = sys.argv[1]
    start = sys.argv[2] if len(sys.argv) > 2 else None
    end = sys.argv[3] if len(sys.argv) > 3 else None
    comp = Company(symbol)

    csv_file = symbol + ".csv"
    with open(csv_file) as fin:
        for rec in csv.DictReader(fin):
            date = rec['Date']
            comp.stock_data[date] = StockData(rec)

    perf = comp.performance(start, end) * 100
    print(f"Stock performance of {comp} from {start} to {end}: {perf:.1f}%")
