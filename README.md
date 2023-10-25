# Bridging-LTLf-Inference-to-GNN-Inference-for-Learning-LTLf-Formulae
Supplement for Bridging LTLf Inference to GNN Inference for Learning LTLf Formulae

## usage
To use the solver:
First Use the following command to obtain model file

```
python code/learn_ltl_matrix.py -train_file=mindata_f15_d3/E2_0.json -test_file=mindata_f15_d3/ET2_0.json -save_model=mindata_f15_d3-2_0.model -log_file=mindata_f15_d3-2_0.log -res_file=mindata_f15_d3-2_0.txt -epoch_num=20
```

Then interpret the model file to LTL formula using
```
python code/matrix2ltl.py -train_file=mindata_f15_d3/E2_0.json -test_file=mindata_f15_d3/ET2_0.json -save_model=mindata_f15_d3-2_0.model -top_num=100
```

## dataset

### random data
This domain contains random formulae and their corresponding positive/negative traces.

To generate input files for training and testing:

```
unzip random_data.zip
python split_data.py
```



### data format

The domain folder is named as ```"domain_d%d"%(i)```, where i means the noise rate in this domain is 0.i

The training data file is named as ```E***.json```, the corresponding test data file is ```ET***.json```, such as  ```blockst10000_d0/E0_0.json``` and ```blockst10000_d0/ET0_0.json```.

Each train data file include "traces_pos", "traces_neg", "vocab", which are required by the learner. 

The file also contains "ltlftree", the target(injected) formula, and "pos_noise_mark", "neg_noise_mark", which tells whether a trace is noise or not.  This information can be used to evaluate the performance and it won't be used by the learner.


