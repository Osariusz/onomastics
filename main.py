from language import Language
import name_generation

if(__name__=="__main__"):
    latin = Language(
        begin_words=[],
        end_words=["ium","ia","um","is"],
        anywhere_words=["alexandr","ae","gt","nd","uiu"],
        consonants=["b","c","d","f","g","h","l","m","n","p","r","s","t","v","z"],
        vowels=["a","e","i","o","u"],
        max_bordering_consonants=1,
        max_bordering_vowels=1
        
    )

    polish = Language(
        begin_words = [],
        end_words = ["owo","in","ce"],
        anywhere_words = ["baran","mazur","ostr"],

        consonants = ["b","c","d","f","g","h","j","k","l","m","n","p","r","s","t","w","z"],
        vowels = ["a","e","i","o","u","y"],
        
        max_bordering_consonants = 1,
        allowed_bordering_consonants = [],

        max_bordering_vowels = 1,
        allowed_bordering_vowels = []

    )

    for i in range(0,10):
        print(polish.generate_word(10))