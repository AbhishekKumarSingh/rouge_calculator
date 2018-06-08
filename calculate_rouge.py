import os
import pdb
import sys
import glob
import subprocess


def get_rouge_score(candidate_summ, gold_summ_dir, ngram, para):
    """
    ngram : can be '1' or '2'
    para  : can be 'R' or 'F'
    """
    output = subprocess.check_output(['java', '-cp', 'C_ROUGE7.jar', 'executiverouge.C_ROUGE7', candidate_summ, gold_summ_dir, ngram, 'A', para])
    # remove '\n' from end of output
    return output[:-1]


def main():
    gold_summ_top_dir = sys.argv[1]
    gold_summaries_dir = [ os.path.join(gold_summ_top_dir, "s" + str(i)) for i in xrange(39803)]
    candidate_summ_top_dir = sys.argv[2]
    output_file = sys.argv[3]
    ngram = sys.argv[4]
    para = sys.argv[5]

    with open(output_file, 'w') as ofile:
        for i, gold_summ_dir in enumerate(gold_summaries_dir):
            candidate_dir = os.path.join(candidate_summ_top_dir, "s" + str(i))
            candidate_summaries = glob.glob(candidate_dir + "/*")
            candidate_summaries.sort(key=lambda x: int(os.path.basename(x)[1:]))

            # calculate rouge score
            for candidate_summ in candidate_summaries:
                rscore = get_rouge_score(candidate_summ, gold_summ_dir, ngram, para)
                data = os.path.basename(gold_summ_dir) + " " + candidate_summ + " " + rscore + "\n"
                ofile.write(data)
                # pdb.set_trace()


if __name__ == '__main__':
    main()
