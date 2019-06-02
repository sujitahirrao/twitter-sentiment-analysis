from flask import Flask, request, jsonify

from ops import Tweeter
from config import Config
from ts_logger import logger

app = Flask(__name__)


@app.route('/twitter_analyser', methods=['GET'])
def get_tweets_with_sentiment():
    if request.method == 'GET':
        try:
            tw_handle = request.args.get('handle', '')
            if not tw_handle:
                raise ValueError("Please, pass the twitter handle.")
            count = int(request.args.get('count', Config.COUNT))

            print("Analysing tweets to:{}".format(tw_handle))

            twitter = Tweeter()
            tweets = twitter.get_tweets(tw_handle, count)
            response = {"tweets": tweets}

            return jsonify(response)
        except Exception as e:
            print("Exception in app: " + str(e))
            logger.error(str(e))
            return str(e)
    else:
        return "Please, GET the analysed tweets!"


if __name__ == '__main__':
    app.run()
