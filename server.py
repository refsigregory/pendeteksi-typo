from flask import Flask
from flask import render_template, request, jsonify
from flask_cors import CORS
from ref_pendeteksi import PendeteksiKataTidakBaku as pendeteksi

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/start_checker", methods=['GET', 'POST'])
def start():
    import numpy as np
    import time

    text = request.values.get('text')
    print(text)
    if text != "" or text is not None:
        text_file = open("data/text", "w")
        text_file.write(text)
        text_file.close()

        daftar_kata = pendeteksi.tokenize('data/text')
        result = []
        kata_baru = []
        for hasil in daftar_kata:
            hasil_ditemukan = pendeteksi.cekKataMaxValue(hasil[0],'data/kamus_typo.csv')
            if hasil_ditemukan is not "":
                result.append([hasil_ditemukan[0], hasil_ditemukan[3], hasil_ditemukan[4]])

        # save salinan
        waktu = int(time.time())
        if(len(daftar_kata) > 0):
            namasalinan = daftar_kata[0][0]
        else:
            namasalinan = "text"
        namasalinan = namasalinan + str(waktu)
        text_file = open("data/" + namasalinan,  "w")
        text_file.write(text)
        text_file.close()

        # BELAJAR KATA BARU
        for hasil in daftar_kata:
            hasil_ditemukan = pendeteksi.cekKata(hasil[0], 'data/kamus_typo.csv')
            if hasil_ditemukan is "":
                print("Tidak mengenal:", hasil[0])
                kata_baru.append(hasil[0])
        if len(kata_baru) > 0:
            print("Belajar Kata Baru...")
            print(daftar_kata)
            pendeteksi.belajarKataBaru(pendeteksi, kata_baru)

            ## ULANGI PENGECEKAN
            result = [] # reset
            for hasil in daftar_kata:
                hasil_ditemukan = pendeteksi.cekKataMaxValue(hasil[0], 'data/kamus_typo.csv')
                if hasil_ditemukan is not "":
                    result.append([hasil_ditemukan[0], hasil_ditemukan[3], hasil_ditemukan[4]])

    print(result)
    print("SELESAI")

    if result is None or result == []:
        return ""
    else:
        return jsonify(result)

@app.route("/check_kata", methods=['GET', 'POST'])
def check():
    import numpy as np

    text = request.values.get('text')

    result = []

    result = pendeteksi.getKataMaxValue(text, 'data/kamus_typo.csv')

    return jsonify(result)

@app.route("/insert_kata", methods=['GET', 'POST'])
def insert_kata():
    kata = request.values.get('kata_typo')
    saran = request.values.get('kata_baku')
    ini_typo = request.values.get('ini_typo')
    ini_baku = request.values.get('ini_baku')
    ini_valid = request.values.get('ini_valid')

    pendeteksi.tambahSaran(pendeteksi, 'data/kamus_typo.csv', [kata, saran, ini_typo, ini_baku, ini_valid])

    return "ok"
@app.route("/reset_kata", methods=['GET', 'POST'])
def reset_kata():
    if pendeteksi.resetKamusKata(pendeteksi):
        return "ok"
    else:
        return "fail"


if __name__ == "__main__":
    app.run(debug=True)