import pandas as pd
import re
from collections import Counter
from pathlib import Path
import csv
# import StemmerFactory class
from urllib.request import urlopen, Request
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import qlearn
import numpy as np

class PendeteksiKataTidakBaku:
    def tokenize(file):
        # buka file
        f = open(Path(file), "r")
        s = f.read().lower()

        s = re.sub('[^A-Za-z\ ]+', ' ', s) #delete special chars

        s = re.sub(' +', ' ', s) # remove multiple space

        pecah_kata = re.findall(r'\S+', s)

        # ambil jumlah setiap kata
        hasil_tokenize = list(Counter(pecah_kata).items())
        # urutkan berdasarkan jumlah kata
        hasil_tokenize = sorted(hasil_tokenize, key=lambda x: x[1], reverse=True)

        return hasil_tokenize

    def cekKata(kata, kamus):
        kamus_kata = pd.read_csv(Path(kamus), delimiter=",")

        hasil_ditemukan = ""
        kata = kata.lower()
        hasil_kata = kamus_kata[kamus_kata['kata_typo'] == kata]
        if len(hasil_kata) > 0:
            hasil_ditemukan = hasil_kata.values.tolist()

        return hasil_ditemukan

    def cekKataTypo(kata, kamus):
        kamus_kata = pd.read_csv(Path(kamus), delimiter=",")

        hasil_ditemukan = ""
        kata = kata.lower()
        hasil_kata = kamus_kata[(kamus_kata['ini_typo'] == 'YA') & (kamus_kata['kata_typo'] == kata)]
        if len(hasil_kata) > 0:
            hasil_ditemukan = hasil_kata.values.tolist()

        return hasil_ditemukan

    def tambahKamus(file,list_element):
        #typo = typo.upper()
        #baku = baku.upper()
        with open(file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_element)
        #writer.writerow([salah, benar, typo, baku])

    def tambahSaran(self, file,list_element):
        typo = list_element[2].upper()
        baku = list_element[3].upper()
        valid = list_element[4].upper()
        salah = list_element[0]
        benar = list_element[1]
        reward = 0
        hasil_ditemukan = self.cekKata(list_element[0], file)
        if hasil_ditemukan is not "":
            for hasil in hasil_ditemukan:
                if hasil[2] == typo:
                    reward = 100
                else:
                    reward = -10
                with open(file, 'a+', newline='') as write_obj:
                    # Create a writer object from csv module
                    csv_writer = csv.writer(write_obj)
                    # Add contents of list as last row in the csv file
                    if hasil[1] is np.nan:
                        hasil_benar = ""
                    else:
                        hasil_benar = hasil[1]
                    csv_writer.writerow([hasil[0], hasil_benar, hasil[2], hasil[3], hasil[4], reward])  # update reward

        else:
            reward = 0

        with open(file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow([salah, benar, typo, baku, valid, 0]) # tambah saran
        #writer.writerow([salah, benar, typo, baku])

    def cek_KBBI(kata):
        try:
            r = Request('http://kateglo.com/api.php?format=json&phrase=' + kata, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(r).read()
            data = json.loads(response)
            data_list = list(data.items())
            data_list = data_list[0][1]
            return data_list
        except:
            return None

    def iniKataBaku(self, kata):
        hasil_kata = self.cek_KBBI(kata)
        if hasil_kata is not None:
            if hasil_kata['phrase_type'] is None:
                return False
            else:
                return True
        else:
            return False

    def stemKata(kata):
        # Check Typo
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        # Stem Kata
        kata_stem = stemmer.stem(kata)
        return  kata_stem

    def pengecekanKBBI(self, daftar_kata):
        for hasil in daftar_kata:
            kata = hasil[0].lower()
            hasil_kata = self.cek_KBBI(kata)
            if hasil_kata is not None:
                if hasil_kata['phrase_type'] is None:
                    print(hasil_kata['phrase'], "digunakan ", hasil[1], "kali, ")
                    print("Tidak baku, harusnya ", hasil_kata['actual_phrase'])
                else:
                    print(hasil_kata['phrase'], "digunakan ", hasil[1], "kali, ")
                    print("Ok")
            else:
                # print(kata, "bukan kata yang benar ")
                # Check Typo
                factory = StemmerFactory()
                stemmer = factory.create_stemmer()
                # Stem Kata
                kata_stem = stemmer.stem(kata)
                print('Hasil stem : ', kata_stem)
                # Cek lagi
                hasil_kata = self.cek_KBBI(kata_stem)
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

    def belajarKataBaru(self, daftar_kata):
        for daftar in daftar_kata:

            asli = daftar
            baku = "TIDAK"
            typo = "YA";
            valid = "TIDAK"


            if self.iniKataBaku(self, daftar) is True:
                # Kata yang Baku
                baku = "YA"
                typo = "TIDAK"
                valid = "YA"

                print(daftar, "baku")
            else:
                print(daftar, "tidak")
                if self.iniKataBaku(self, self.stemKata(daftar)) is True:
                    print(daftar, "stem baku")
                    baku = "YA"
                    asli = self.stemKata(daftar)
                else:
                    asli = ""

            self.tambahKamus('kamus_typo.csv', [daftar, asli,  typo, baku, valid, 0])




if __name__ == '__main__':

    pendeteksi = PendeteksiKataTidakBaku
    daftar_kata = pendeteksi.tokenize('text.txt')
    kata_baru = []
    for hasil in daftar_kata:
        hasil_ditemukan = pendeteksi.cekKata(hasil[0],'kamus_typo.csv')
        if hasil_ditemukan is not "":
            for hasil in hasil_ditemukan:
                if hasil[2] == 'YA':
                    print("Ditemukan:", hasil[0])
                    if hasil[1] is np.nan:
                        print("Harusnya:", hasil[1])
                    else:
                        print("Kata Ini Salah, Harap periksa kembali!")
                    print("\n")
        else:
            print("Tidak mengenal:", hasil[0])
            kata_baru.append(hasil[0])

    # BELAJAR KATA BARU
    print("Belajar Kata Baru...")
    if len(kata_baru) > 0:
        pendeteksi.belajarKataBaru(pendeteksi, kata_baru)

    print("SELESAI")

    pendeteksi.tambahSaran(pendeteksi, 'kamus_typo.csv', ['yang', 'yang', 'TIDAK', 'YA', 'YA'])

    #pendeteksi.tambahKamus('kamus_typo.csv', ['bagaimana', 'bagaimana', 'TIDAK', "YA", "YA"])

    #pendeteksi.tambahKamus('kamus_typo.csv', ['universitas', 'universitas', 'TIDAK', "TIDAK", "YA"])

    #pendeteksi.pengecekanKBBI(PendeteksiKataTidakBaku,daftar_kata)
    #
    # ai = qlearn.QLearn(actions=range(5),
    #               alpha=0.1, gamma=0.9, epsilon=0.1)
    # state = 0
    # reward = 0
    # lastState = 0
    # lastAction = 0
    #
    # reward = 100
    # print(ai.learn(lastState, lastAction, reward, state))
    #
    #
    # # Choose a new action and execute it
    # state = 2
    # action = ai.chooseAction(state)
    # lastState = state
    # lastAction = action
    #
    # print(ai.learn(lastState, lastAction, reward, state))