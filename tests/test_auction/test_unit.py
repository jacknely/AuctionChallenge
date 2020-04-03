from unittest import TestCase
from app.auction import Auction


class AuctionTest(TestCase):
    def setUp(self):
        bids = [("20", "8", "BID", "toaster_1", "7.50")]
        sells = [("10", "1", "SELL", "toaster_1", "4.00", "20")]
        self.auction = Auction(bids, sells)

    def test_is_sell_item(self):
        bid = self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        sell = self.auction.Listing("10", "1", "SELL", "toaster_1", "10.00", "20")
        validate_item = self.auction.is_sell_item(bid, sell)

        self.assertEqual(validate_item, True)

    def test_is_valid_price(self):
        bid = self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        sell = self.auction.Listing("10", "1", "SELL", "toaster_1", "4.00", "20")
        validate_item = self.auction.is_valid_price(bid, sell)

        self.assertEqual(validate_item, True)

    def test_is_valid_time(self):
        bid = self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        sell = self.auction.Listing("10", "1", "SELL", "toaster_1", "4.00", "20")
        validate_item = self.auction.is_valid_time(bid, sell)

        self.assertEqual(validate_item, True)

    def test_evaluate_bid(self):
        condition = lambda x, y: x is x
        print(condition)
        bid_evaluation = self.auction.evaluate_bid(condition)

        self.assertEqual(bid_evaluation, self.auction.bids)
