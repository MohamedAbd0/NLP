import tkinter
from tkinter import *
import nltk
from nltk.corpus import brown
root = tkinter.Tk()
root.title("NLP Text Prodection")
root.geometry("250x200")
lst_filter_Dec={}
var = StringVar()
def Test (txt_en):
    lst_filter_Dec={}
    var = StringVar()
    if len(txt_en.split())>1:
        detect_sentence( Words_sentence(txt_en))
    elif len(txt_en.split())==1 :
        detect_sentence( Char_words(txt_en))
def Char_words(keyWord):
    news=brown.words(categories='news')
    lst_filter_Dec=nltk.FreqDist([s for s in news if s.startswith(keyWord)])
    if len(lst_filter_Dec.keys())==0 :
        return Words_sentence(keyWord.split()[0])
    return lst_filter_Dec
def Words_sentence(keyWord):
    news=brown.sents(categories='news')
    keyWord=" "+keyWord+" "
    sc=keyWord.split()
    t=sc[len(sc)-1]
    lst_filter_Dec=nltk.FreqDist([str(keyWord+l.split()[l.split().index(t)+1]) for s in news for l in ' '.join(s).split(',') if keyWord in l and l.split()[len(l.split())-1]!=t])     
    return lst_filter_Dec
def detect_sentence(lst_filter_Dec):
    if (len(lst_filter_Dec.values())):
        for item in lst_filter_Dec.keys():
            if lst_filter_Dec[item] ==max(lst_filter_Dec.values()):
                var.set(item)
                print(item)
        print(" The Number of the same words is :",len(lst_filter_Dec.keys()),"The Max of repeting is :",max(lst_filter_Dec.values()))
        for m in lst_filter_Dec:
            print(m + ':', lst_filter_Dec[m], end='\n')
        return lst_filter_Dec
    else:
        var.set("Not Found")
def GUI():
    lb1=tkinter.Label(root,text="Enter your sentence : ",fg = "red", font = "Helvetica 16 bold italic")
    lb1.grid(row=0)
    en1=tkinter.Entry(root,fg = "Blue", font = "Times 16 bold")
    en1.grid(row=1,columnspan=2)
    bt=tkinter.Button(root,text="Production",relief='raised',command = lambda:Test(en1.get()))
    bt.grid(row=5,column=0,columnspan=3)     
    lb1Res=tkinter.Label(root,text=" your sentence prodection is :- ",fg = "red",font = "Helvetica 10 bold italic")
    lb1Res.grid(row=6)
    lb1ResPro=tkinter.Label(root,textvariable=var,fg = "Blue",font = "Helvetica 12 bold italic")
    lb1ResPro.grid(row=7)
    root.mainloop()

GUI()
