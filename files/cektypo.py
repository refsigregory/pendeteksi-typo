import re
import json
from collections import Counter
from urllib.request import urlopen, Request
import csv


def words(text): return re.findall(r'\w+', text.lower())


WORDS =WORDS = Counter(words(open('katadasar.txt','r').read()))

print(WORDS)


def P(word, N=sum(WORDS.values())):
    # "Probability of `word`."
    return WORDS[word] / N


def correction(word):
    # "Most probable spelling correction for word."
    #return max(candidates(word), key=P)
    return candidates(word)


def candidates(word):
    # "Generate possible spelling corrections for word."
    #return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
    word = cekKata(word)
    return(cekKata([word]) or cekKata(edits1(word)) or cekKata(edits2(word)) or [word])

def known(words):
    # "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    # "All edits that are one edit away from `word`."
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in
              range(len(word) + 1)]  # [('', 'kemarin'), ('k', 'emarin'), ('ke', 'marin'), dst]
    deletes = [L + R[1:] for L, R in splits if R]  # ['emarin', 'kmarin', 'kearin', dst]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]  # ['ekmarin', 'kmearin', 'keamrin', dst]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]  # ['aemarin', 'bemarin', 'cemarin', dst]
    inserts = [L + c + R for L, R in splits for c in letters]  # ['akemarin', 'bkemarin', 'ckemarin', dst]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    # "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def cekKata(kata):
    try:
        r = Request('http://kateglo.com/api.php?format=json&phrase=' + kata, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(r).read()
        data = json.loads(response)
        data_list = list(data.items())
        data_list = data_list[0][1]
        if data_list is not None:
            if data_list['phrase_type'] is None:
                return set([data_list['actual_phrase']])
            else:
                return data_list['phrase']
        else:
            return kata
    except:
        return kata

def iniKataBaku(kata):
    try:
        r = Request('http://kateglo.com/api.php?format=json&phrase=' + kata, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(r).read()
        data = json.loads(response)
        data_list = list(data.items())
        data_list = data_list[0][1]
        if data_list is not None:
            if data_list['phrase_type'] is None:
                return set([data_list['actual_phrase']])
            else:
                return data_list['phrase']
        else:
            return ""
    except:
        return ""

kata = 'praktik'

file = open('kamus_typo.csv', 'w', newline='')

#cari jika ada di KBBI

hasil_kbbi = ""
hasil = ""

print(edits1(kata))

jumlah_data = len(edits1(kata))
progress = 0
for cek in edits1(kata):
    progress = progress + 1
    print(progress, "/", jumlah_data)
    if cek == "praktik": # hapus line ini, hanya untuk mempersingkat waktu
    #if iniKataBaku(cek):
        hasil_kbbi = cekKata(cek)

# tulis CSV
for kata_typo in edits1(kata):
    writer = csv.writer(file)
    if kata_typo == hasil_kbbi:
        typo = "TIDAK"
    else:
        typo = "YA"

    writer.writerow([kata_typo, hasil_kbbi, typo])

hasil = hasil_kbbi

print("Kata Typo: ", kata)
print("Hasil KBBI: ", hasil_kbbi)
print("Hasil Akhir: ", hasil)

    #print(kata, " tidak dikenal")