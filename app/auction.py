import csv
from collections import namedtuple
from operator import attrgetter


class Auction:
    Sell = namedtuple("Sell",
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

    def __init__(self):
        self.sells = []
        self.bids = []
        self.sold = []

    def parse_file(self, file: str) -> None:
        """
        takes a file path and imports contents into
        Bid and Sell namedTuples
        :param file: path to pipeline delimited file
        :return: list of bids and list of sold items
        """
        with open(file, encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="|"):
                if len(row) == 6:
                    action = self.Sell(
                        int(row[0]),
                        int(row[1]),
                        row[2],
                        row[3],
                        float(row[4]),
                        int(row[5]),
                    )
                    self.sells.append(action)
                elif len(row) == 5:
                    action = self.Bid(
                        int(row[0]), int(row[1]), row[2], row[3], float(row[4])
                    )
                    self.bids.append(action)

    @property
    def get_bids_without_invalid(self) -> list:
        """
        return a bid list with bids made after
        auction closed removed
        :return: bid list without invalid bids
        """
        return self.bid_evaluation(self.validate_item, self.validate_time)

    @property
    def get_accepted_bids(self) -> list:
        """
        return a bid list with success bids that were above
        reserve price and before closing time
        :return:  bid list of accepted bids
        """
        return self.bid_evaluation(
            self.validate_item, self.validate_price, self.validate_time
        )

    def sort_bids_by(self, attribute: str) -> list:
        """
        returns a sorted self.bids by a given attribute
        :param attribute: a bid attribute (e.g bid_amount)
        :return: a sorted bid list by attribute
        """
        return sorted(self.bids, key=attrgetter(attribute), reverse=True)

    @staticmethod
    def validate_item(bid: namedtuple, sell: namedtuple) -> bool:
        """
        returns the boolean if bid equals sell item
        :param bid: namedtuple of type bid
        :param sell: namedtuple of type
        :return: boolean
        """
        return bid.item == sell.item

    @staticmethod
    def validate_price(bid: namedtuple, sell: namedtuple) -> bool:
        """
        returns the boolean if bid amount is greater than or
        equal to the sell reserve price
        :param bid: namedtuple of type bid
        :param sell: namedtuple of type
        :return: boolean
        """
        return float(bid.bid_amount) >= float(sell.reserve_price)

    @staticmethod
    def validate_time(bid: namedtuple, sell: namedtuple) -> bool:
        """
        returns the boolean if bid timestamp is greater than or
        equal to the sell close time
        :param bid: namedtuple of type bid
        :param sell: namedtuple of type
        :return: boolean
        """
        return int(bid.timestamp) <= int(sell.close_time)

    def bid_evaluation(self, *conditions) -> list:
        """
        filters self.bids based on conditions passed
        :param conditions: funcs returning bool
        :return: list of filtered bids
        """
        accepted_bids = []
        for sell in self.sells:
            for bid in self.bids:
                if all(condition(bid, sell) for condition in conditions):
                    accepted_bids.append(bid)
        return accepted_bids

    @staticmethod
    def get_max_bid(bid_list: list, sell: namedtuple) -> namedtuple:
        """
        takes a bid list and a sell item then return the
        max bid for given item
        :param bid_list: list of bid namedtuple
        :param sell: namedtuple with sell item
        :return: namedtuple of max bid
        """
        return max(
            [bid for bid in bid_list if bid.item == sell.item],
            key=attrgetter("bid_amount"),
        )

    def get_min_and_max_bids(self, sell: namedtuple) -> tuple:
        """
        returns the maximum and minimum bids for an item
        :param sell: item to return data for
        :return: tuple of max & min bids
        """
        bids_sorted_by_amount = self.sort_bids_by("bid_amount")
        max_bid = max([bid for bid in bids_sorted_by_amount if bid.item == sell.item]).bid_amount
        min_bid = min([bid for bid in bids_sorted_by_amount if bid.item == sell.item]).bid_amount
        return max_bid, min_bid

    def save_to_file(self, file: str) -> None:
        """
        writes sold namedtuple to given file
        :param file: path to file
        """
        with open(file, 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f, delimiter="|")
            for sold in self.sold:
                writer.writerow(sold)

    def finish_auction(self):
        """
        processes and stores sold data
        :return: namedtuple of sold items
        """
        accepted_bids = self.get_accepted_bids
        bids_without_invalid = self.get_bids_without_invalid

        for sell in self.sells:
            if any(bid.item == sell.item for bid in accepted_bids):
                bid_win = self.get_max_bid(accepted_bids, sell)
                user_id = bid_win.user_id
                status = "SOLD"
                price_paid = [bid for bid in self.bids if bid.item == sell.item][1].bid_amount
                price_paid = f"{price_paid:.2f}"
                highest_bid, lowest_bid = self.get_min_and_max_bids(sell)
                total_bid_count = len([bid for bid in self.bids if bid.item == sell.item])

            else:
                bid_win = self.get_max_bid(bids_without_invalid, sell)
                user_id = ""
                status = "UNSOLD"
                price_paid = 0
                highest_bid, lowest_bid = self.get_min_and_max_bids(sell)
                highest_bid = bid_win.bid_amount
                total_bid_count = len([bid for bid in bids_without_invalid if bid.item == sell.item])

            closing_time = sell.close_time
            item = sell.item

            self.sold.append(
                self.Sold(
                    closing_time,
                    item,
                    user_id,
                    status,
                    price_paid,
                    total_bid_count,
                    f"{highest_bid:.2f}",
                    f"{lowest_bid:.2f}",
                )
            )
        return self.sold
