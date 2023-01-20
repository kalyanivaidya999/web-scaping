#!/usr/bin/env python
# coding: utf-8

# ## Import required libraries

# In[1]:


import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 


# ## Load Data

# In[2]:


df = pd.read_csv(r"C:\Users\Tushar\Desktop\kalyani\Input.Sheet1.csv")


# In[3]:


df.head(10)


# ## scrabing data from links

# In[4]:


headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}
data = df.URL
ID = df.URL_ID


# In[ ]:


record=[]
for i,url in zip(ID,data):
    page = requests.get(url,headers=headers).text
    soup = BeautifulSoup(page,"html.parser")
    
    article_title = soup.find('h1',class_='entry-title')
    if not article_title: 
        print('NO .entry-title CONTENT FROM',i)
        continue 
    title=article_title.text.replace('\n',"  ").replace('\xa0'," ")

    article = soup.find('div',class_='td-post-content')
    body = article.text.replace('\xa0'," ").replace('\n'," ")
    
    record.append([title,body])
    


# ## cleaning and preparing data 

# In[ ]:


df.drop('URL_ID',axis=1,inplace=True)


# In[ ]:


df.drop(index=[43,56,113],inplace = True)


# In[ ]:


stop_words = list(set(stopwords.words('english')))


# In[ ]:


cleaned_articles = [' ']*len(record) #cleaned record


# In[ ]:


for i in range(len(record)):
    for w in stop_words:
        cleaned_articles[i]= str(record[i]).replace(' '+w+' ',' ').replace('?','').replace('.','').replace(',','').replace('!','')


# processing of data

# In[ ]:


#count of words
count_word=[] 
for i in range(len(cleaned_articles)):
    count_word.append(len(word_tokenize(cleaned_articles[i])))


# In[ ]:


#seperate words
words=[] 
for i in cleaned_articles:
    words.append((word_tokenize(i)))


# In[ ]:


#seprate sentences 
sentences=[] 
for i in cleaned_articles:
    sentences.append(sent_tokenize(i))


# In[ ]:


#count of sentences
len_sent=[]
for i in range(len(cleaned_articles)):
    len_sent.append((len(cleaned_articles[i])))


# ## Analysing data 

# In[ ]:


# load negative positive files
def readwords( filename ):
    f = open(filename)
    words = [ line.rstrip() for line in f.readlines()]
    return words


# In[ ]:


negative = readwords(r"C:\Users\Tushar\Desktop\kalyani\MasterDictionary\negative-words.txt")
positive = readwords(r"C:\Users\Tushar\Desktop\kalyani\MasterDictionary\positive-words.txt")


# In[ ]:


#to find +ve and -ve score
pos_score=[]
neg_score=[]    
for i in range(0,len(cleaned_articles)):
    pos=0
    neg=0
    #k=str(cleaned_articles[i])
    #count = Counter(k.split())
    for key in cleaned_articles[i].split(' '):
        key = key.rstrip('.,?!\n]""[') # removing possible punctuation signs
        if key in positive:
            pos += 1
        if key in negative:
            neg += 1
    pos_score.append(pos)
    neg_score.append(neg)      


# In[ ]:


df['POSITIVE SCORE'] = pos_score


# In[ ]:


df['NEGATIVE SCORE'] = neg_score


# In[ ]:


df['POLARITY SCORE'] = (df['POSITIVE SCORE']-df['NEGATIVE SCORE'])/ ((df['POSITIVE SCORE'] +df['NEGATIVE SCORE']) + 0.000001) 


# In[ ]:


df['SUBJECTIVITY SCORE'] = (df['POSITIVE SCORE'] + df['NEGATIVE SCORE'])/(count_word) + 0.000001


# In[ ]:


df['AVG SENTENCE LENGTH'] = np.array(count_word)/np.array(len_sent)


# In[ ]:


df['AVG NUMBER OF WORDS PER SENTENCES'] = df['AVG SENTENCE LENGTH']


# In[ ]:


complex_words = []
sylabble_counts = []
for i in range(len(sentences)):
    sylabble_count=0
    d=str(sentences[i]).split()
    ans=0
    for word in d:
        count=0
        for i in range(len(word)):
            if(word[i]=='a' or word[i]=='e' or word[i] =='i' or word[i] == 'o' or word[i] == 'u'):
                count+=1
                #print(word)
            if(i==len(word)-2 and (word[i]=='e' and word[i+1]=='d')):
                count-=1;
            if(i==len(word)-2 and (word[i]=='e' and word[i]=='s')):
                count-=1
        sylabble_count+=count    
        if(count>2):
            ans+=1
    sylabble_counts.append(sylabble_count)
    complex_words.append(ans)


# In[ ]:


df['sylabble counts']=sylabble_counts
df['complex words count'] = complex_words


# In[ ]:


df['WORD COUNT'] = count_word


# In[ ]:


df['PERCENTAGE OF COMPLEX WORDS'] = np.array(complex_words)/np.array(count_word)


# In[ ]:


df['SYLLABLE PER WORD'] = np.array(sylabble_counts)/np.array(count_word)


# In[ ]:


df['FOG INDEX'] = 0.4 * (df['AVG SENTENCE LENGTH'] + df['PERCENTAGE OF COMPLEX WORDS'])


# In[ ]:


df['AVG NUMBER OF WORDS PER SENTENCES'] = df['AVG SENTENCE LENGTH']


# In[ ]:


total_characters = []
for i in range(len(record)):
    characters = 0
    for word in str(sentences[i]).split():
        characters+=len(word)
    total_characters.append(characters)  


# In[ ]:


df['AVG WORD LENGTH'] = np.array(total_characters)/np.array(count_word)


# In[ ]:


personal_nouns = []
personal_noun =['I', 'we','my', 'ours','and' 'us','My','We','Ours','Us','And'] 
for i in range(len(sentences)):
    ans=0
    for word in str(sentences[i]):
        if word in personal_noun:
            ans+=1
    personal_nouns.append(ans)


# In[ ]:


df['PERSONAL PRONOUN'] = personal_nouns


# In[ ]:


df.head(10)


# ## save file 

# In[ ]:


blackcoffer_output_file = pd.DataFrame(df) 


# In[ ]:


file_name = 'blackcoffer_output.xlsx'
blackcoffer_output_file.to_excel(file_name)


# Thank you!
