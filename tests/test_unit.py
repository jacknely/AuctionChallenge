from unittest import TestCase
from unittest.mock import patch, mock_open
from app.auction import Auction
import pathlib


class AuctionTest(TestCase):

    def setUp(self):
        self.auction = Auction()
        current_dir = pathlib.Path(__file__).parent
        filename = pathlib.Path.joinpath(current_dir / "test_input.txt")
        self.auction.parse_file(filename)

    def test_validate_item(self):
        bid = self.auction.Bid('20', '8', 'BID', 'toaster_1', '7.50')
        sell = self.auction.Sell('10', '1', 'SELL', 'toaster_1', '10.00', '20')
        validate_item = self.auction.validate_item(bid, sell)

        self.assertEqual(validate_item, True)

    def test_validate_price(self):
        bid = self.auction.Bid('20', '8', 'BID', 'toaster_1', '7.50')
        sell = self.auction.Sell('10', '1', 'SELL', 'toaster_1', '4.00', '20')
        validate_item = self.auction.validate_price(bid, sell)

        self.assertEqual(validate_item, True)

    def test_validate_time(self):
        bid = self.auction.Bid('20', '8', 'BID', 'toaster_1', '7.50')
        sell = self.auction.Sell('10', '1', 'SELL', 'toaster_1', '4.00', '20')
        validate_item = self.auction.validate_time(bid, sell)

        self.assertEqual(validate_item, True)

    def test_bid_evaluation(self):
        self.auction.bids = [self.auction.Bid('20', '8', 'BID', 'toaster_1', '7.50')]
        self.auction.sells = [self.auction.Sell('10', '1', 'SELL', 'toaster_1', '4.00', '20')]
        condition = (lambda x, y: x is x)
        print(condition)
        bid_evaluation = self.auction.bid_evaluation(condition)

        self.assertEqual(bid_evaluation, self.auction.bids)


class FileTests(TestCase):

    def setUp(self):
        self.auction = Auction()

    @patch("builtins.open", new_callable=mock_open, read_data="10|1|SELL|toaster_1|10.00|20")
    def test_parse_file(self, mock_file):
        current_dir = pathlib.Path(__file__).parent
        filename = pathlib.Path.joinpath(current_dir / "test_input.txt")
        self.auction.parse_file(filename)

        self.assertEqual(3, len(self.auction.sells))
        mock_file.assert_called_with(filename, encoding='utf-8')

    def test_save_to_file(self):
        pass
