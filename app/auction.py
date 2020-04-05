from collections import namedtuple
from operator import attrgetter


class Auction:
    Listing = namedtuple(
        "Sell",
        [
            "timestamp",
            "user_id",
            "action",
            "item",
            "reserve_price",
            "close_time",
        ],
    )
    Bid = namedtuple(
        "Bid", ["timestamp", "user_id", "action", "item", "bid_amount"]
    )
    Sold = namedtuple(
        "Sold",
        [
            "closing_time",
            "item",
            "user_id",
            "status",
            "price_paid",
            "total_bid_count",
            "highest_bid",
            "lowest_bid",
        ],
    )

    def __init__(self, bids: list, sells: list) -> None:
        self.bids = [self.Bid(*bid) for bid in bids]
        self.listings = [self.Listing(*sell) for sell in sells]

    @property
    def get_valid_bids(self) -> list:
        """
        return a bid list with all valid bids. All bids
        made after listing closing time are removed
        :return: bid list without invalid bids
        """
        return self.evaluate_bid(self.is_listed_item, self.is_valid_time)

    @property
    def get_accepted_bids(self) -> list:
        """
        return a bid list with success bids that are above
        the listing reserve price and before closing time
        :return:  bid list of accepted bids
        """
        return self.evaluate_bid(
            self.is_listed_item, self.is_valid_price, self.is_valid_time
        )

    @staticmethod
    def sort_bids_by(bids: list, attribute: str) -> list:
        """
        returns a sorted list of bids by a given attribute
        :param attribute: a bid attribute (e.g bid_amount)
        :param bids: list of bids
        :return: a sorted bid list by attribute
        """
        return sorted(bids, key=attrgetter(attribute), reverse=True)

    @staticmethod
    def is_listed_item(bid: namedtuple, listing: namedtuple) -> bool:
        """
        returns the boolean if bid.item equals sell.item
        e.g. if there has been bids on a listed item
        :param bid: namedtuple of type bid
        :param listing: namedtuple of type
        :return: boolean
        """
        return bid.item == listing.item

    @staticmethod
    def is_valid_price(bid: namedtuple, listing: namedtuple) -> bool:
        """
        returns the boolean if bid amount is greater than or
        equal to the listing reserve price
        :param bid: namedtuple of type bid
        :param listing: namedtuple of type
        :return: boolean
        """
        return float(bid.bid_amount) >= float(listing.reserve_price)

    @staticmethod
    def is_valid_time(bid: namedtuple, listing: namedtuple) -> bool:
        """
        returns the boolean if bid timestamp is greater than or
        equal to the listing close time
        :param bid: namedtuple of type bid
        :param listing: namedtuple of type
        :return: boolean
        """
        return int(bid.timestamp) <= int(listing.close_time)

    def evaluate_bid(self, *conditions) -> list:
        """
        filters bids based on conditions passed
        :param conditions: funcs returning bool
        :return: list of filtered bids
        """
        accepted_bids = []
        for listing in self.listings:
            for bid in self.bids:
                if all(condition(bid, listing) for condition in conditions):
                    accepted_bids.append(bid)
        return accepted_bids

    @staticmethod
    def __get_winning_user(bids: list, listing: namedtuple, status) -> str:
        """
        returns the user.id of winning user if sold and "" is unsold
        :param bids: list of bid namedtuple
        :param listing: namedtuple with sell item
        :return: namedtuple of max bid
        """
        user = ""
        if status == "SOLD":
            bid = max(
                [bid for bid in bids if bid.item == listing.item],
                key=attrgetter("bid_amount"),
            )
            user = bid.user_id
        return user

    def __get_auction_attribute(
        self, operator: callable, bids: list, listing: namedtuple
    ) -> str:
        """
        returns the maximum and minimum bids for an item
        :param operator:
        :param listing: item to return data for
        :param bids: list of bids
        :return: tuple of max & min bids
        """
        bids_sorted = self.sort_bids_by(bids, "bid_amount")
        bid = operator(
            [bid for bid in bids_sorted if bid.item == listing.item]
        ).bid_amount
        return bid

    def __get_price_paid(self, status: str, item: str) -> str:
        """
        takes a item and a status then returns a sell price
        :param status: Sold or Unsold as str
        :param item: item name as str
        :return: price paid as str
        """
        price_paid = 0.00
        if status == "SOLD":
            bids_for_listing = [bid for bid in self.bids if bid.item == item]
            if len(bids_for_listing) > 1:
                price_paid = bids_for_listing[1].bid_amount
            else:
                price_paid = bids_for_listing[0].bid_amount

        return price_paid

    @staticmethod
    def __count_total_bids(bids: list, item: str) -> int:
        """
        returns a count of bids for a given item
        :param bids: list of bids
        :param item: item as str
        :return: int count of bids
        """
        item_bids = [bid for bid in bids if bid.item == item]
        bid_count = len(item_bids)
        return bid_count

    def finish_auction(self) -> list:
        """
        processes and stores sold data
        :return: namedtuple of sold items
        """
        listings = []
        for listing in self.listings:
            status = "UNSOLD"
            bids = self.get_valid_bids
            if any(bid.item == listing.item for bid in self.get_accepted_bids):
                status = "SOLD"
                bids = self.get_accepted_bids
            user_id = self.__get_winning_user(bids, listing, status)
            highest_bid = self.__get_auction_attribute(max, bids, listing)
            lowest_bid = self.__get_auction_attribute(min, bids, listing)
            total_bid_count = self.__count_total_bids(
                self.get_valid_bids, listing.item
            )
            price_paid = self.__get_price_paid(status, listing.item)

            listing = self.Sold(
                listing.close_time,
                listing.item,
                user_id,
                status,
                price_paid,
                total_bid_count,
                highest_bid,
                lowest_bid,
            )
            listings.append(listing)

        return listings
