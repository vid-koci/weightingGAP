#Compute weights for GAP test examples
import json

matlab_file = open("linprog_compute_trimmed_weights.m",'w')

gap_examples = list(open("gap-test.tsv",'r'))[1:]
name_spans = json.load(open("gap-test-name-spans.json","r"))

males,females = [],[]
# ids that should be left out either because both negative or because they have too many names/too many words between the pronoun and the answer
# set ignored_ids to an empty list if you do not want a trimmed dataset, negative examples are removed anyway
ignored_ids = json.load(open("ignored_ids_only_by_n_names.json"))
for ex in gap_examples:
    pronoun=ex.strip().split("\t")[2]
    ex_id=int(ex.strip().split("\t")[0][5:]) 
    if pronoun.lower() in ["she","her","hers"]:
        females.append(ex_id)
    else:
        males.append(ex_id)
n_variables = len(males)+len(females)+(len(males)-1)*len(males)//2+(len(females)-1)*len(females)//2#weight for each 
equalities = []#list of pairs of lists indices, such that sum of variables at indices in left list is equal to sum of variables at indices in right list
inequalities = []#same as above except that contents of first list are greater or equal than contents of the second list

#non-negativity constraints
matlab_file.write("lb = spalloc("+str(n_variables)+",1,1);\n")
matlab_file.write("ub = [];\n")

equalities.append((males+females,[]))#sum of all weights is equal to n ("n" will be added to beq vector in the last part of the code)

#Sum of all masculine weights should equal to sum of all feminine weights
equalities.append((males,females))

#Sum of all negative and ignored examples should equal 0  
neg_row = []
for ex in gap_examples:
    truth_a=ex.strip().split("\t")[6]
    truth_b=ex.strip().split("\t")[9]
    ex_id=int(ex.strip().split("\t")[0][5:]) 
    if truth_a.lower()=="false" and truth_b.lower()=="false" or str(ex_id) in ignored_ids:
        neg_row.append(ex_id)
equalities.append((neg_row,[]))

#Subsets of examples with equal number of personal names in the sentence should weight equally
n_names_bins_m_pos = [[] for i in range(50)]#there are never more than 50 names per sentence
n_names_bins_f_pos = [[] for i in range(50)]
for ex in gap_examples:
    pronoun = ex.strip().split("\t")[2]
    ex_id = ex.strip().split("\t")[0]
    if ex.strip().split("\t")[6].lower()=="false" and ex.strip().split("\t")[9].lower()=="false":
        continue
    n_names = len(name_spans[ex_id])
    if int(ex_id[5:]) in males:
        n_names_bins_m_pos[n_names].append(ex_id[5:])
    else:
        n_names_bins_f_pos[n_names].append(ex_id[5:])

for n_names in range(50):
    if len(n_names_bins_m_pos[n_names])+len(n_names_bins_f_pos[n_names])>0:
        equalities.append((n_names_bins_m_pos[n_names],n_names_bins_f_pos[n_names]))

#subsets of examples where the correct candidate is i-th closest name (for some i) should weight equally
m_dist_bins_pos = [[] for _ in range(50)]#never more than 50 names per sentence
f_dist_bins_pos = [[] for _ in range(50)]
import spacy
nlp = spacy.load("en_core_web_sm")

def compare(span_a, span_b):
    if span_a[0]>span_b[1]:
        return False
    if span_a[1]<span_b[0]:
        return False
    return True

for l in gap_examples:
    ex_id,text,pronoun,p_off,a_text,a_off,a_truth,b_text,b_off,b_truth,_=l.strip().split("\t")
    candidates = name_spans[ex_id]
    candidates.sort(key=lambda candidate : len(nlp( \
        text[candidate[1]:int(p_off)].strip().lstrip() \
        if candidate[1]< int(p_off) \
        else text[int(p_off)+len(pronoun):candidate[0]].strip().lstrip() \
        ,disable=['parser','tagger','ner'])))
    position=-1
    for i,cand in enumerate(candidates):
        if compare(cand,(int(a_off),int(a_off)+len(a_text))):
            position=i+1
            break
    if position != -1:
        if pronoun.lower() in ["she","her","hers"]:
            if a_truth.lower() == "true":
                f_dist_bins_pos[position].append(ex_id[5:])
        elif pronoun.lower() in ["he","his","him"]:
            if a_truth.lower() == "true":
                m_dist_bins_pos[position].append(ex_id[5:])
    position=-1
    for i,cand in enumerate(candidates):
        if compare(cand,(int(b_off),int(b_off)+len(b_text))):
            position=i+1
            break
    if position != -1:
        if pronoun.lower() in ["she","her","hers"]:
            if b_truth.lower() == "true":
                f_dist_bins_pos[position].append(ex_id[5:])
        elif pronoun.lower() in ["he","his","him"]:
            if b_truth.lower() == "true":
                m_dist_bins_pos[position].append(ex_id[5:])

for dist in range(50):
    if len(m_dist_bins_pos[dist])+len(f_dist_bins_pos[dist])>0:
        equalities.append((m_dist_bins_pos[dist],f_dist_bins_pos[dist]))


#auxiliary variables and their inequalities
curr_aux_var = len(males)+len(females)+1
for i in range(len(males)):
    for j in range(i):
        inequalities.append(([curr_aux_var],[males[i]]))
        inequalities.append(([curr_aux_var],[males[j]]))
        curr_aux_var+=1
for i in range(len(females)):
    for j in range(i):
        inequalities.append(([curr_aux_var],[females[i]]))
        inequalities.append(([curr_aux_var],[females[j]]))
        curr_aux_var+=1

ignored_ids = list(set(ignored_ids))#remove duplicates
matlab_file.write(f"A = spalloc({len(inequalities)},{n_variables},{len(inequalities)*2});\n")
matlab_file.write(f"b = spalloc({len(inequalities)},1,1);\n")
for i,(lhs,rhs) in enumerate(inequalities):
    for ind in lhs:
        matlab_file.write(f"A({i+1},{ind})=-1;\n")
    for ind in rhs:
        matlab_file.write(f"A({i+1},{ind})=1;\n")

matlab_file.write(f"Aeq = spalloc({len(equalities)},{n_variables},{sum(len(lhs)+len(rhs) for lhs,rhs in equalities)});\n")
matlab_file.write(f"beq = spalloc({len(equalities)},1,1);\n")
matlab_file.write(f"beq(1) = {len(males)+len(females)-len(neg_row)};\n") #the first equality was sum(all weights) = number of non-zero weights; the only equality with a non-zero sum
for i,(lhs,rhs) in enumerate(equalities):
    for ind in lhs:
        matlab_file.write(f"Aeq({i+1},{ind})=1;\n")
    for ind in rhs:
        matlab_file.write(f"Aeq({i+1},{ind})=-1;\n")

matlab_file.write("f = ["+",".join(["0" if i<len(males)+len(females) else "1" for i in range(n_variables) ])+"];\n")
matlab_file.write("options = optimoptions('linprog','Display','iter','Algorithm','interior-point','MaxIter',1000000,'OptimalityTolerance',1e-4);\n")
matlab_file.write("[x,obj,info,lambda] = linprog(f,A,b,Aeq,beq,lb,ub,options);\n")
matlab_file.write("round(x .* 10000) ./ 10000;\ninfo\n")
matlab_file.write("save linear_weights_trimmed.txt x -ascii;\n")
matlab_file.close()

