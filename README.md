![Python application](https://github.com/jacknely/AuctionChallenge/workflows/Python%20application/badge.svg)
# Auction Challenge
Given an input file containing instructions to both start 
auctions and place bids, the application executes all instructions. 
On completion, an output is created which contains the 
end of auction statistics.

## Usage
Ensure path to 'input.txt' file is set in run.py. The file should 
contain bids and item_listings in the following formats:


### Bids
This will appear in the format:

timestamp|user_id|action|item|bid_amount

`timestamp` will be an integer representing a unix
 epoch time and is the time of the bid,
`user_id` is an integer user id
`action` will be the string "BID"
`item` is a unique string code for that item.
`bid_amount` is a decimal representing a bid in the 
auction site's local currency.

### Item Listings (Sells)
This appears in the format:

timestamp|user_id|action|item|reserve_price|close_time

- `timestamp` will be an integer representing a unix 
epoch time and is the auction start time,
- `user_id` is an integer user id
- `action` will be the string "SELL"
- `item` is a unique string code for that item.
- `reserve_price` is a decimal representing the 
item reserve price in the site's local currency.
- `close_time` will be an integer representing 
a unix epoch time

## Output
On successfully execution of an 'output.txt' will be created in the
following format

### Sold
close_time|item|user_id|status|price_paid|total_bid_count|highest_bid|lowest_bid

- `close_time` should be a unix epoch of the time the auction finished
- `item` is the unique string item code.
- `user_id` is the integer id of the winning user, or blank if the item did not sell.
- `status` should contain either "SOLD" or "UNSOLD" depending on the auction outcome.
- `price_paid` should be the price paid by the auction winner (0.00 if the item is UNSOLD), as a
number to two decimal places
- `total_bid_count` should be the number of bids received for the item.
- `highest_bid` the highest bid received for the item as a number to two decimal places
- `lowest_bid` the lowest bid placed on the item as a number to two decimal places
