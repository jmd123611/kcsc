import heapq
from numpy import random as rd
import numpy as np
import scipy.stats as stats
import collections
import time
import random
import copy

data=[['4','2','3','1','1','5'],['1','0','4','2','3'],['4','2','3','5','5','5'],['1','0','4','0','2','3'],['1','1','0','4','1'],['4','2','3','5','1','5'],['1','0','4','0','0','3']]
'''file_path=''
with open(file_path) as file_object:
    for line in file_object:
        line=line.replace('\n','')
        data.append(line.split(' '))'''
k=2
alpha=0.005
'''thre=len(max(data, key=len))
print("最长的序列长度：",thre)'''
'''def true_label():
    file_path1=''
    true_labels=[]
    file=open(file_path1)
    for line in file:
        data=line.split(' ')
        true_labels.append((data[0]))
    return true_labels'''
def purity(cluster, label):
    cluster = np.array(cluster)
    label = np. array(label)
    indedata1 = {}
    for p in np.unique(label):
        indedata1[p] = np.argwhere(label == p)
    indedata2 = {}
    for q in np.unique(cluster):
        indedata2[q] = np.argwhere(cluster == q)

    count_all = []
    for i in indedata1.values():
        count = []
        for j in indedata2.values():
            a = np.intersect1d(i, j).shape[0]
            count.append(a)
        count_all.append(count)
    return sum(np.max(count_all, axis=0))/len(cluster)
def minDistance(word1, word2) :
    '''if len(word1) == 0:
        return len(word2)
    elif len(word2) == 0:
        return len(word1)'''
    M = len(word1)
    N = len(word2)
    output = [[0] * (N + 1) for _ in range(M + 1)]
    for i in range(M + 1):
        for j in range(N + 1):
            if i == 0 and j == 0:
                output[i][j] = 0
            elif i == 0 and j != 0:
                output[i][j] = j
            elif i != 0 and j == 0:
                output[i][j] = i
            elif word1[i - 1] == word2[j - 1]:
                output[i][j] = output[i - 1][j - 1]
            else:
                output[i][j] = min(output[i - 1][j - 1] + 1, output[i - 1][j] + 1, output[i][j - 1] + 1)
    return output,output[i][j]

def backtrackingPath(word1,word2):
    dp,nu = minDistance(word1,word2)
    m = len(dp)-1
    n = len(dp[0])-1
    edit_distance=dp[m][n]
    operation = []

    while n>0 or m>0:
        if n and dp[m][n-1]+1 == dp[m][n]:
            operation.append("ins:"+word2[n-1])
            n -= 1
            continue
        if m and dp[m-1][n]+1 == dp[m][n]:
            operation.append(word1[m-1]+":del")
            m -= 1
            continue
        if dp[m-1][n-1]+1 == dp[m][n]:
            operation.append(word1[m - 1] + ":"+word2[n-1])
            n -= 1
            m -= 1
            continue
        if dp[m-1][n-1] == dp[m][n]:
            operation.append(word1[m-1])
        n -= 1
        m -= 1
    operation = operation[::-1]
    return operation,edit_distance
time_start = time.time()
len_data=len(data)
fl=1
max_len=len(max(data, key=len))
seed=random.sample(range(len_data),1)

#print(seed)


dis_matrix=[[max_len for col in range(k-1)] for row in range(len_data)]
for i in range(k-1):   #第i个种子选取
    min_dis=[]
    for j in range(len_data):   #对每个点
        no,distance02=minDistance(data[j],data[seed[i]])
        dis_matrix[j][i]=distance02
    #print(dis_matrix)
    for j in range(len_data):
        min_dis.append(min(dis_matrix[j]))
        m2 = list(map(lambda x: x ** 2, min_dis))
    #print(min_dis)
    p = m2 / np.sum(m2)
    #print(p)
    cum_p = np.cumsum(p)
    #print(cum_p)
    rand_num = rd.random()
    select_index = list(rand_num > cum_p).index(False)
    #print(rand_num, select_index)
    #select_index=min_dis.index(max(min_dis))
    #print(select_index)
    seed.append(select_index)

