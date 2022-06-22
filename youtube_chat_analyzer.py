import pytchat
from graph_painter import graph_painter


def analyze():
    video_id: str = input("please type youtube video id: ")
    keywords = list(input(
        "Type keywords that you want to match, make sure separate each keyword into spaces. Case insensitive.\nex) lol yabe lmao\n* Type enter in order to keep the default setting(lmao lol lewd yabe)\n").split())
    try:
        chat = pytchat.create(video_id=video_id)
    except:
        print('Invalid video id. please try again.')
        analyze()
        return
    graph_painter(chat, keywords).draw_chat_graph()


if __name__ == '__main__':
    analyze()
