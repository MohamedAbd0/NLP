# -*- coding: utf-8 -*-
"""
@author: mohamed abdo elnashar
"""
import math
import nltk
import operator
from nltk.corpus import brown
import tkinter
from tkinter import *
root = tkinter.Tk()
root.title("NLP Text Correlation")
root.geometry("250x200")
var = StringVar()
news=brown.words(categories='news')
news_sent=brown.sents(categories='news')
dec ={} #عشان اخزن جواها كل كانديت ست لكل كلمة ا 
lst_sent=[] #دي عشان اخزن فيها كل الجمل المتوقعة
atlm={} # دي استخدمتها في توليد الجمل من الكلمات اللي طلعتلي
# الدالة دي عشان اقدر اكون الكانديدت لكل كلمة عن طريقة اني بحسب ال منيمم ايدت دستنس لكل كلمة مع كل الكوربس
def CandSet(txt):
    dec1 ={} #دي هستخدمها عشان اخد جواها كل الكانديدت ست لكل كلمة وفي الاخر هخد منها اقل 4 بس
    lst1=txt.split()
    for i in lst1:
        for j in news:
            dec1[j.lower()]=min_edit_dist(i.lower(),j.lower())
        #هنا بخزن اقل 4 ف المينيم اديت دستنس                
        dec[i.lower()]=sorted(dec1.items(), key=operator.itemgetter(1))[:4] 
        dec1={} # برجع افضية عشان اخزن لكلمة جديد
    print(dec) # هيطبع كل الكانديديت هنا انا مجزن الكلمة نفسها key والكانديدت بتاعها في ديكشنري وخزنتة في ال value
    Sentence(lst1)

def min_edit_dist(word1,word2):
    len_1=len(word1)
    len_2=len(word2)
    x = [[0]*(len_2+1) for _ in range(len_1+1)]
    for i in range(0,len_1+1):  
        x[i][0]=i
        for j in range(0,len_2+1):
            x[0][j]=j
    for i in range (1,len_1+1):
        for j in range(1,len_2+1):
            if word1[i-1]==word2[j-1]:
                x[i][j] = x[i-1][j-1]
            else :
                x[i][j]= min(x[i][j-1],x[i-1][j],x[i-1][j-1])+1
    return x[i][j]

# دي بقي الميثود الخاصة بتوليد الجملة يكون دينامك
    # الفكرة هنا انا استخدمك قانون الاحتمالات وقدرت اخزن كل جملة في ديكشنري ويفضل يضيف علية لحد ميكون الجمله كلها
def Sentence(lst):
    # ال lst دي اراي ناتجة عن اني قطعت الجملة اللي هو دخلها لكلمات
    n=0 # دا هيبقي الكي بتاع الدكشنري
    flg='F' # دي عشان اولد كل كلمة في بداية كل الجملة
    po=0 #دي عشان اللوب
    Por=(math.pow(4,len(lst)))/4 # دي عشان هشوف كل مرة هلف كام مرة
    lp=4 # دي عشان انا شغال ع اربع احتمالات لكل كلمة
    for Wrd in lst:  
        for item in dec[Wrd]:   
            while po<Por and flg =='F' :
                #print (item[0])
                atlm[n]=item[0] #هنا هيضيف كل بدايات الجمل المحتملة
                n=n+1
                po=po+1
            po=0
        while flg=='S' and lp > 0 and n<math.pow(4,len(lst)) :
            for item in dec[Wrd]:
                while po<Por :
                    atlm[n]=atlm[n]+" "+item[0] #هنا عملت update لل value عشان اقدر اولد بقيت الجملة
                    #print(atlm[n])
                    n=n+1
                    po=po+1
                po=0
            lp=lp-1    
        flg='S'
        Por=Por/4 # دي خاصة بالاحتمالات 
        lp=lp*4 # دي خاصة بردوا بالاحتمالات 
        n=0
    print( "\n Number of all Sentanse are Generated is :- ",len (list(atlm.values())))
    lst_sent= list(atlm.values()) # هنا هياخد كل الجمل اللي انا مخدنها في الفاليو وخزنتها في لست لوحدها
    # ال lst_dec دي هيبقي جواها كل الجمل وعدد تكرار كل جملة فيهم    
    lst_dec=nltk.FreqDist([ls for s in news_sent for l in ' '.join(s).split(',') for ls in lst_sent if ls in l ])
    print("\n Number of all Right Sentanse are in courps :- ",len(lst_dec.keys()))
    if (len(lst_dec.keys())):   # دي عشان لو ملقاش اي جملة عندي في الكوربس شبة الجمل اللي اتولدت 
        var.set(sorted(lst_dec.items(), key=operator.itemgetter(1),reverse=True)[0][0]) #هطبعلي اعلي جملة في التكرار
        print(" The Correction Is :- ",sorted(lst_dec.items(), key=operator.itemgetter(1),reverse=True)[0][0],"\n The number is :- ",sorted(lst_dec.items(), key=operator.itemgetter(1),reverse=True)[0][1])
    else:
        var.set("Not Found")
    
def GUI():
    lb1=tkinter.Label(root,text="Enter your sentence : ",fg = "red", font = "Helvetica 16 bold italic")
    lb1.grid(row=0)
    en1=tkinter.Entry(root,fg = "Blue", font = "Times 16 bold")
    en1.grid(row=1,columnspan=2)
    bt=tkinter.Button(root,text="Correlation",relief='raised',command = lambda:CandSet(en1.get()))
    bt.grid(row=5,column=0,columnspan=3)     
    lb1Res=tkinter.Label(root,text=" your sentence Correlation is :- ",fg = "red",font = "Helvetica 10 bold italic")
    lb1Res.grid(row=6)
    lb1ResPro=tkinter.Label(root,textvariable=var,fg = "Blue",font = "Helvetica 18 bold italic")
    lb1ResPro.grid(row=7)
    root.mainloop()

GUI()