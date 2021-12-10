import json
import os
from copy import deepcopy
import random

def main(ifile,o_floder,ins,casenum,noise_rate=0.1,test_start_idx=500):
    if not os.path.exists(o_floder):
        os.makedirs(o_floder)
    with open(ifile,'r') as f:
        datas=json.load(f)

    for i in range(len(datas)):

        test_data=deepcopy(datas[i])
        test_data['traces_pos']=test_data['traces_pos'][test_start_idx:]
        test_data['traces_neg'] = test_data['traces_neg'][test_start_idx:]

        train_data=deepcopy(datas[i])
        train_data['traces_pos']=train_data['traces_pos'][:casenum//2]
        train_data['traces_neg'] = train_data['traces_neg'][:casenum//2]
        noise_pos = [j for j in range(len(train_data['traces_pos']) + len(train_data['traces_neg']))] # [1, 2, 3, ... ]
        random.shuffle(noise_pos) #洗牌一次
        noise_mark={noise_pos[j]:1 if j<noise_rate*len(noise_pos) else 0 for j in range(len(noise_pos))} # index->noise_mark
        new_traces_pos=[]
        new_traces_neg=[]
        train_data['pos_noise_mark']=[]
        train_data['neg_noise_mark']=[]
        for j in range(len(train_data['traces_pos'])):
            if noise_mark[j]==1: #是噪声就放反例
                new_traces_neg.append(train_data['traces_pos'][j])
                train_data['neg_noise_mark'].append(1)
            else:
                new_traces_pos.append(train_data['traces_pos'][j])
                train_data['pos_noise_mark'].append(0)
        for j in range(len(train_data['traces_neg'])):
            if noise_mark[j+len(train_data['traces_pos'])]==1: #是噪声就放正例，注意要用+len(..)
                new_traces_pos.append(train_data['traces_neg'][j])
                train_data['pos_noise_mark'].append(1)
            else:
                new_traces_neg.append(train_data['traces_neg'][j])
                train_data['neg_noise_mark'].append(0)
        train_data['traces_pos']=new_traces_pos
        train_data['traces_neg']=new_traces_neg
        print('i', i, 'tracespos', len(train_data['traces_pos']), 'neg', len(train_data['traces_neg']))
        print('finished:',o_floder+'/E%d_%d.json'%(ins,i))
        with open(o_floder+'/E%d_%d.json'%(ins,i),'w') as f:
            json.dump(train_data,f)
        with open(o_floder+'/ET%d_%d.json'%(ins,i),'w') as f:
            json.dump(test_data,f)


# ins_count={0:50,1:100,2:500,3:1000}

ins_count={2:500}  # This can be changed to generate training files containing different numbers(<=1000) of traces.
fsizes=[3,6,9,12,15]
noise_rates=[0,1,2,3,4]  # number i means there are 10i% of the traces will be noise.
for noise_rate in noise_rates:
    for fsize in fsizes:
        for key in ins_count.keys():
            main('mindata_case_100_vszie_5_fsize_%d_tsize_2000_maxlen_20.json'%fsize,'mindata_f%d_d%d'%(fsize,noise_rate),key,ins_count[key],noise_rate/10)
