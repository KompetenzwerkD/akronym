import sys
from acronym import Phrase, WordList

N_DATASET = "data/N_1M_clean.csv"
NVA_DATASET = "data/N_V_A_1M_clean.csv"


if __name__ == "__main__":
    q = sys.argv[1]

    word_list = WordList(N_DATASET)

    p = Phrase(q)
    p.find_acronyms(word_list)

    #print first 30 results
    for acronym in p.acronyms[:30]:
        print(q)

        ac_line = ""
        for char, pos in acronym:
            ac_line += ((pos)- len(ac_line)) * " " + char

        print(ac_line)
        print(acronym.word.value)
        print(" ")
        

    