import logging

logger = logging.getLogger('twitter-scraper')

file_handler = logging.FileHandler("logs/tweets.log")
logger.addHandler(file_handler)

formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

level = logging.INFO
logger.setLevel(level)
