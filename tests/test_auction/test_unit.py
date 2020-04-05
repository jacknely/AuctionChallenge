from unittest import TestCase
from app.auction import Auction


class AuctionTest(TestCase):
    def setUp(self):
        bids = [("20", "8", "BID", "toaster_1", "7.50")]
        listings = [("10", "1", "SELL", "toaster_1", "4.00", "20")]
        self.auction = Auction(bids, listings)

    def test_init_(self):
        bids = [("20", "8", "BID", "toaster_1", "7.50")]
        listings = [("10", "1", "SELL", "toaster_1", "4.00", "20")]
        expected_bids = [
            self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        ]
        expected_listings = [
            self.auction.Listing("10", "1", "SELL", "toaster_1", "4.00", "20")
        ]
        auction = Auction(bids, listings)

        self.assertEqual(auction.bids, expected_bids)
        self.assertEqual(auction.listings, expected_listings)

    def test_is_listed_item(self):
        bid = self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        sell = self.auction.Listing(
            "10", "1", "SELL", "toaster_1", "4.00", "20"
        )
        validate_item = self.auction.is_listed_item(bid, sell)

        self.assertEqual(validate_item, True)

    def test_is_valid_price(self):
        bid = self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        sell = self.auction.Listing(
            "10", "1", "SELL", "toaster_1", "4.00", "20"
        )
        validate_item = self.auction.is_valid_price(bid, sell)

        self.assertEqual(validate_item, True)

    def test_is_valid_time(self):
        bid = self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        sell = self.auction.Listing(
            "10", "1", "SELL", "toaster_1", "4.00", "20"
        )
        validate_item = self.auction.is_valid_time(bid, sell)

        self.assertEqual(validate_item, True)

    def test_evaluate_bid(self):
        bid_evaluation = self.auction.evaluate_bid(lambda x, y: x is x)

        self.assertEqual(bid_evaluation, self.auction.bids)

    def test_get_valid_bids(self):
        test_valid_bids = self.auction.get_valid_bids
        expected_valid_bids = [
            self.auction.Bid("20", "8", "BID", "toaster_1", "7.50")
        ]

        self.assertEqual(test_valid_bids, expected_valid_bids)

    def test_get_accepted_bids(self):
        self.auction.bids = [
            self.auction.Bid("20", "8", "BID", "toaster_1", "1.50")
        ]
        test_accepted_bids = self.auction.get_accepted_bids
        expected_valid_bids = []

        self.assertEqual(test_accepted_bids, expected_valid_bids)

    def test_sort_bids_by(self):
        bids = [
            self.auction.Bid("20", "8", "BID", "toaster_1", "12.50"),
            self.auction.Bid("20", "8", "BID", "toaster_1", "16.50"),
        ]
        test_sort = self.auction.sort_bids_by(bids, "bid_amount")
        expected_sorted = [
            self.auction.Bid("20", "8", "BID", "toaster_1", "16.50"),
            self.auction.Bid("20", "8", "BID", "toaster_1", "12.50"),
        ]

        self.assertEqual(test_sort, expected_sorted)

    def test_finish_auction(self):
        sold = self.auction.finish_auction()
        expected_sold = [
            self.auction.Sold(
                "20", "toaster_1", "8", "SOLD", "7.50", 1, "7.50", "7.50"
            )
        ]

        self.assertEqual(sold, expected_sold)

        self.auction.bids = [
            self.auction.Bid("20", "8", "BID", "toaster_1", "1.50")
        ]
        sold = self.auction.finish_auction()
        expected_unsold = [
            self.auction.Sold(
                "20", "toaster_1", "", "UNSOLD", 0.0, 1, "1.50", "1.50"
            )
        ]

        self.assertEqual(sold, expected_unsold)
