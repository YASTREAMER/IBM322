from scrapy import *
from bs4 import BeautifulSoup
import urllib.request

import pandas as pd
import numpy as np

import os

import ExtractionRemoval as ER
import ClassificationCalculator as CC

df=pd.read_excel("Input/Input.xlsx")

file_dict=ER.RemovalText('Input/removal.txt')

FileNameP=[]#This stores all the name of the processed article stored in the system
FileName=[]#This stores all the name of the article stored in the system
IntShape=0

#used clean and extract the data
while (IntShape!=114):
    
    name = ER.DataExtration(df.iloc[IntShape,0],df.iloc[IntShape,1],file_dict)
    FileName.append(name)

    name=ER.StopWordRemoval(name,df.iloc[IntShape,0])

    FileNameP.append(name)
    IntShape+=1

#Used to Calculate the rest of the things

df[["POSITIVE SCORE","NEGATIVE SCORE","POLARITY SCORE","SUBJECTIVITY SCORE","AVG SENTENCE LENGTH","PERCENTAGE OF COMPLEX WORDS","FOG INDEX","AVG NUMBER OF WORDS PER SENTENCE","COMPLEX WORD COUNT","WORD COUNT","SYLLABLE PER WORD","PERSONAL PRONOUNS","AVG WORD LENGTH"]]=0
IntShape=0
DataFrameInt=2
Polarity_scores=[]#Used to store the postive negative and neutral score
# TotalWordsArr=[]
# ComplexwordArr=[]
# NoSyllabusArr=[]
# SyllabussWordArr=[]
# PercentageComplexArr=[]
# polarArr=[]
# SubArr=[]
# pronounsArr=[]
# AverWordArr=[]
# SentenceLengthArr=[]
# AverageSentenceArr=[]
# FogIndexArr=[]
while (IntShape!=114):
    DataFrameInt=2

    #Used to store the postive negative and neutral score
    Neg,Neu,Pos=CC.ScoreCalculator(FileNameP[IntShape])

    #Stores the total number of words, complex words amd syllabus 
    TotalWords,Complexword,NoSyllabus=CC.CountWords(FileNameP[IntShape])

    CharCount=0
    #SYllabus per word
    SyllabussWord=(NoSyllabus/TotalWords)

    #Complex word percentage
    PercentageComplex=(Complexword/TotalWords) 
    #Polarity Score and Subjectivity Score
    polar,Sub=CC.PolarityCal(TotalWords,Neg,Pos)

     #Number of Pronouns
    pronouns=CC.pronouns(FileName[IntShape])

    #Average word length
    AverWord=CC.WordLen(FileName[IntShape])

    #Total number of Sentences
    SentenceLength=CC.Sentence(FileName[IntShape])

    #Average lenght of the senetence
    AverageSentence=TotalWords/SentenceLength

    #Fog Index
    FogIndex=(0.4*(AverageSentence+PercentageComplex))


    df.iloc[IntShape,DataFrameInt]=Pos
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=Neg
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=polar
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=Sub
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=AverageSentence
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=PercentageComplex
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=FogIndex
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=AverWord
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=Complexword
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=TotalWords
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=SyllabussWord
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=pronouns
    DataFrameInt+=1
    df.iloc[IntShape,DataFrameInt]=AverWord
    DataFrameInt+=1    

    IntShape+=1


df.to_excel("output.xlsx")