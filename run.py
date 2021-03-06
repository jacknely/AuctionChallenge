from app.auction import Auction
from app.file import File

file = File()
bids, sells = file.parse("./input.txt")
auction = Auction(bids, sells)
sold_items = auction.get_sold_items()
file.save(sold_items, "./output.txt")
