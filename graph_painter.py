import pytchat
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from time_util import to_time
import matplotlib.dates as mdates


class graph_painter:
    keywords: list = ['lmao', 'lol', 'lewd', 'yabe']

    def __init__(self, chat: pytchat, keywords: list = None):
        self.chat = chat
        self.chat.get()  # Get rid of First data
        self.acc = self.getHighlightScore(self.chat.get().items)
        self.count = 1
        self.x = []
        self.y_highlight_score = []
        self.y_avg = []
        self.y_avg_15 = []  # 1.15 times
        self.y_avg_2 = []  # 1.2 times
        self.y_avg_3 = []  # 1.3 times
        self.ani = FuncAnimation(plt.gcf(), self.animate, interval=100)
        if keywords:
            self.keywords = keywords
        print("Applied keywords : " + str(self.keywords))

    def draw_chat_graph(self):
        plt.show()

    def animate(self, i):
        if not self.chat.is_alive():
            print("Completed.")
            self.ani.pause()
            return

        items = self.chat.get().items
        if not items:
            return

        score = self.getHighlightScore(items)
        # Highlight score = (# of chat + # of keywords match)
        self.x.append(to_time(items[0].elapsedTime))
        self.y_highlight_score.append(score)
        avg = self.acc // self.count
        self.y_avg.append(avg)
        self.y_avg_15.append(avg * 1.15)
        self.y_avg_2.append(avg * 1.2)
        self.y_avg_3.append(avg * 1.3)
        self.acc += score
        self.count += 1
        plt.cla()
        plt.xlabel('timeline')
        plt.ylabel('highlight score')  # chat count per 2 ~ 10 second

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.plot(self.x, self.y_highlight_score, label='realtime')
        plt.plot(self.x, self.y_avg, label='avg')
        plt.plot(self.x, self.y_avg_15, label='avg * 1.15')
        plt.plot(self.x, self.y_avg_2, label='avg * 1.2')
        plt.plot(self.x, self.y_avg_3, label='avg * 1.3')

        plt.gcf().autofmt_xdate()
        plt.legend()

    def getHighlightScore(self, items):
        return len(items) + self.getKeywordHitCount(items)

    def getKeywordHitCount(self, items):
        return len([x for x in items if self.isMsgContainsKeyword(x.message)])

    def isMsgContainsKeyword(self, msg):
        target = msg.lower()
        return any(keyword in target for keyword in self.keywords)
