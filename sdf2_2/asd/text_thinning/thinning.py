def thin0(sentence):
    if sentence=="おやすみ":
        sdf=2
    else:
        sdf=0
    return sdf

def thin1(sentence):
    if sentence in "ご視聴ありがとうございました":
        asd=1
        sentence1=open("data/mutter/mutter1.txt", "r", encoding="utf-8").read()
    elif sentence in "見てくれてありがとう":
        asd=1
        sentence1=open("data/mutter/mutter2.txt", "r", encoding="utf-8").read()
    elif sentence in "ありがとうございました":
        asd=1
        sentence1=open("data/mutter/mutter1.txt", "r", encoding="utf-8").read()
    elif sentence in "ご紹介させていただきありがとうございます":
        asd=1
        sentence1=open("data/mutter/mutter1.txt", "r", encoding="utf-8").read()
    elif sentence in "大阪市立大阪市":
        asd=1
        sentence1=open("data/mutter/mutter1.txt", "r", encoding="utf-8").read()
    else:
        asd=0
        sentence1=sentence
    return sentence1,asd

def thin2(output):
    resp = output.replace("<NL>","")
    resp = resp.replace("</s>","")
    resp = resp.replace("フルル:","")
    resp = resp.replace("mait","マイト")
    return resp

if __name__ == "__main__":
    sentence="ご視聴ありがとうございました"
    sentence1,asd=thin1(sentence)
    print(sentence1,"\n",asd)
