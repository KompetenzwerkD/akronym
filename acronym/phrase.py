import re
import pandas as pd
from dataclasses import dataclass
from .wordlist import WordListEntry

class Phrase: 

    def __init__(self, s):
        self.s = s
        self.std = s.lower()
        self.tokens = self.std.split()        
        self.word_pos = [ x.span()[1] for x in re.finditer(" ", s)]
        self.acronyms = []


    def find_acronyms(self, word_list):

        last_word_pos = self.word_pos[-1]
        
        for word_list_entry in word_list:
            word = word_list_entry.std()

            positions = []
            acronym_found = True

            # search first character in the first word and
            # search last character in the last word
            first_pos = self.tokens[0].find(word[0])
            last_pos = self.tokens[-1].find(word[-1])      

            # only continue if first character is in the first word and last character
            # is in the last word
            if first_pos > -1 and last_pos > -1:
                positions.append(first_pos)

                # define new search substring
                offset = first_pos + 1
                rest = self.std[offset: last_word_pos + last_pos]

                # now search for the rest of the characters within the remaining search substring
                # and ajust the substring accordingly if found. if a character is not found the
                # acronym is not possible
                for c in word[1:-1]:
                    c_pos = rest.find(c)
                    positions.append(offset+c_pos)
                    if c_pos > -1:
                        offset +=  c_pos + 1
                        rest =  rest[c_pos + 1:]
                    else:
                        acronym_found = False
                        break

                positions.append(last_word_pos + last_pos)
                    
            else:
                acronym_found = False

            if acronym_found:
                score = self._calculate_score(word_list_entry, positions)
                self.acronyms.append(Acronym(word_list_entry, positions, score))

        #sort by highest score
        self.acronyms = sorted(self.acronyms, key=lambda x: -x.score)


    def _calculate_score(self, word_list_entry, positions):
        """
        todo
        """

        first_letter_bonus = 0
        for position in positions:
            if position in self.word_pos:
                first_letter_bonus += 1

        first_letter_bonus = first_letter_bonus / len(self.tokens) * 15

        return float(len(word_list_entry) * 0.5 + (word_list_entry.freq_ratio * 15)) + first_letter_bonus


@dataclass
class Acronym:
    word: WordListEntry
    positions: list
    score: float 

    def __iter__(self):
        for char, pos in zip(self.word.value, self.positions):
            yield char, pos
