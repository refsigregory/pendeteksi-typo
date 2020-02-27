import re, json
from contextlib import redirect_stdout
from io import StringIO
from collections import Counter
from urllib.request import urlopen, Request
# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Test:
    def aku(self):
        print("Halo")

class Tokenize:
    def token_to_sentence(text):
        f = StringIO()
        with redirect_stdout(f):
            regex_of_sentence = re.findall('([\w\s]{0,})[^\w\s]', text)
            regex_of_sentence = [x for x in regex_of_sentence if x is not '']
            for i in regex_of_sentence:
                print(i)
            first_step_to_sentence = (f.getvalue()).split('\n')
        g = StringIO()
        with redirect_stdout(g):
            for i in first_step_to_sentence:
                try:
                    regex_to_clear_sentence = re.search('\s([\w\s]{0,})', i)
                    print(regex_to_clear_sentence.group(1))
                except:
                    print(i)
            sentence = (g.getvalue()).split('\n')
        return sentence

    def token_to_words(text):
        f = StringIO()
        with redirect_stdout(f):
            for i in text:
                regex_of_word = re.findall('([\w]{0,})', i)
                regex_of_word = [x for x in regex_of_word if x is not '']
                for word in regex_of_word:
                    print(regex_of_word)
            words = (f.getvalue()).split('\n')

    def convert_to_words(self, text):
        sentences = self.token_to_sentence(text)
        for i in sentences:
            word = self.token_to_words(i)
        return word

    def compare_list_of_words__to_another_list_of_words(from_strA, to_strB):
            fromA = list(set(from_strA))
            for word_to_match in fromA:
                totalB = len(to_strB)
                number_of_match = (to_strB).count(word_to_match)
                data = str((((to_strB).count(word_to_match))/totalB)*100)
                print('words: -- ' + word_to_match + ' --' + '\n'
                '       number of match    : ' + number_of_match + ' from ' + str(totalB) + '\n'
                '       percent of match   : ' + data + ' percent')

    def cekKata(kata):
        try:
            r = Request('http://kateglo.com/api.php?format=json&phrase=' + kata, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(r).read()
            data = json.loads(response)
            data_list = list(data.items())
            data_list = data_list[0][1]
            return data_list
        except:
            return None

# Spellchecker

class SpellCheckker(object):

    def words(self, text): return re.findall(r'\w+', text.lower())

    def __init__(self):
        self.WORDS = Counter(re.findall(r'\w+', open('katadasar.txt','r').read().lower()))

    def P(self, word, N=None):
        if N is None:
            N = sum(self.WORDS.values())
        # "Probability of `word`."
        return self.WORDS[word] / N

    def correction(self, word):
        # "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)


    def candidates(self, word):
        # "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])


    def known(self, words):
        # "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)


    def edits1(self, word):
        # "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in
                  range(len(word) + 1)]  # [('', 'kemarin'), ('k', 'emarin'), ('ke', 'marin'), dst]
        deletes = [L + R[1:] for L, R in splits if R]  # ['emarin', 'kmarin', 'kearin', dst]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]  # ['ekmarin', 'kmearin', 'keamrin', dst]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]  # ['aemarin', 'bemarin', 'cemarin', dst]
        inserts = [L + c + R for L, R in splits for c in letters]  # ['akemarin', 'bkemarin', 'ckemarin', dst]
        return set(deletes + transposes + replaces + inserts)


    def edits2(self, word):
        # "All edits that are two edits away from `word`."
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

# Stemmer
class Stemmer:
    def stem(text):
        # create stemmer
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()

        # stemming process
        #sentence = 'Perekonomian Indonesia sedang dalam pertumbuhan yang membanggakan'
        #output = stemmer.stem(sentence)

        #print(output)
        # ekonomi indonesia sedang dalam tumbuh yang bangga

        #print(stemmer.stem('Mereka meniru-nirukannya'))
        # mereka tiru

        return  stemmer.stem(text)

if __name__ == '__main__':

    # buka file
    f = open("text.txt", "r")
    s = f.read().lower()

# Proses untuk Tokenize
    tokenize = Tokenize
    #tokenize paragraph in example to sentence:
    getsentences = tokenize.token_to_sentence(s)
    # tokenize sentence to words (sentences in getsentences)
    getwords = tokenize.token_to_words(getsentences)
    # sambung sentence jadi string
    getsentences = ' '.join(getsentences)
    # pecah lagi berdasarkan spasi
    getsentences = re.findall(r'\S+', getsentences)

    # ambil jumlah setiap kata
    hasil_tokenize = list(Counter(getsentences).items())
    # urutkan berdasarkan jumlah kata
    hasil_tokenize = sorted(hasil_tokenize, key=lambda x : x[1], reverse=True)

    print(hasil_tokenize)

    for hasil in hasil_tokenize:
        kata = hasil[0].lower()
        hasil_kata = tokenize.cekKata(kata)
        if hasil_kata is not None:
            if hasil_kata['phrase_type'] is None:
                print(hasil_kata['phrase'], "digunakan ", hasil[1], "kali, ")
                print("Tidak baku, harusnya ", hasil_kata['actual_phrase'])
            else:
                print(hasil_kata['phrase'], "digunakan ", hasil[1], "kali, ")
                print("Ok")
        else:
            #print(kata, "bukan kata yang benar ")
            # Check Typo
            stemmer = Stemmer
            kata_typo = SpellCheckker().correction(kata)
            print('Koreksi : ', kata_typo)
            #Stem Kata
            kata_stem = stemmer.stem(kata_typo)
            print('Hasil stem : ', kata_stem)
            # Cek lagi
            hasil_kata = tokenize.cekKata(kata_stem)
            if hasil_kata is not None:
                if hasil_kata['phrase_type'] is None:
                    print(hasil_kata['phrase'], "digunakan ", kata, "kali, ")
                    print("Tidak ini baku, harusnya ", hasil_kata['actual_phrase'])
                else:
                    print(hasil_kata['phrase'], "adalah kata yang benar, ", kata, "digunakan ", hasil[1], "kali, ")
                    print("Ok")
            else:
                print(kata, "bukan kata yang benar, kata ini digunakan ", hasil[1], "kali, ")
        print("\n")

