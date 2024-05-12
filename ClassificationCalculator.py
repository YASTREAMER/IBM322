from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment" #using a pretrained model 
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import re

ps = PorterStemmer()


#This is used to Calculate the Average postive negative and neutrality score
def ScoreCalculator(FileName):

    f=open(FileName, 'r')
    NegativeScore=0    
    PositiveScore=0
    NeutralScore=0
    number=0
    StringWord=[]
    ExceptionEncountered=False
    Scores_exp=[0,0,0]

    for line in f:
        number+=1
        try:
            encoded_text = tokenizer(line, return_tensors='pt')
            output = model(**encoded_text)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            NegativeScore=NegativeScore+scores[0]
            NeutralScore=NeutralScore+scores[1]
            PositiveScore=PositiveScore+scores[2]
        except:
            StringWord.append(line)
            ExceptionEncountered=True
            

    if(ExceptionEncountered):
        Scores_exp=ExceptionHandler(StringWord)       
        Average_dict = {
            'roberta_NegativeScore' : (NegativeScore+Scores_exp["NegativeScore"])/(number+1),
            'roberta_NeutralScore' : (NeutralScore+Scores_exp["NeutralScore"])/(number+1),
            'roberta_PositiveScore' : (PositiveScore+Scores_exp["PositiveScore"])/(number+1)
        }
    else:
         Average_dict = {
            'roberta_NegativeScore' : NegativeScore/number,
            'roberta_NeutralScore' : NeutralScore/number,
            'roberta_PositiveScore' : NeutralScore/number,
        }       
    
    return(NegativeScore/number,NeutralScore/number,NeutralScore/number,)

#This function is used to handle the Exception thrown by the Model as the model does not support tensor larger than 520
def ExceptionHandler(String):
    NegativeScore=0    
    PositiveScore=0
    NeutralScore=0
    StringNeed=[]
    StringProcess=""
    itr=0
    length=len(String)
    TotalNeu=0
    TotalNeg=0
    TotalPost=0
    for StringItem in String:
        number =0
        StringNeed=StringItem.split()
        for item in StringNeed:
            if(number%25==0 and number !=0):
                scores=ModelOuput(StringProcess)
                StringProcess=""
                NegativeScore=NegativeScore+scores[0]
                NeutralScore=NeutralScore+scores[1]
                PositiveScore=PositiveScore+scores[2]
            else:
                StringProcess=StringProcess+" "+item
            number+=1
        TotalPost=(PositiveScore/number)+TotalPost
        TotalNeg=(NegativeScore/number)+TotalNeg
        TotalNeu=(NeutralScore/number)+TotalNeu


    Average_local = {
        'NegativeScore' : TotalNeg/length,
        'NeutralScore' : TotalNeu/length,
        'PositiveScore' : TotalPost/length
    }


    return(Average_local)


def ModelOuput(String):

    encoded_text = tokenizer(String, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    return(scores)


def PolarityCal(TotalWords,Neg,Positive):

    PolarityScore=((Positive-Neg)/(Positive+Neg))+0.000001

    Subjectivity=((Positive+Neg)/TotalWords)+ 0.000001

    return(PolarityScore,Subjectivity)

def CountWords(filename):
    NoComplex=0
    NoSyllabus=0
    WordCount=0
    with open(filename, 'r') as file:
        content = file.read()
        words = content.split()
        TotalWords = len(words)
        for itere in range(TotalWords):
            if(ComplexWord(words[itere])):
                NoComplex+=1  
            NoSyllabus=NoSyllabus+syllabus(ps.stem(words[itere]))
             
    return (TotalWords,NoComplex,NoSyllabus)

def ComplexWord(words):
    count=0
    for char in range(len(words)):
            if (words[char] == 'a' or words[char] == 'e' or words[char] == 'i' or words[char] == 'o' or words[char] == 'u' or words[char] == 'A' or words[char] == 'E' or words[char] == 'I' or words[char] == 'O' or words[char] == 'U'):
                count+=1
    if(count>=2):
        return(True)
    else:
        return(False)   
    
def Sentence(FileName):
    num_lines=0
    number=0
    with open(FileName,'r') as file:
        for line in file:
            number+=1
            num_lines += line.count(".")
            num_lines += line.count("?")
            num_lines += line.count(":-")
    return(num_lines)

def syllabus(word):
    count=0
    for char in range(len(word)):
            if (word[char] == 'a' or word[char] == 'e' or word[char] == 'i' or word[char] == 'o' or word[char] == 'u' or word[char] == 'A' or word[char] == 'E' or word[char] == 'I' or word[char] == 'O' or word[char] == 'U'):
                count+=1
    return(count)

def pronouns(FileName):
    pronouns=0
    pro = re.compile(r'\b(I|he|she|we|my|ours|(?-i:us))\b',re.I)
    with open(FileName,'r') as file:
        for line in file:
            pronouns = pronouns+len(pro.findall(line))
    return(pronouns)

def WordLen(FileName):
    count=0
    with open(FileName,'r') as file:
        content = file.read()
        word = content.split()
        TotalWords = len(word)
        for itere in range(TotalWords):
            WordChar=word[itere]
            for char in range(len(WordChar)):
                count+=1
        count=count/TotalWords
    return(count)

