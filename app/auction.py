import csv
import pathlib
from collections import namedtuple

Sell = namedtuple("Sell", ['timestamp', 'user_id', 'action', 'item', 'reserve_price', 'close_time'])
Bid = namedtuple("Bid", ['timestamp', 'user_id', 'action', 'item', 'bid_amount'])
Sold = namedtuple("Sold", ['closing_time', 'item', 'user_id', 'status', 'price_paid', 'total_bid_count', 'highest_bid', 'lowest_bid'])


def open_file(file):
    action_list = []
    with open(file) as f:
        for row in csv.reader(f, delimiter='|'):
            if len(row) == 6:
                action = Sell(*row)
            elif len(row) == 5:
                action = Bid(*row)
            action_list.append(action)
        print(action_list)



if __name__ == '__main__':
    open_file(pathlib.Path.cwd() / 'input.txt')