seed.sort()
seed=[0,2]
print("seed:",seed)
'''while fl==1:
    seeddistance = []
    seed=random.sample(range(len_data),k)
    print(seed)
    for i in range(0,k-1):
        for j in range(i+1,k):
            aa,seed_distance=minDistance(data[seed[i]],data[seed[j]])
            seeddistance.append(seed_distance)
    if min(seeddistance)>=thre/2:
        fl=0
    else:
        print("重新选")
print("seed:",seed)'''


#seed=[11,20]


def updata_medstring(string,cluster):
    ope_index=0
    position=0
    len_cluster = len(cluster)
    medianString = copy.deepcopy(string)  # 初始串的选取
    ope = []

    for i in range(len_cluster):
        opera, sim = backtrackingPath(medianString, cluster[i])
        ope.append(opera)
    len_ope=len(ope)
        # 所有出现过的操作sequence
    all_ope = []
    for i in range(len_ope):
        for j in range(len(ope[i])):
            if ":" in ope[i][j] and ope[i][j] not in all_ope:
                all_ope.append(ope[i][j])
    #print("所有出现过的操作统计完毕！:",all_ope)
    #time2=time.time()
    #print("统计所有的操作所耗时间:",time2-time1)



    len_all_ope=len(all_ope)
    #print("所有出现过的操作个数:", all_ope)
    # 统计操作的次数，位置
    #time3 = time.time()
    sta = [[0 for col in range(len(medianString) + 1)] for row in range(len_all_ope)]
    # 所有操作逐个统计
    for i in range(len_all_ope):
        for j in range(len_ope):
            symbol=0
            for z in range(len(ope[j])):
                pos = 0
                if ":" not in ope[j][z]:
                    symbol = 0
                if all_ope[i] == ope[j][z] and symbol==0:
                    for x in range(z):
                        if 'ins' not in ope[j][x]:
                            pos = pos + 1
                        #print(all_ope[i],ope[j],pos)
                        #print(sta)
                    #print(i,pos)
                    sta[i][pos] = sta[i][pos] + 1
                    symbol=1
        #time4 = time.time()
        #print("计算sta矩阵所耗时间:",time4-time3)
        #print("矩阵计算完毕!")
        #time5 = time.time()
    #print("ope:",all_ope)
    #print("sta:",sta)
    most_frequent = 0


    for i in range(len_all_ope):
        for j in range(len(medianString) + 1):
            if (sta[i][j] >= most_frequent):
                ope_index = i
                position = j
                most_frequent=sta[i][j]
    #print("mostfrequent：", most_frequent)
    #print("操作索引及位置：",ope_index,position)
    if 'ins' in all_ope[ope_index]:
        obj = all_ope[ope_index].split(':')
        #print("插入元素及位置:", obj[1], position)
        medianString.insert(position, obj[1])
        #print("替换后medianstring:", medianString)
    elif 'del' in all_ope[ope_index]:
        obj = all_ope[ope_index].split(':')

        #print("删除元素及位置:", obj[0], position)
        del medianString[position]
        #print("替换后medianstring:", medianString)
    else:
        obj = all_ope[ope_index].split(':')
        #print("执行替换操作及位置:", obj, position)
        medianString[position] = obj[1]
        #print("替换后medianstring:", medianString)
    return medianString



#主程序
#初始化：
neibour_num=[0 for i in range(k)]
string_sumdis=[0 for i in range(k)]
D_N=[0 for i in range(k)]
ini_obj=0
label = [0 for i in range(len_data)]
for i in range(len_data):
    distance = []

    for j in range(k):
        xx, dis = minDistance(data[i], data[seed[j]])  # 每个sequence和每个medianstring计算相似度
        distance.append(dis)
    #print("distance",distance)
    min_dis=min(distance)
    label[i] = distance.index(min_dis)
    neibour_num[label[i]]=neibour_num[label[i]]+1
    string_sumdis[label[i]]=string_sumdis[label[i]]+min_dis
    ini_obj=ini_obj+min_dis
