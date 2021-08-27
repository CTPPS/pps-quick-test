#!/usr/bin/env python3
from ROOT import TFile
import sys
import getopt

glimit=float("inf")
summary=True
summaries=[["Path","ObjectName","AvgFail","PercentageFailedBins"]]

options, remainder = getopt.gnu_getopt(sys.argv[1:], 'l:si', ['limit', 
                                                         'info',
                                                         'summary',
                                                         ])
for opt, arg in options:
    if opt in ('-l', '--limit'):
        glimit = float(arg)
    elif opt in ('-s', '--summary'):
        summary = False
    elif opt in ('-i','--info'):
        print("Usage: histogram_compare.py [-isl] file1 file2\n -i --info\n\t o show this menu \n -s --summary\n\t to suppress summaries \n -l --limit\n\t to set limit of differences shown")
        exit()
    
if len(remainder)>1:
    f=TFile.Open(remainder[0])
    f2=TFile.Open(remainder[1])
else:
    print("Not enough files supplied, run with -i to see help")
    exit()

def compare_histos1D(h,h2,path):
    binsh=h.GetXaxis().GetNbins()
    binsh2=h2.GetXaxis().GetNbins()
    if binsh!=binsh2:
        print("Histograms have different number of bins, "+str(binsh)+" and "+str(binsh2))
        print(h.GetName(),h2.GetName())
        return False

    returnVal=True
    llimit=-1
    diff=[]
    for i in range(binsh):
        if h.GetBinContent(i)!=h2.GetBinContent(i):
            returnVal=False
            diff.append(abs((h.GetBinContent(i)-h2.GetBinContent(i))))
            llimit=llimit+1
            if(llimit<glimit):
                print(path+";\t"+h.GetName()+";\tBin("+str(i)+");\t"+str(h.GetBinContent(i))+";\t"+str(h2.GetBinContent(i)))

    if summary and not returnVal:
        diff=sorted(diff)
        summaries.append((path,h.GetName(),str(sum(diff)/len(diff)),str(len(diff)*100.0/binsh)))
    return returnVal

def compare_histos2D(h,h2,FullPath):
    binX=h.GetXaxis().GetNbins()
    binY=h.GetYaxis().GetNbins()
    binX2=h2.GetXaxis().GetNbins()
    binY2=h2.GetYaxis().GetNbins()

    if binX!=binX2 or binY!=binY2:
        print("Histograms have different number of bins:")
        print(str(binX)+" and "+str(binX2))
        print(str(binY)+" and "+str(binY2))
        print(h.GetName(),h2.GetName())
        return False

    returnVal=True
    diff=[]
    llimit=-1
    for i in range(binX):
        for j in range(binY):
            if h.GetBinContent(i,j)!=h2.GetBinContent(i,j):
                    returnVal=False
                    diff.append(abs((h.GetBinContent(i,j)-h2.GetBinContent(i,j))))
                    llimit=llimit+1
                    if(llimit<glimit):
                        print(FullPath+";\t"+h.GetName()+";\tBin("+str(i)+","+str(j)+");\t"+str(h.GetBinContent(i,j))+";\t"+str(h2.GetBinContent(i,j)))
    
    if summary and not returnVal:
        diff=sorted(diff)
        summaries.append((FullPath,h.GetName(),str(sum(diff)/len(diff)),str((len(diff)*100.0)/(binX*binY))))
    return returnVal

def GetPoint_own(g,i):
    if i<0 or i>=g.GetN(): return -1
    if not g.GetX() or not g.GetY(): return -1
    x=g.GetX()[i]
    y=g.GetY()[i]
    return (x,y)

def compare_graphs(h,h2):
    n=h.GetN()
    n2=h2.GetN()
    if n!=n2:
        print("Graphs have different number of points, "+str(n)+" and "+str(n2))
        print(h.GetName(),h2.GetName())
        return False

    for i in range(n):
        x,y=GetPoint_own(h,i)
        x2,y2=GetPoint_own(h2,i)
        if (x,y)!=(x2,y2):
            print("Graphs are different, differentiating points: ("+str(x)+","+str(y)+") and ("+str(x2)+","+str(y2)+")")
            print(h.GetName(),h2.GetName())
            return False
    return True


def search_root_rec(keys,keys2,path):
    global t
    global hl
    global hl2
    for k in keys: hl.append(k.GetName())
    for k in keys2: hl2.append(k.GetName())

    keys=sorted(keys, key=lambda tkey: tkey.GetName())
    keys2=sorted(keys2, key=lambda tkey: tkey.GetName())
    for k,k2 in zip(keys,keys2):
        h=k.ReadObj()
        h2=k2.ReadObj()
        if h.GetName()=="EventInfo":    
            continue
        if h.GetName()!=h2.GetName():
            print("Specified root files have different file structure, keys: ")
            print("1 "+h.GetName())
            print("2 "+h2.GetName())
            t=False
            continue
        if (h.ClassName()=="TH1F" and h2.ClassName()=="TH1F") : 
            if not compare_histos1D(h,h2,path): t=False
        if (h.ClassName()=="TH2F" and h2.ClassName()=="TH2F"):
            if not compare_histos2D(h,h2,path): t=False
        if h.ClassName()=="TGraph" and h2.ClassName()=="TGraph": 
            if not compare_graphs(h,h2): t=False
        if h.ClassName()=="TDirectoryFile" and h2.ClassName()=="TDirectoryFile": 
            path2=path+h.GetName()+"/"
            search_root_rec(h.GetListOfKeys(),h2.GetListOfKeys(),path2)

def cdandcheck(f, dir):
    t=f.Get(dir)
    if not t:
        print("cdandcheck to "+dir+" failed")
        exit(0)
    return t

hl=[]
hl2=[]
t=True

tree=cdandcheck(f,"DQMData")
tree=cdandcheck(tree,tree.GetListOfKeys()[0].GetName())
tree=cdandcheck(tree,"CTPPS/Run summary")

tree2=cdandcheck(f2,"DQMData")
tree2=cdandcheck(tree2,tree2.GetListOfKeys()[0].GetName())
tree2=cdandcheck(tree2,"CTPPS/Run summary")

#if len(remainder) == 4:
#    tree=cdandcheck(tree,remainder[2])
#    tree2=cdandcheck(tree2,remainder[3])

search_root_rec(tree.GetListOfKeys(),tree2.GetListOfKeys(),"/")

if t: print("The root files are identical")
elif summary:
    hl=set(hl)
    hl2=set(hl2)

    if hl!=hl2:
        print("Things present in the second file but not in the first one: ")
        out=hl2-hl
        for e in out: print(e)
    
        print("\nThings present in the first file but not in the second one: \n")
        out=hl-hl2
        for e in out: print(e)

    print("Summaries:")
    lens = []
    for col in zip(*summaries):
        lens.append(max([len(v) for v in col]))
    format = "  ".join(["{:<" + str(l) + "}" for l in lens])
    
    for summary in summaries:
        print(format.format(*summary))
    
    print("Numbers of keys in the first and second file: "+str(len(hl))+" "+str(len(hl2)))
else:
    print("The root files are different")
