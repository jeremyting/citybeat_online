from tweet_interface import TweetInterface



def main():
    ei = TweetInterface()

    now = 1381357000
    last_24_hours = now - 24 * 3600 * 1
    print ei.rangeQuery(period=[last_24_hours, now], field='_id').count()

main()