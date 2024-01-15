import math
import re
from collections import Counter
from collections import OrderedDict


def maxval(wordtoidf):
    counterformaxvalues = max(wordtoidf.items(), key=lambda x: x[1])
    dicmax = {}

    
    for word, tfidfscorerounded in wordtoidf.items(): #checking for a tie
        if(tfidfscorerounded == counterformaxvalues[1]):
            dicmax[word] = tfidfscorerounded

    
    if (len(dicmax) > 1):
        dicmax = OrderedDict(sorted(dicmax.items(), key=lambda t: t[0])) #ordered alphabetically and sorted using values
        counterformaxvalues = max(dicmax.items(), key=lambda x: x[1]) #sorting by max val
    
    return counterformaxvalues
    
    
def process_file(fileinput):
    
    
    
    with open(fileinput, 'r') as file:
        text = file.read()
    #Cleaning 
    finalstring = text
    
  
    patternTomatch = r'http.*\b'   #Scanning for website links
    finalstring = re.sub(patternTomatch, '', finalstring) 
    


    
    finalstring = finalstring.replace('\n', ' ') #Replacing new row with space 
    




    
    patternTomatch = r'[W ]+' #Removing all unwanted characters
    finalstring = re.sub(patternTomatch, '', finalstring)
    
    
            
    patternTomatch = r' +'  #Removing extra white spaces
    finalstring = re.sub(patternTomatch, ' ', finalstring)



    
    
    finalstring = finalstring.lower()#Using the lower function to convert all to lowercase
    #Removing the stopwords
    liststopwords = []
    with open('stopwords.txt') as file:
        for row in file:
            liststopwords.append(row.strip())
        
    eachword = finalstring.split()
    
    no_liststopwords_words  = [word for word in eachword if word not in liststopwords]
    finalstring = ' '.join(no_liststopwords_words)
    #Stemming and Lemmatization   
    patternTomatch = 'ing$'  
    
    finalstring = re.sub(patternTomatch, '', finalstring)
    
    patternTomatch = 'ly$'    
    
    finalstring = re.sub(patternTomatch, '', finalstring)
    
    patternTomatch = 'ment$'    
    
    finalstring = re.sub(patternTomatch, '', finalstring)
    
        
    preproc_file = open( ''.join( ("preproc_", fileinput)) ,"w")
    
    preproc_file.write(finalstring)
    

    #Computing TF-IDF scores
    #word frequencies of distinct words
    eachword = finalstring.split()
    
    diccountofwords = Counter(eachword)
    #Term frequencies
    dicwordtf = {}

    for word, count in diccountofwords.items(): #TF

        
        tf_of_word = count / len(eachword)  

        
        dicwordtf[word] = tf_of_word


    
    return dicwordtf
    
def main():
    dicwordsperdoc = {}
    doccount = 0
    occuranceperdoc = 0
    setofallwordsindocs = set()
    dicwordtf = {}
    dicwordidf = {}
    wordtoidf = {}
    
    
    docsfiletfid = 'tfidf_docs.txt'
    
    with open(docsfiletfid) as docs:

        
        for nameofdoc in docs:
            nameofdoc = nameofdoc.strip() #strip name 
            dicwordtf = process_file(nameofdoc) #run method on file for preprocessing
            dicwordsperdoc[nameofdoc] = dicwordtf #add to dic


    
    for nameofdoc, dicwordtf in dicwordsperdoc.items():
        setofallwordsindocs.update(dicwordtf.keys())


        
    counterofdocs = len(dicwordsperdoc) 


    
    for word in setofallwordsindocs:
        occuranceperdoc = 0
        
        for nameofdoc, dicwordtf in dicwordsperdoc.items(): #Checking if word is in doc for each document
            if word in dicwordtf.keys():
                occuranceperdoc = occuranceperdoc + 1
                
        if occuranceperdoc == 0:
            idf = 0

            
        else:
           
            idf = math.log(counterofdocs / occuranceperdoc) #Calculating IDF
            
        dicwordidf[word] = idf + 1
    
    top5maxval=[]
    counterformaxvalues = 0
    
    
    for nameofdoc, dicwordtf in dicwordsperdoc.items():

        
        for word in dicwordtf.keys():

            
            tf = dicwordtf[word]
            idf = dicwordidf[word]
            tfidfscorerounded = tf * idf
            wordtoidf[word] = round(tfidfscorerounded, 2)
        
        for i in range(5):

            
            if len(wordtoidf) == 0:
                break
            counterformaxvalues = maxval(wordtoidf)
            top5maxval.append(counterformaxvalues)
            word = counterformaxvalues[0]
            del wordtoidf[word]


            
        #Printing the top 5 max vals 
        with open(''.join(("tfidf_", nameofdoc)) ,"w") as file:
            file.write(str(top5maxval)) 
        wordtoidf = {}
        top5maxval = []
            
if __name__ == "__main__":
    main()