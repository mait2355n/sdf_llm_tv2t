def cur(histry):
    for i in range(10):
        with open("data/current_mem_data/current_mem_data_"+str(i)+"0.txt",encoding="utf-8") as txt0:
            histry[i][0]=txt0.read()
        with open("data/current_mem_data/current_mem_data_"+str(i)+"1.txt",encoding="utf-8") as txt1:
            histry[i][1]=txt1.read()
    return histry

#今回分を保存し、n回前の会話を削除
def cur_w(histry,prompt,resp):
    n=10
    for i in range(n):
        with open("data/current_mem_data/current_mem_data_"+str(i)+"0.txt",mode="w",encoding="utf-8") as txt0:
            if i==9:
                txt0.write(prompt)
            else:
                txt0.write(histry[i+1][0])
        with open("data/current_mem_data/current_mem_data_"+str(i)+"1.txt",mode="w",encoding="utf-8") as txt1:
            if i==9:
                txt1.write(resp)
            else:
                txt1.write(histry[i+1][1])
    return

if __name__ == "__main__":
    hist=cur()
    print(hist)