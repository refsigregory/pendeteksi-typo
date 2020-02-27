import re, json
from contextlib import redirect_stdout
from io import StringIO
from urllib.request import urlopen, Request
# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

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