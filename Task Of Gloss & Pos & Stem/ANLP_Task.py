from __future__ import unicode_literals
import pyaramorph
import tkinter
from tkinter import *

root = tkinter.Tk()
root.title("Morphology")
root.geometry("350x300")
Analyse = pyaramorph.Analyzer()

var = StringVar() #store result
posSent={} #store all pos for eash word
CorrectPos={} #store currect pos
Gloss={} #store gloss of sent
# prob of prior      P(pos/pos)
def Prior(w2,w1):
    if(w1=='VERB' and w2=='NOUN'):
        return 0.4
    elif(w1=='VERB' and w2=='VERB'):
        return 0.01
    elif(w1=='NOUN' and w2=='NOUN'):
        return 0.2
    elif(w1=='NOUN' and w2=='ADJ'):
        return 0.4
    elif(w1=='VERB' and w2=='ADJ'):
        return 0.02
    elif(w1=='FUNC' and w2=='VERB'):
        return 0.4
    elif(w1=='FUNC' and w2=='NOUN'):
        return 0.3
    else :
        return 0.0001
    
# clc prob of Likelihood  P(word/pos) from arabic tree bank
def LikeLihood(Wrd_Pos,lema):
    PosTreeBank={'NOUN':'Treebank_subcats_nouns-nrm.txt','VERB':'Treebank_subcats_verbs-nrm.txt','ADJ':'Treebank_subcats_adjectives-nrm.txt'}
    Data = open(PosTreeBank[Wrd_Pos],"r") 
    lines=Data.readlines()
    Data.close()
    for line in lines:
        if(lema == line.split(':')[1].split("\t")[0] ):#splite to lema
            return line.split(':')[3].split('\t')[0] #splite to prob
    return 0.0001

# to fill posSent pos for each words
def ChkPos(wrd):
    posWord={}
    Table = Analyse.analyze_text(wrd)
    i=1
    while(i<len(Table[0])):
        #split to get the pos from solution of pyaramorph
        P=Table[0][i].split('pos: ')[1].split('/')[1].split('_')[0]
        if(len(P)==4):
            posWord[P]=Table[0][i].split('pos: ')[0].split('[')[1].split(']')[0]
        else:
            pp=(Table[0][i].split('pos: ')[1].split('\n')[0].split('_')[0].split('/')[len(Table[0][i].split('pos: ')[1].split('\n')[0].split('_')[0].split('/'))-1])
            if(pp=='NOUN' or pp=='VERB' or pp == 'ADJ'):   
                posWord[pp]=Table[0][i].split('pos: ')[0].split('[')[1].split(']')[0]
        i=i+1
    posSent[wrd]=posWord

#clc equation 
def ClcProb():
    l=0#flag
    for ii in CorrectPos:
        ppp={}#store value of prob of each pos
        if(CorrectPos[ii]==0):
            lstp=posSent[ii]
            for item in list(lstp.keys()) :
                prob=( float(LikeLihood(item,lstp[item])) * float(Prior(item,CorrectPos[list(CorrectPos.keys())[l-1]])) * float(Prior(item,CorrectPos[list(CorrectPos.keys())[l+1]])))
                ppp[item]=prob
            #to get max of prob of pos
            for itm in ppp.keys():
                if( len(list(ppp.values())) !=0  and ppp[itm]==max(ppp.values())):
                    CorrectPos[ii]=itm #store
        l=l+1

    for iii in CorrectPos :
        if(CorrectPos[iii]==0 and iii.startswith('ال')):
            CorrectPos[iii]='NOUN'
    
def ChkGloss(wrd):#gloss of words from solution
    Table = Analyse.analyze_text(wrd)
    i=1
    while(i<len(Table[0])):
        P=Table[0][i].split('pos: ')[1].split('/')[1].split('_')[0]
        if(len(P)==4 and  (Table[0][i].split('pos: ')[0].split('[')[1].split(']')[0]) == CorrectPos[wrd]) :
            Gloss[wrd]=Table[0][i].split('gloss:')[1].split('+')[1].split(';')[0]
        else:
            pp=(Table[0][i].split('pos: ')[1].split('\n')[0].split('_')[0].split('/')[len(Table[0][i].split('pos: ')[1].split('\n')[0].split('_')[0].split('/'))-1])
            if(pp==CorrectPos[wrd]):   
                Gloss[wrd]=Table[0][i].split('gloss:')[1].split('+')[1].split(';')[0].split('/')[0]
        i=i+1
