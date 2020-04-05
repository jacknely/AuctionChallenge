import csv
from decimal import Decimal


class File:
    @staticmethod
    def parse(file: str) -> tuple:
        """
        takes a file path and imports contents into
        tuple of bids and a tuple of sells
        :param file: path to pipeline delimited file
        :return: list of bids and list of sold items
        """
        sells = []
        bids = []
        with open(file, encoding="utf-8") as f:
            for row in csv.reader(f, delimiter="|"):
                if len(row) == 6:
                    action = (
                        int(row[0]),
                        int(row[1]),
                        row[2],
                        row[3],
                        Decimal(row[4]),
                        int(row[5]),
                    )
                    sells.append(action)
                elif len(row) == 5:
                    action = (
                        int(row[0]),
                        int(row[1]),
                        row[2],
                        row[3],
                        Decimal(row[4]),
                    )
                    bids.append(action)

        return bids, sells

    @staticmethod
    def save(sold: list, file: str) -> None:
        """
        writes sold namedtuple to given file
        :param file: filename and location to save file
        :param sold: list of sold items in tuple
        """
        with open(file, "w", newline="", encoding="utf8") as f:
            writer = csv.writer(f, delimiter="|")
            for sold in sold:
                writer.writerow(sold)
