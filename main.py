import nltk
import math
import urllib.request
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


print("Search Engine using Natural Language Processing in Python")
string = input("Enter the search query : ")

######################################################Performing Tokenization using nltk#########################################
tokens = nltk.word_tokenize(string)
print("Tokenized query is : ")
for i in nltk.word_tokenize(string):
       print (i)

######################################################Removing stopwords#########################################################
stop_words = set(stopwords.words("english"))

filtered_string = []
print("\nFiltered string that contains words except articles, pronouns & prepositions : ")
for w in tokens:
       if w not in stop_words:
          filtered_string.append(w)

print(filtered_string)


###########################################################Performing Stemming using nltk#############################################

ps = PorterStemmer()
stemmed_string = []
print("\nStemmed words which are present in filtered string : ")
for w in filtered_string:
       stemmed_string.append(ps.stem(w))

print(stemmed_string)
n = len(stemmed_string)

print("\n\n\n")

############################################################# KMP Algorithm  ##########################################################
# Python program for KMP Algorithm
def KMPSearch(pat, text, mydict):
    array1 = []
    array2 = []
    M = len(pat)
    N = len(text)
    b = 0
    p = 0
    # create lps[] that will hold the longest prefix suffix 
    # values for pattern
    lps = [0]*M
    j = 0 # index for pat[]
 
    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)
 
    i = 0 # index for txt[]
    while i < N:
        if pat[j] == text[i]:
            i += 1
            j += 1
 
        if j == M:
            p += 1
            j = lps[j-1]
 
        # mismatch after j matches
        elif i < N and pat[j] != text[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1      
    mydict.update({pat:p})
 
def computeLPSArray(pat, M, lps):
    len = 0 # length of the previous longest prefix suffix
 
    lps[0] # lps[0] is always 0
    i = 1
 
    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            if len != 0:
                len = lps[len-1]
                # note that we do not increment i here
            else:
                lps[i] = 0
                i += 1
############################################################################################################################################################
print("Searching.........................................")
print("\n")
text_file = open("links.txt","r")
normalizedict = dict()
countelem = [0]*len(stemmed_string)
for link in text_file.readlines():
        if (link == '\n'):
            pass
        else :
            tf = []
            idf = []
            p = 0
            url = link
            print("-----------------------------------------------------------------------------------------------------")
            print("URL of the webpage is : ",url)
            try:
              resp = urllib.request.urlopen(url)
              html = resp.read()
            except urllib.error.URLError as e:
              contents = e.read()
            soup = BeautifulSoup(html,"html.parser")                        # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            text = soup.get_text()                            # get text 
            lines = (line.strip() for line in text.splitlines()) # break into lines and remove leading and trailing space on each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))             # break multi-headlines into a line each
            text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
            mydict = dict()
            d = 0
            e = 0
            
            for word in stemmed_string:
                 KMPSearch(word, text, mydict)
                 
            for items in mydict.keys():
                  
                        if mydict[items] == 0:
                            pass
                        else:
                            countelem[p] = countelem[p] + 1
                        p = p + 1

            for i in mydict:
                d = d + mydict[i]
            e = d*1.0/len(text)
            if e == 0:
              pass
            else:
              normalizedict.update({link:e})
            print(mydict)
            print("Normalized value (sum of values present)/(length of text) is :  ",e)
print("-----------------------------------------------------------------------------------------------------")
#################################################### Output on basis of normalization ###############################################################################       
print("\n")
#print(normalizedict)
print("\n############### Results ###############")
print("\n")
sorted_list = [k for v,k in sorted([(v,k) for k,v in normalizedict.items()], reverse = True)]
for i in sorted_list:
     print(i)
print("\n")
print("###############A document is relevant if normalization is greater than 0.25 and is retrieved if normalization > 0 \n")
#######################################################################################################################################################

#####################################################Calculating Precision ###############################################################################
retrieve = 0
relevant = 0
for i in normalizedict.keys():
      if normalizedict[i] >= 0.0015:
             relevant = relevant+1
      elif normalizedict[i] >= 0:
             retrieve = retrieve + 1
if retrieve != 0:
  print("###############Precision for the given set of documents is ",relevant/retrieve)
print("\n \n")
print("\n###############Results on the basis of tf*idf ###############\n")
#########################################################################################################################################################
text_file = open("links.txt","r")
score = dict()
for difflink in text_file.readlines():
        if (difflink == '\n'):
            pass
        else :
            tf = []
            idf = []
            tfidf = []
            q = 0
            diffurl = difflink
            print("-----------------------------------------------------------------------------------------------------")
            print("URL of given webpage is : ",diffurl)
            try:
              resp = urllib.request.urlopen(diffurl)
              html = resp.read()
            except urllib.error.URLError as e:
              contents = e.read()
            soup = BeautifulSoup(html,"html.parser")                        # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            text = soup.get_text()                            # get text 
            lines = (line.strip() for line in text.splitlines()) # break into lines and remove leading and trailing space on each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))             # break multi-headlines into a line each
            text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
            mydict = dict()
            d = 0
            e = 0
            
            for word in stemmed_string:
                 KMPSearch(word, text, mydict)
            s = sum(mydict.values())
            for elements in mydict.keys():
               if s != 0 :
                   tf.append(mydict[elements]/s)
               if countelem[q] == 0:
                   idf.append(0)
               else:
                  idf.append(math.log(8/countelem[q]))
               q = q + 1
            print("tf = ",tf)
            print("idf = ",idf)
            for i in range(0,len(tf)):
                  tfidf.append(tf[i]*idf[i])
            print("tfidf = ",tfidf)
            e = sum(tfidf)
            print("Score for the given link is : ",e)
            score.update({difflink:e})
print("-----------------------------------------------------------------------------------------------------")
print("\n")
##################################################### Output on the basis of tf*idf ###############################################################################
#print(score)
print("\n############### Results ###############")
print("\n")
sorted_list = [k for v,k in sorted([(v,k) for k,v in score.items()],reverse = True)]
for i in sorted_list:
     print(i)
text_file.close()
##########################################################################################################################################################
