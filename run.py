from app.auction import Auction

auction = Auction()
auction.parse_file("./input.txt")
sold_items = auction.finish_auction()
auction.save_to_file("./output.txt")
