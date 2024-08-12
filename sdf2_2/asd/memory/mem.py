import datetime
from asd.memory.vec_momory import save_search 
def sen2pr(sentence,speaker,sistem,resped,model):
    time=datetime.datetime.now()
    time1 = [
        "現在年月日時\n"
    ]
    time2=time1+[
        f"{time}\n"
    ]
    time3="<NL>".join(time2)
    #今回のプロンプト
    prompt = [
        {
        "speaker ":speaker,
        "text ":sentence+"\n",
        }
    ]
    prompt1=[
        "今回のプロンプト\n"
    ]
    prompt2 = prompt1+[
        f"{speaker}:{sentence}"
    ]
    prompt3 = "<NL>".join(prompt2)
    #sentence=今回のuserの発言
    resped=save_search(sentence,num=1,model,database_name="aaa",k=1)
    #前提知識呼び出し
    mem=[
        {
        "pre ":resped[0][0],
        "int ":resped[0][1]+"\n",
        },
        {
        "pre ":resped[1][0],
        "int ":resped[1][1]+"\n",
        },
        {
        "pre ":resped[2][0],
        "int ":resped[2][1]+"\n",
        },
    ]   
    mem1 = [
        "前提知識\n"
    ]
    mem2=mem1+[
        f"{uttr['pre ']}:{uttr['int ']}" 
        for uttr in mem
    ]
    mem3 = "<NL>".join(mem2)

    #関連会話呼び出し
    rela=[
        {
            "sprela ":related[0][0],
            "sirela ":related[0][1],
        },
        {
            "sprela ":related[1][0],
            "sirela ":related[1][1],
        },
        {
            "sprela ":related[2][0],
            "sirela ":related[2][1],
        }
    ]
    rela1 = [
        "関連会話\n"
    ]
    rela2=rela1+[
        f"{speaker}:{uttr['sprela ']}\n<NL>{sistem}:{uttr['sirela ']}\n" 
        for uttr in rela
    ]
    rela3 = "<NL>".join(rela2)


    prompt4 = (
        "[\n"+
        time3+
        mem3+
        "\n<NL>"+
        sistem+":"
        )
    return prompt4


if __name__=="__main__":
    sentence="こんにちは。では君の名前と目的、それと現在可能なことを踏まえて自己紹介してほしい。"
    memory=[["名前","フルル・リグバート"],
            ["目的","世界中の本を読むこと"],
            ["現在可能なこと","小説が書ける"]
            ]
    related=[["こんにちは","こんにちは！今日はいい日ですね。"],
            ["やあ","どうしました？"],
            ["そうだな","どうしたんですか？"]
            ]
    speaker="mait"
    sistem="フルル"
    prompt=sen2pr(sentence,memory,related,speaker,sistem).strip()
    print(prompt)