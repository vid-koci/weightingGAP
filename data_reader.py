import os
from tqdm import trange,tqdm
import gap_utils

class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, candidate_a, candidate_b, ex_true=True):
        """Constructs a InputExample.

        Args:
            guid: Unique id for the example.
            text_a: string. Sentence analysed with pronoun replaced for _
            candidate_a: string, correct candidate
            candidate_b: string, incorrect candidate
        """
        self.guid = guid
        self.text_a = text_a
        self.candidate_a = candidate_a
        self.candidate_b = candidate_b #only used for train
        self.ex_true = ex_true
        #ex_true only matters for testing and has following string values:
        #"true" - LM has to pick this over others,
        #"false" - LM should not pick this over others
        #"other" - not known, not important, this is "other" candidate
        #"err_true" - Correct candidate but Spacy failed to find it. Automatically wrong
        #"err_false" - Incorrect candidate but Spacy failed to find it. Automatically correct

class DataProcessor(object):
    """Processor for the Wiki data set."""

    def gap_train(self, source):
        examples=[]
        for line in tqdm(list(open(source,'r'))[1:],desc="Reading and pre-processing data"):
            tokens = line.strip().split('\t')
            guid = tokens[0]
            sentence = tokens[1]
            pronoun = tokens[2]
            pronoun_offset = int(tokens[3])
            sentence = sentence[:pronoun_offset]+"_"+sentence[pronoun_offset+len(pronoun):]
            candidate_a = tokens[4]
            candidate_b = tokens[7]
            if tokens[6].lower()=="true":
                examples.append(InputExample(guid,sentence,candidate_a,candidate_b))
            if tokens[9].lower()=="true":
                examples.append(InputExample(guid,sentence,candidate_b,candidate_a))
        return examples

    def gap_test(self,source):
        examples=[]
        for line in tqdm(list(open(source,'r'))[1:],desc="Reading and pre-processing data"):
            tokens = line.strip().split('\t')
            guid = tokens[0]
            sentence = tokens[1]
            pronoun = tokens[2]
            pronoun_offset = int(tokens[3])
            sentence = sentence[:pronoun_offset]+"_"+sentence[pronoun_offset+len(pronoun):]
            candidate_a = tokens[4]
            candidate_b = tokens[7]
            other_candidates = gap_utils.get_candidates(sentence)
            if pronoun.casefold() == "his":#due to the abiguity of English language, the same cannot be done for "her"
                candidate_a = candidate_a+"\'s"
                candidate_b = candidate_b+"\'s"
                for i in range(len(other_candidates)):
                    other_candidates[i]= other_candidates[i]+"\'s"
            if candidate_a.casefold() in [cand.casefold() for cand in other_candidates]:#candidate_a was detected by NER
                examples.append(InputExample(guid+"A",sentence,candidate_a,None,ex_true = tokens[6].lower()))
                for other in list(filter(lambda a: a.casefold()!= candidate_a.casefold(), other_candidates)):
                    examples.append(InputExample(guid+"A",sentence,other,None,ex_true = "other"))
            else:
                examples.append(InputExample(guid+"A",sentence,candidate_a,None,ex_true = "err_"+tokens[6].lower()))
            if candidate_b.casefold() in [cand.casefold() for cand in other_candidates]:
                examples.append(InputExample(guid+"B",sentence,candidate_b,None,ex_true = tokens[9].lower()))
                for other in list(filter(lambda a: a.casefold()!= candidate_b.casefold(), other_candidates)):
                    examples.append(InputExample(guid+"B",sentence,other,None,ex_true = "other"))
            else:
                examples.append(InputExample(guid+"B",sentence,candidate_b,None,ex_true = "err_"+tokens[9].lower()))
        return examples


    def get_examples(self, data_dir, set_name):#works for differently for train!
        """See base class."""
        file_names = {
                "gap-train": "gap-development.tsv",
                "gap-dev": "gap-validation.tsv",
                "gap-test": "gap-test.tsv",
               }
        source = os.path.join(data_dir,file_names[set_name])
        if set_name == "gap-train":
            return self.gap_train(source)
        elif set_name in ["gap-dev","gap-test"]:
            return self.gap_test(source)
        else:
            print("Unknown set_name: ",set_name)
