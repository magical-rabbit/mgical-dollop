#感谢知乎：https://zhuanlan.zhihu.com/p/138356932

import matplotlib.pyplot as plt #数据可视化
import jieba #词语切割
import wordcloud #分词
from wordcloud import WordCloud,ImageColorGenerator,STOPWORDS #词云，颜色生成器，停止词
import numpy as np #科学计算
from PIL import Image #处理图片

def ciyun():
    with open('data.txt','r',encoding='gbk') as f:  #打开新的文本转码为gbk
        textfile= f.read()  #读取文本内容
    wordlist = jieba.lcut(textfile)#切割词语
    space_list = ' '.join(wordlist) #空格链接词语
    #print(space_list)
    backgroud = np.array(Image.open('template/91529822720e0cf31ea30fc80946f21fbe09aaa9.jpg')) 
	
    wc = WordCloud(width=80000, height=80000,
			background_color='white',
	        mode='RGB', 
			mask=backgroud, #添加蒙版，生成指定形状的词云，并且词云图的颜色可从蒙版里提取
			max_words=600,
			stopwords=STOPWORDS,#内置的屏蔽词,并添加自己设置的词语
			font_path='C:\Windows\Fonts\STZHONGS.ttf',
			max_font_size=150,
			relative_scaling=0.6, #设置字体大小与词频的关联程度为0.4
			random_state=50, 
			scale=2 
			).generate(space_list) 
			
    image_color = ImageColorGenerator(backgroud)#设置生成词云的颜色，如去掉这两行则字体为默认颜色
    wc.recolor(color_func=image_color)

    plt.imshow(wc) #显示词云
    plt.axis('off') #关闭x,y轴
    plt.show()#显示
    wc.to_file('test1_ciyun.jpg') #保存词云图

def main():
    ciyun()
 
if __name__ == '__main__':
    main()