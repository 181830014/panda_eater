from wordcloud import WordCloud


if __name__ == '__main__':
    f = open('data.txt', 'r', encoding='gb18030')
    plain_text = f.read()
    text = ''
    for line in plain_text.splitlines():
        if ('[closed]' not in line) and ('[duplicate]' not in line):
            text += line
            print(line)

    cloud = WordCloud().generate(text)
    image = cloud.to_image()
    image.show()