#call pos fun     
def POS(Sent):
    WORDS=Sent.split(" ")
    for word in WORDS:
        ChkPos(word)
    for item in posSent:    
        if(len(set(posSent[item].keys())) == 1):
            CorrectPos[item]=list(set(posSent[item].keys()))[0]
        else :
            CorrectPos[item]=0            
    ClcProb()
    var.set(CorrectPos)
#call gloss fun
def FnGloss(Sent):
    if(len(list(CorrectPos.keys()))==0):
        POS(Sent)
        
    for j in list(CorrectPos.keys()):
        Gloss[j]=0
    for jj in list(CorrectPos.keys()):
        ChkGloss(jj) 
    for jjj in list(CorrectPos.keys()):
        if(Gloss[jjj]==0):
            Table = Analyse.analyze_text(jjj)
            Gloss[jjj]=Table[0][1].split('gloss:')[1].split('+')[1].split(';')[0].split('/')[0]
    var.set(Gloss)
#call stem fun
def StemSearch(fstem):
    words="قول مكتبه  قال قائل مقالات كتب و كاتب قيل ".split(" ") #to more words connect to file
    restem=[fstem] #المصدر المعتل الاوسط ممكن حرف العلة يتحول لحرف ال و او ي 
    if('ا' in fstem):
        ustem=list(fstem)
        ind=fstem.index('ا')
        ustem[ind]='و'
        restem.append("".join(ustem))#عشان اضيف العنصر الجديد
        ustem[ind]='ي'
        restem.append("".join(ustem))#اضافة العنصر
    elif(fstem[len(fstem)-1]=='ى'):
        ustem=list(fstem)
        ind=len(fstem)-1
        ustem[ind]='و'
        restem.append("".join(ustem))#اضافة عنصر
        ustem[ind]='ي'
        restem.append("".join(ustem))#اضافة عنصر

    #عشان اوصل لكل المشتقات الاول بقارن كل مصدر بكل كلة عندي شرط لزم حروف المصدر موجوده في الكلمة والشرط التاني ترتيب عناصر حروف المص
    lst=[word for stem in restem for word in words if (stem[0] in word and stem[1] in word and stem[2] in word and word.index(stem[0]) < word.index(stem[1])and word.index(stem[1]) < word.index(stem[2])) and ((word.index(stem[2])- word.index(stem[1])== 1) or ((word.index(stem[2])- word.index(stem[1])!= 1) and word[word.index(stem[1])+1] in 'اويئ') or ((word.index(stem[1])- word.index(stem[0])!= 1) and word[word.index(stem[0])+1] in 'اويئ'))   ]
    var.set(lst)#result
    

def GUI():
    lb1=tkinter.Label(root,text="Enter your sentence : ",fg = "red", font = "Helvetica 16 bold italic")
    lb1.grid(row=0)
    en1=tkinter.Entry(root,fg = "Blue",width=20, font = "Times 20 bold")
    en1.grid(row=1,columnspan=2)
    btStem=tkinter.Button(root,text="Stem",width=20,bg="yellow",font=14,padx=3,pady=3,relief='raised',command = lambda:StemSearch(en1.get()))
    btStem.grid(row=5,column=0,columnspan=3)
    btPos=tkinter.Button(root,text="Pos",width=20,bg="yellow",font=14,padx=3,pady=3,relief='raised',command = lambda:POS(en1.get()))
    btPos.grid(row=6,column=0,columnspan=3)
    btGloss=tkinter.Button(root,text="Gloss",width=20,bg="yellow",font=14,padx=3,pady=3,relief='raised',command = lambda:FnGloss(en1.get()))
    btGloss.grid(row=7,column=0,columnspan=3)
    lb1Res=tkinter.Label(root,text=" your Solution is :- ",fg = "Blue",font = "Helvetica 16 bold italic")
    lb1Res.grid(row=8)
    lb1ResPro=tkinter.Label(root,textvariable=var,fg = "red",font = "Helvetica 18 bold italic")
    lb1ResPro.grid(row=9)
    root.mainloop()

GUI()
