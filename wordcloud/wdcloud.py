import jieba
from wordcloud import WordCloud

txt=open('title.txt','r',encoding='utf-8').read()
words=jieba.lcut(txt)
counts={}

for word in words:
    if '\u4e00' <= word <= '\u9fff':
        rword=word
    else:
        continue
    counts[rword]=counts.get(rword,0)+1

items=list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)

new_word=''

for i in range(20):
    word,count=items[i]
    #print("{0:<10}{1:>5}".format(word,count))
    new_word=','.join([new_word,word])

print(new_word)
wordcloud=WordCloud(font_path='STFANGSO.TTF',background_color='white').generate(new_word)
wordcloud.to_file('cloud.jpg')
