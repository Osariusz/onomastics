from language import Language
import name_generation

if(__name__=="__main__"):
    latin = Language(
        begin_words=[],
        end_words=["ium"],
        anywhere_words=["alexandr"],
        consonants=["b","c","d","f","g","h","l","m","n","p","r","s","t","v","x","z"],
        vowels=["a","e","i","o","u"],
        max_bordering_consonants=2,
        max_bordering_vowels=2
        
    )

    for i in range(0,10):
        print(latin.generate_word(10))