import webbrowser, sys
search_word = " ".join(sys.argv[1:])
webbrowser.open('https://www.google.co.jp/maps/search/{}'.format(search_word))
