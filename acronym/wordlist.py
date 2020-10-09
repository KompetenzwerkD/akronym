import re
import csv
import pandas as pd
from dataclasses import dataclass

class WordList:
    """
    Class representing a word list, a csv containing a "Word" and a "Freq" column.
    Words with less than 3 characters are excluded.
    """

    def __init__(self, filepath, sep=",", n=300000):

        self._list = []
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            max_freq = 0
            for i, row in enumerate(reader):
                word = row[0]
                freq = float(row[1])

                if len(word) >= 3:
                    self._list.append(WordListEntry(word, freq))

                    if freq > max_freq:
                        max_freq = freq

        for elem in self._list:
            elem.freq_ratio = elem.freq/max_freq

        
    def __iter__(self):
        for elem in self._list:
            yield elem



class WordListEntry:

    def __init__(self, value, freq):
        self.value = value
        self.freq = freq
        self.freq_ratio = 0

    def __len__(self):
        return len(self.value)

    def std(self):
        return self.value.lower()