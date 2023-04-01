from flightprice.logger import logging
from flightprice.exception import FlightPriceException
import sys

def test_logger_and_exception():
    try:
        logging.info("Starting point the test_logger_and_exception")
        result = 3/0
        print(result)
        logging.info("Ending point the test_logger_and_exception")
    except Exception as e:
        logging.debug(str(e))
        raise FlightPriceException(e, sys)

if __name__ == "__main__":
    try:
        test_logger_and_exception()
    except Exception as e:
        print(e)
  