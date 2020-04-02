from collections import namedtuple
from operator import attrgetter


class Auction:
    Listing = namedtuple("Sell",
                      ["timestamp",
                       "user_id",
                       "action",
                       "item",
                       "reserve_price",
                       "close_time"]
                      )
    Bid = namedtuple("Bid",
                     ["timestamp",
                      "user_id",
                      "action",
                      "item",
                      "bid_amount"]
                     )
    Sold = namedtuple("Sold",
                      ["closing_time",
                       "item",
                       "user_id",
                       "status",
                       "price_paid",
                       "total_bid_count",
                       "highest_bid",
                       "lowest_bid"]
                      )

    def __init__(self, bids: list, sells: list) -> None:
        self.bids = [self.Bid(*bid) for bid in bids]
        self.listings = [self.Listing(*sell) for sell in sells]
        self.sold = []

    @property
    def get_valid_bids(self) -> list:
        """
        return a bid list with bids made after
        auction closed removed
        :return: bid list without invalid bids
        """
        return self.evaluate_bid(self.is_sell_item, self.is_valid_time)

    @property
    def get_accepted_bids(self) -> list:
        """
        return a bid list with success bids that were above
        reserve price and before closing time
        :return:  bid list of accepted bids
        """
        return self.evaluate_bid(
            self.is_sell_item, self.is_valid_price, self.is_valid_time
        )

    def sort_bids_by(self, attribute: str) -> list:
        """
        returns a sorted self.bids by a given attribute
        :param attribute: a bid attribute (e.g bid_amount)
        :return: a sorted bid list by attribute
        """
        return sorted(self.bids, key=attrgetter(attribute), reverse=True)

    @staticmethod
    def is_sell_item(bid: namedtuple, sell: namedtuple) -> bool:
        """
        returns the boolean if bid.item equals sell.item
        :param bid: namedtuple of type bid
        :param sell: namedtuple of type
        :return: boolean
        """
        return bid.item == sell.item

    @staticmethod
    def is_valid_price(bid: namedtuple, sell: namedtuple) -> bool:
        """
        returns the boolean if bid amount is greater than or
        equal to the sell reserve price
        :param bid: namedtuple of type bid
        :param sell: namedtuple of type
        :return: boolean
        """
        return float(bid.bid_amount) >= float(sell.reserve_price)

    @staticmethod
    def is_valid_time(bid: namedtuple, sell: namedtuple) -> bool:
        """
        returns the boolean if bid timestamp is greater than or
        equal to the sell close time
        :param bid: namedtuple of type bid
        :param sell: namedtuple of type
        :return: boolean
        """
        return int(bid.timestamp) <= int(sell.close_time)

    def evaluate_bid(self, *conditions) -> list:
        """
        filters self.bids based on conditions passed
        :param conditions: funcs returning bool
        :return: list of filtered bids
        """
        accepted_bids = []
        for sell in self.listings:
            for bid in self.bids:
                if all(condition(bid, sell) for condition in conditions):
                    accepted_bids.append(bid)
        return accepted_bids

    @staticmethod
    def get_tuple_with_highest_bid(bid_list: list,
                                   sell: namedtuple) -> namedtuple:
        """
        takes a bid list and a sell item then return the
        tuple of with max bid for given item
        :param bid_list: list of bid namedtuple
        :param sell: namedtuple with sell item
        :return: namedtuple of max bid
        """
        return max(
            [bid for bid in bid_list if bid.item == sell.item],
            key=attrgetter("bid_amount"),
        )

    def get_min_and_max_bid_value(self, sell: namedtuple) -> tuple:
        """
        returns the maximum and minimum bids for an item
        :param sell: item to return data for
        :return: tuple of max & min bids
        """
        bids_sorted_by_amount = self.sort_bids_by("bid_amount")
        max_bid = max([bid for bid in bids_sorted_by_amount
                       if bid.item == sell.item]).bid_amount
        min_bid = min([bid for bid in bids_sorted_by_amount
                       if bid.item == sell.item]).bid_amount
        return f"{max_bid:.2f}", f"{min_bid:.2f}"

    def get_price_paid(self, status: str, item: str) -> str:
        """
        takes a item and a status then returns a sell price
        :param status: Sold or Unsold as str
        :param item: item name as str
        :return: price paid as str
        """
        if status == "SOLD":
            price_paid = [bid for bid in self.bids
                          if bid.item == item][1].bid_amount
        else:
            price_paid = 0
        return f"{price_paid:.2f}"

    def finish_auction(self) -> list:
        """
        processes and stores sold data
        :return: namedtuple of sold items
        """
        accepted_bids = self.get_accepted_bids
        valid_bids = self.get_valid_bids

        for sell in self.listings:
            highest_bid, lowest_bid = self.get_min_and_max_bid_value(sell)
            if any(bid.item == sell.item for bid in accepted_bids):
                status = "SOLD"
                bid_win = self.get_tuple_with_highest_bid(accepted_bids, sell)
                user_id = bid_win.user_id
            else:
                status = "UNSOLD"
                bid_win = self.get_tuple_with_highest_bid(valid_bids, sell)
                highest_bid = f"{bid_win.bid_amount:.2f}"
                user_id = ""

            total_bid_count = len([bid for bid in valid_bids
                                   if bid.item == sell.item])
            price_paid = self.get_price_paid(status, sell.item)
            closing_time = sell.close_time
            item = sell.item

            sold = self.Sold(closing_time, item, user_id, status,
                             price_paid, total_bid_count,
                             highest_bid, lowest_bid)
            self.sold.append(sold)

        return self.sold
