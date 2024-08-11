sentence="こんにちは。では君の名前と目的、それと現在可能なことを踏まえて自己紹介してほしい。"
memory=[["名前","フルル・リグバート"],["目的","本を読むこと"],["現在可能なこと","小説が書ける"]]
histry=[["こんにちは","こんばんは"],["やあ","どうしました？"],["失敗した","どうしたんですか？"]]
speaker="mait"
sistem="フルル"
print(histry[0][0])

hist =[
    {
        "sphist":histry[0][0],
        "sihist":histry[0][1],
    },
    {
        "sphist":histry[1][0],
        "sihist":histry[1][1],
    },
    {
        "sphist":histry[2][0],
        "sihist":histry[2][1],
    }
]

hist1 = [
    "会話履歴\n"
]
hist2=hist1+[
    f"({speaker}:{uttr['sphist']},{sistem}:{uttr['sihist']})\n" 
    for uttr in hist
]
hist3 = "<NL>".join(hist2)
print(hist3)

prompt = [{
    "speaker":speaker,
    "text":sentence+"\n",
}]
prompt1 = [
    f"{speaker}:{sentence}"
]
prompt2 = "<NL>".join(prompt1)

mem=[
    {
    "pre":memory[0][0],
    "int":memory[0][1]+"\n",
    },
    {
    "pre":memory[1][0],
    "int":memory[1][1]+"\n",
    },
    {
    "pre":memory[2][0],
    "int":memory[2][1]+"\n",
    },
]
mem1 = [
    "前提知識\n"
]
mem2=mem1+[
    f"{uttr['pre']}:{uttr['int']}" 
    for uttr in mem
]
mem3 = "<NL>".join(mem2)
print(mem3)
prompt3 = (
    "[\n"+
    hist3+
    mem3+
    "]\n<NL>"+
    prompt2+
    "\n<NL>"+
    sistem+":"
)
print(prompt3)

"""
def sen2pr(sentence):
    memory="名前=フルル・リグバート,目的=本を読むこと,現在可能なこと=小説が書ける"
    prompt = [{

        "speaker": "mait",
        "text":sentence+"\n",
    }]
    prompt1 = [
        f"{uttr['speaker']}:{uttr['text']}"
        for uttr in prompt
    ]
    prompt2 = "<NL>".join(prompt1)

    mem =[{
        "mem":"前提知識",
        "int":memory+"\n",
    }]
    mem1 = [
        f"{uttr['mem']}:{uttr['int']}" 
        for uttr in mem
    ]
    mem2 = "<NL>".join(mem1)

    prompt3 = (
        prompt2
        #+mem2
        + "<NL>"
        + "フルル:"
    )
    return prompt3"""