#print("初始标签:",label)
print("初始目标函数值:",ini_obj)
#print("邻居数:",neibour_num)
#print("距离和:",string_sumdis)
#print("初始purity：",purity(label,true_label()))
#for i in range(k):
    #D_N[i] = string_sumdis[i] / neibour_num[i]
for i in range(k):
    if neibour_num[i]==0:
        neibour_num[i]=1
D_N=[a/b for a,b in zip(string_sumdis,neibour_num)]
#print("D/N:",D_N)
#循环部分
medianstring=[]#初始的中心
for i in range(k):
    medianstring.append(data[seed[i]])
new_obj=0
old_obj=ini_obj
flag=1
new_medianstring=copy.deepcopy(medianstring)
new_label = copy.deepcopy(label)
new_D_N=copy.deepcopy(D_N)
ite_num=0
red=1
while flag==1 and   (red>alpha or ite_num<=10):
    ite_num=ite_num+1

    print("迭代次数:",ite_num)

    ite=0
    flag2 = 1
    while flag2==1:
        neibour_num = [0 for i in range(k)]
        string_sumdis = [0 for i in range(k)]
        new_obj=0
        chosen_string_index=D_N.index(max(D_N))
        #print("D/N:",D_N)
        #print("中心集合:",medianstring)
        #print("所选取要更新的中心:",medianstring[chosen_string_index])
        D_N[chosen_string_index]=0
        #print("D/N:", D_N)
        cluster=[]
        for i in range(len_data):
            if label[i]==chosen_string_index:
                cluster.append(data[i])
        #print("选中cluster:",cluster)
        #print("len_c",len(cluster))
        #print("更改之前的串:", medianstring[chosen_string_index])
        new_medianstring[chosen_string_index]=updata_medstring(medianstring[chosen_string_index],cluster)
        print("更改之前:",medianstring[chosen_string_index])
        print("更改之后:",new_medianstring[chosen_string_index])
        for i in range(len_data):
            distance = []
            for j in range(k):
                xx, dis = minDistance(data[i], new_medianstring[j])  # 每个sequence和每个medianstring计算相似度
                distance.append(dis)
            #print("distance",distance)
            min_dis = min(distance)
            new_label[i] = distance.index(min_dis)
            neibour_num[new_label[i]] = neibour_num[new_label[i]] + 1
            string_sumdis[new_label[i]] = string_sumdis[new_label[i]] + min_dis
            new_obj = new_obj + min_dis
        print("新的目标函数：",new_obj)
        print("旧的目标函数：",old_obj)
        #for i in range(k):
            #new_D_N[i]=string_sumdis[new_label[i]]/neibour_num[new_label[i]]
            #print(new_D_N[i])
        for i in range(k):
            if neibour_num[i] == 0:
                neibour_num[i] = 1
        new_D_N=[a/b for a,b in zip(string_sumdis,neibour_num)]
        if new_obj<old_obj:
            reduce=old_obj-new_obj
            red=reduce/ini_obj
            print("减少的目标函数比例：",reduce, red)
            old_obj=new_obj
            medianstring=new_medianstring.copy()
            label=new_label.copy()
            D_N=new_D_N.copy()
            D_N[chosen_string_index]=max(D_N)+1
            flag2=0
            #print("当前串更新成功,索引为:",chosen_string_index)
            print("更新后label:",label)
            #print("purity:",purity(label,true_label()))
        else:
            ite = ite + 1
            print("当前串更新失败，尝试下一个中心索引为:", ite)
        if ite == k:
            flag2 = 0
            flag = 0
            print("所有串更新失败，结束！")
            #print("迭代次数", ite_num)
print(label)




#print(purity(label,true_label()))
time_end = time.time()
time_c= time_end - time_start   #运行所花时间
print('time cost', time_c, 's')