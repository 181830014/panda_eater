from wordcloud import WordCloud
from textblob import TextBlob

if __name__ == '__main__':

    keywords = ''
    for idx in range(1,21):
        print(idx)
        text = ''
        filepath = './results/data' + str(idx) + '.txt'
        f = open(filepath, 'r', encoding='utf8').read()
        plain_text = f.lower()
        for line in plain_text.splitlines():
            if 'answer' in line:
                continue
            if '[closed]' in line or '[duplicate]' in line:
                continue
            # words = line.split(' ')
            # if(len(words) == 0):
            #     continue
            text += line
        blob = TextBlob(text)
        print(len(blob.noun_phrases))
        for word in blob.noun_phrases:
            keywords += word + ' ' 
    
    cloud = WordCloud().generate(keywords)
    image = cloud.to_image()
    image.show()
