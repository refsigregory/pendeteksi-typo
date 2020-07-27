import pandas as pd, numpy as np, re, json, csv
from collections import Counter
from pathlib import Path
from urllib.request import urlopen, Request
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class Pendeteksi:
    def clearData(self):
        text = "kata_typo,kata_benar,ini_typo,ini_baku,ini_valid,value"
        text_file = open("data/kamus_typo.csv", "w")
        text_file.write(text + "\n")
        text_file.close()

        return True

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

    def showWords(self):
        kata = pd.read_csv(Path('data/kamus_typo.csv'), delimiter=",")

        hasil_ditemukan = ""
        if len(kata) > 0:
            hasil_ditemukan = kata.values.tolist()

        return hasil_ditemukan

    def checkWord(kata, kamus):
        kamus_kata = pd.read_csv(Path(kamus), delimiter=",")

        hasil_ditemukan = ""
        kata = kata.lower()
        hasil_kata = kamus_kata[kamus_kata['kata_typo'] == kata]
        if len(hasil_kata) > 0:
            hasil_ditemukan = hasil_kata.values.tolist()

        return hasil_ditemukan

    def checkWords(kata, kamus):
        kamus_kata = pd.read_csv(Path(kamus), delimiter=",")

        hasil_ditemukan = ""
        kata = kata.lower()
        hasil_kata = kamus_kata[kamus_kata['kata_typo'] == kata]
        if len(hasil_kata) > 0:

            katatypo = hasil_kata.groupby('kata_typo').sum()
            katabaku = hasil_kata.groupby('kata_benar').sum()
            typo = hasil_kata.groupby('ini_typo').sum()
            baku = hasil_kata.groupby('ini_baku').sum()
            valid = hasil_kata.groupby('ini_valid').sum()

            max_hasil = typo['value'].argmax()

            result_typo = ""
            result_baku = ""
            result_initypo = ""
            result_inibaku = ""
            result_inivalid = ""

            if katatypo.iloc[katatypo['value'].argmax()].name is not None:
                result_typo = katatypo.iloc[katatypo['value'].argmax()].name
            if katabaku.iloc[katabaku['value'].argmax()].name is not None:
                result_baku = katabaku.iloc[katabaku['value'].argmax()].name

            if  baku.iloc[baku['value'].argmax()].name is not None:
                result_inibaku = baku.iloc[baku['value'].argmax()].name

            if  typo.iloc[typo['value'].argmax()].name is not None:
                result_initypo = typo.iloc[typo['value'].argmax()].name
            print(hasil_kata)

            if valid.iloc[valid['value'].argmax()].name is not None:
                result_inivalid = valid.iloc[valid['value'].argmax()].name

            if result_initypo != "":
                if result_initypo == 'YA' or result_inibaku == 'TIDAK':
                    hasil_ditemukan = [result_typo,
                                       result_baku,
                                       result_initypo, result_inibaku,
                                       result_inivalid]

        return hasil_ditemukan

    def getWords(kata, kamus):
        kamus_kata = pd.read_csv(Path(kamus), delimiter=",")

        hasil_ditemukan = ""
        kata = kata.lower()
        hasil_kata = kamus_kata[kamus_kata['kata_typo'] == kata]
        katatypo = hasil_kata.groupby('kata_typo').sum()
        katabaku = hasil_kata.groupby('kata_benar').sum()
        typo = hasil_kata.groupby('ini_typo').sum()
        baku = hasil_kata.groupby('ini_baku').sum()
        valid = hasil_kata.groupby('ini_valid').sum()

        if len(hasil_kata) > 0:
            try:
                hasil_ditemukan = [katatypo.iloc[katatypo['value'].argmax()].name, katabaku.iloc[katabaku['value'].argmax()].name, typo.iloc[typo['value'].argmax()].name, baku.iloc[baku['value'].argmax()].name, valid.iloc[valid['value'].argmax()].name]
            except ValueError:
                pass

        return hasil_ditemukan


    def checkTypo(kata, kamus):
        kamus_kata = pd.read_csv(Path(kamus), delimiter=",")

        hasil_ditemukan = ""
        kata = kata.lower()
        hasil_kata = kamus_kata[(kamus_kata['ini_typo'] == 'YA') & (kamus_kata['kata_typo'] == kata)]
        if len(hasil_kata) > 0:
            hasil_ditemukan = hasil_kata.values.tolist()

        return hasil_ditemukan

    def addWord(file,list_element):
        #typo = typo.upper()
        #baku = baku.upper()
        with open(file, 'a+', newline='') as write_obj:
            # Create a writer object from csv module
            csv_writer = csv.writer(write_obj)
            # Add contents of list as last row in the csv file
            csv_writer.writerow(list_element)
        #writer.writerow([salah, benar, typo, baku])

    def addCorrection(self, file,list_element):
        typo = list_element[2].upper()
        baku = list_element[3].upper()
        if baku == "":
            baku = "-"
        valid = list_element[4].upper()
        salah = list_element[0]
        benar = list_element[1]
        reward = 0
        hasil_ditemukan = self.checkWord(list_element[0], file)
        if hasil_ditemukan is not "":
            for hasil in hasil_ditemukan:
                if hasil[2] == typo and hasil[3] == baku and hasil[4] == valid and hasil[1] == benar:
                    reward = 100
                else:
                    reward = -10
                with open(file, 'a+', newline='') as write_obj:
                    # Create a writer object from csv module
                    csv_writer = csv.writer(write_obj)
                    # Add contents of list as last row in the csv file
                    if hasil[1] is np.nan or hasil[1] == "":
                        hasil_benar = "-"
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

    def checkKBBI(kata):
        try:
            r = Request('http://kateglo.com/api.php?format=json&phrase=' + kata, headers={'User-Agent': 'Mozilla/5.0'})
            response = urlopen(r).read()
            data = json.loads(response)
            data_list = list(data.items())
            data_list = data_list[0][1]
            return data_list
        except:
            return None

    def hasKBBI(self, kata):
        hasil_kata = self.checkKBBI(kata)
        if hasil_kata is not None:
            if hasil_kata['phrase_type'] is None:
                return False
            else:
                return True
        else:
            return False

    def stemWord(kata):
        # Check Typo
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        # Stem Kata
        kata_stem = stemmer.stem(kata)
        return  kata_stem

    def checkerKBBI(self, daftar_kata):
        for hasil in daftar_kata:
            kata = hasil[0].lower()
            hasil_kata = self.checkKBBI(kata)
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
                hasil_kata = self.checkKBBI(kata_stem)
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

    def addNewWords(self, daftar_kata):
        for daftar in daftar_kata:

            asli = daftar
            baku = "TIDAK"
            typo = "YA";
            valid = "TIDAK"


            if self.hasKBBI(self, daftar) is True:
                # Kata yang Baku
                baku = "YA"
                typo = "TIDAK"
                valid = "YA"

                print(daftar, "baku")
            else:
                print(daftar, "tidak")
                if self.hasKBBI(self, self.stemWord(daftar)) is True:
                    print(daftar, "stem baku")
                    baku = "YA"
                    asli = self.stemWord(daftar)
                else:
                    asli = "-"

            self.addWord('data/kamus_typo.csv', [daftar, asli,  typo, baku, valid, 0])


