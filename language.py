from decimal import ConversionSyntax
from math import ceil
from multiprocessing import allow_connection_pickling
from operator import length_hint
from tokenize import group
import numpy

class Language:
    begin_words = ["ostr"]
    end_words = ["owo","owszczyzna", "wszczyzna"]
    anywhere_words = ["baran","mazur"]

    consonants = ["b","c","d","f","g","h","j","k","l","m","n","p","r","s","t","w","x","z"]
    vowels = ["a","e","i","o","u","y"]
    
    max_bordering_consonants = 2
    allowed_bordering_consonants = []

    max_bordering_vowels = 1
    allowed_bordering_vowels = []


    def __init__(self, begin_words=[], end_words=[], anywhere_words=[], consonants=[], vowels=[], max_bordering_consonants=2, allowed_bordering_consonants=[], max_bordering_vowels=1, allowed_bordering_vowels=[]):
        self.begin_words = begin_words
        self.end_words = end_words
        self.anywhere_words = anywhere_words
        self.consonants = consonants
        self.vowels = vowels
        self.max_bordering_consonants = max_bordering_consonants
        self.allowed_bordering_consonants = max_bordering_consonants
        self.max_bordering_vowels = max_bordering_vowels
        self.allowed_bordering_vowels = allowed_bordering_vowels

    def random_letters(self, length):
        result = ""
        letters = self.consonants+self.vowels
        generated = numpy.random.choice(letters,length)
        for letter in generated:
            result += letter
        return result

    def random_consonants(self, length):
        result = ""
        generated = numpy.random.choice(self.consonants,length)
        for letter in generated:
            result += letter
        return result

    def random_vowels(self, length):
        result = ""
        generated = numpy.random.choice(self.vowels,length)
        for letter in generated:
            result += letter
        return result
    def consonant_segment(self, max_length):
        consonant_length = numpy.random.random_integers(1, min(max_length, self.max_bordering_consonants))
        generated = self.random_consonants(consonant_length)
        return generated
    
    def vowel_segment(self, max_length):
        vowel_length = numpy.random.random_integers(1, min(max_length, self.max_bordering_vowels))
        generated = self.random_vowels(vowel_length)
        return generated

    def word_last_letter_consonant(self, word):
        if(len(word)<=0):
            return numpy.random.random_integers(0,1)
        if(word[-1] in self.consonants):
            return True
        return False
    def word_first_letter_consonant(self, word):
        if(len(word)<=0):
            return numpy.random.random_integers(0,1)
        if(word[0] in self.consonants):
            return True
        return False

    def segment_group_length(self, segment_group):
        length = 0
        for segment in segment_group:
            length += len(segment)
        return length

    def word_start_segment(self, max_length):
        segments = []
        for word in self.begin_words:
            if(len(word) < max_length):
                segments.append(word)
        if(len(segments)<=0):
            return ""
        return numpy.random.choice(segments)

    def start_segment(self, max_length):
        segment_chance = 0.4
        if(numpy.random.uniform()<=segment_chance):
            return self.word_start_segment(max_length)
        else:
            return ""

    def word_anywhere_segment(self, max_length, consonant_first):
        segments = []
        for word in self.anywhere_words:
            if(len(word) < max_length):
                if((word[0] in self.consonants) == consonant_first):
                    segments.append(word)
        if(len(segments)<=0):
            return self.generate_random_word(max_length, consonant_first)
        return numpy.random.choice(segments)

    def end_word_fits_segment(self, max_length, word, consonant_first):
        return len(word)<max_length or (len(word)==max_length and (consonant_first == self.word_first_letter_consonant(word)))

    def generate_partial_segment_front(self, max_length, consonant_first):

        segment_usage_chance = 0.3

        result = ""
        length_left = max_length
        consonant_before = True
        if(consonant_first):
            consonant_before = False
        while(length_left>0):
            if(numpy.random.uniform()<=segment_usage_chance):
                fitting_words = []
                for word in self.anywhere_words:
                    if(len(word)<=length_left and self.word_first_letter_consonant(word) == consonant_before and not word in result):
                        fitting_words.append(word)
                if(len(fitting_words)>0):
                    result += numpy.random.choice(fitting_words)
                    length_left = max_length-len(result)
                    consonant_before = not self.word_last_letter_consonant(result)
                    continue
            if(consonant_before):
                result += self.consonant_segment(length_left)
            else:
                result += self.vowel_segment(length_left)
            length_left = max_length-len(result)
            consonant_before = not self.word_last_letter_consonant(result)
        return result

    def fitting_segment(self, max_length,consonant_first):
        segment_chance = 0.7

        if(numpy.random.uniform()<=segment_chance):
            fitting_end_words = []
            for word in self.end_words:
                if(self.end_word_fits_segment(max_length,word,consonant_first)):
                    if(len(word)==max_length):
                        return word
                    else:
                        fitting_end_words.append(word)

            if(len(fitting_end_words)==0):
                return self.generate_partial_segment_front(max_length,consonant_first)
            fitting_end_word = numpy.random.choice(fitting_end_words)

            liner = self.generate_partial_segment_front(max_length-len(fitting_end_word),consonant_first)
            if(self.end_word_fits_segment(max_length-len(liner),fitting_end_word,not self.word_last_letter_consonant(liner))):
                return liner+fitting_end_word
            else:
                return self.generate_partial_segment_front(max_length, consonant_first)

        else:  
            return self.generate_partial_segment_front(max_length,consonant_first)


        


    def generate_word(self, max_length):
        result = ""
        segment_group = self.generate_segment_group(max_length)
        for segment in segment_group:
            result += segment
        return result

    def generate_segment_group(self, max_length):
        if(max_length<=self.max_bordering_consonants):
            return [self.random_consonants(max_length)]
        if(max_length<=self.max_bordering_vowels):
            return [self.random_vowels(max_length)]
        segment_group = []
        group_length = 0
        space_left = max_length-group_length



        start_segment = self.start_segment(space_left)
        segment_group.append(start_segment)

        group_length = self.segment_group_length(segment_group)



        last_consonant = self.word_last_letter_consonant(start_segment)
        while(group_length<max_length):
            space_left = max_length-group_length
            word_added = self.fitting_segment(space_left,last_consonant)
            segment_group.append(word_added)
            group_length = self.segment_group_length(segment_group)
            last_consonant = self.word_last_letter_consonant(word_added)

        return segment_group






