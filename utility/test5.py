from tweet_interface import TweetInterface
from tool import getCurrentStampUTC
import matplotlib.pyplot as plt

def main():
    ti = TweetInterface()

    counts = []
    x = []
    now = 1381536000
    interval = 24*3600
    max = 0
    for day in xrange(3000):
        begin_time = now - (day + 1) * interval
        end_time = now - day * interval
        c = ti.rangeQuery(period=[begin_time, end_time], field='_id').count()
        counts.append(c)
        x.append(str((12-day)%30))
        if c > 0:
            if c > max:
                max = c
        print max
'''
    plt.plot(range(len(counts)), counts)
    plt.xticks(range(len(counts)), x)
    plt.xlabel('Date from 10/12/2013 to 09/13/2013')
    plt.ylabel('Number of tweets in Mongodb')
    plt.title('Number of tweets during the past 30 days')
    plt.show()
'''
main()