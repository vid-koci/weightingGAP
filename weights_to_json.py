import json
weights = list(open("linear_weights_trimmed.txt",'r'))[:2001]
gap_examples = list(open("gap-test.tsv",'r'))[1:]
labelled_weights = {}
for i,ex in enumerate(gap_examples):
    truth_a=ex.strip().split("\t")[6]
    truth_b=ex.strip().split("\t")[9]
    ex_id=int(ex.strip().split("\t")[0][5:]) 
    if truth_a.lower()=="true":
        labelled_weights["test-"+str(ex_id)+"a"] = float(weights[ex_id-1].strip())
    else:
        labelled_weights["test-"+str(ex_id)+"a"] = 0.0
    if truth_b.lower()=="true":
        labelled_weights["test-"+str(ex_id)+"b"] = float(weights[ex_id-1].strip())
    else:
        labelled_weights["test-"+str(ex_id)+"b"] = 0.0
json.dump(labelled_weights,open("linear_weights_trimmed.json",'w+'))

