from flask import render_template, request
from flask import Flask


from collections import Counter
import pymysql
from datetime import datetime, timedelta

from werkzeug import secure_filename
from subprocess import call
from fastai.vision import *
import numpy as np
import subprocess
from pydub import AudioSegment
import librosa
import librosa.display
import matplotlib.pyplot as plt

np.random.seed(42)

# class(label) setting
# class name must be sorted in alphabet ascend order
classes = ['bad_ball_joint', 'bad_brake_pad', 'engine_seizing_up', 'failing_water_pump',
           'hole_in_muffler', 'no_problem']

# machine learning data setting

time_slice = 3

# audio setting

audio_sampling_rate = 44100  # sampling rate 44.1kHz
audio_bit_rate = 128000  # bit rate 128k
audio_channels = 1  # 1 is mono 2 is stereo, mono is default setting in android & IOS

# file path & name setting
wav_type = '.wav'
wav_path = '/app/MD_Web/app/upload/'
wav_name = ''
img_type = '.png'
img_path = '/app/MD_Web/app/upload/'
img_name = ''
mod_path = '/app/MD_Web/app/model/'

# server to client setting
top_rank = 3
percent_decimal_point = 4

# wav to mel spectrogram setting
img_size_x = 10
img_size_y = 4


def mapping_label(n):
    return classes[n]


def list_to_dic(label, prediction):
    return {label[i]: prediction[i] for i in range(0, len(label))}


def percentage(some_list):
    total_sum = sum(some_list)
    return [round((some_list[i] / total_sum) * 100, percent_decimal_point)
            for i in range(0, len(some_list))]

def sound_to_wav(name_tmp):
    global wav_name
    global img_name
    wav_name = name_tmp
    img_name = name_tmp
    command = "ffmpeg -y -i " + wav_path + wav_name + \
              " -ab " + str(audio_bit_rate) + \
              " -ac " + str(audio_channels) + \
              " -ar " + str(audio_sampling_rate) + \
              " " + wav_path + wav_name
    subprocess.call(command, shell=True)


def cut_wav_only3sec():
    wav = AudioSegment.from_wav(wav_path + wav_name)
    if len(wav) > 4000:
        edit_wav = wav[1000:1000+time_slice*1000]
        edit_wav.export(wav_path + wav_name, format="wav",
                parameters=["-ab", str(audio_bit_rate),
                    "-ac", str(audio_channels),
                    "-ar", str(audio_sampling_rate)])



def wav_to_mel():
    global img_name
    img_name = wav_name.split(".")[0]
    wav, sr = librosa.load(wav_path + wav_name)
    mel_spec = librosa.feature.melspectrogram(y=wav, sr=sr)
    plt.figure(figsize=(img_size_x, img_size_y))
    librosa.display.specshow(librosa.power_to_db(mel_spec, ref=np.max), sr=sr)
    plt.axis('off')
    plt.xticks([]), plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, hspace=0, wspace=0)
    plt.savefig(img_path + img_name + img_type, bbox_inces='tight', pad_inches=0)
    plt.close('all')


def predict():
    defaults.device = torch.device('cpu')
    learn = load_learner(mod_path)
    img = open_image(img_path + img_name + img_type)
    predict_class, predict_idx, output = learn.predict(img)
    result = output.tolist()
    result = percentage(result)
    top_rank_index = np.flip(np.argsort(result)[-top_rank:])
    top_rank_value = [result[i] for i in top_rank_index]
    top_rank_names = list(map(mapping_label, top_rank_index))
    return list_to_dic(top_rank_names, top_rank_value)

db = pymysql.connect("52.14.78.174", "root", "peoplespace5", "md_db")
#db = pymysql.connect("localhost", "root", "temp", "md_db")

app = Flask(__name__)

@app.route('/')
@app.route('/login')
def index(state=None):
    return render_template('/login.html', LoginState="None")

@app.route('/upload')
def render_file():
   return render_template('upload.html')

@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save("./upload/"+secure_filename(f.filename))
      sound_to_wav(f.filename)
      cut_wav_only3sec()
      wav_to_mel()
      print(predict())

      items = predict()
      for index, (key, elem) in enumerate(items.items()):
          print(index, key, elem)
      print("most : {}".format(list(items.keys())[0]))

      #input result to database
      curs = db.cursor(pymysql.cursors.DictCursor)
      sql = """insert into application(state)
               values (%s)"""
      curs.execute(sql, (list(items.keys())[0]).encode('utf-8'))
      db.commit()

      return str(predict())

@app.route('/main', methods=['POST', 'GET'])
def loginResult():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        print(id)
        print(password)

        try:
            if id == 'admin' and password == '12345':
                data = usageResult()
                return render_template('/index.html', dateCnt=data[0], causeTotal=data[1])
            else:
                return render_template('/login.html', LoginState="NO")

        except:
            return 'You are not registered'
    else:
        data = usageResult()
        return render_template('/index.html', dateCnt=data[0], causeTotal=data[1])

def usageResult():
    dateList = []
    dateCnt = [0, 0, 0, 0, 0, 0, 0]
    causeTotal = [0, 0, 0, 0, 0, 0]

    db = pymysql.connect("52.14.78.174", "root", "peoplespace5", "md_db")
    cursor = db.cursor()
    sql = "SELECT * FROM application"
    cursor.execute(sql)
    sqlresult = cursor.fetchall()
    print(sqlresult)

    #보낼데이터 : dateList, dateCnt
    today = datetime.today()
    for i in range(0,7):
        date = today + timedelta(days=-i)
        dateList.append(str(date)[:10])
    print(dateList)

    peopleUsage = []
    cause =[]
    for row in sqlresult:
        peopleUsage.append(row[1]) #날짜저장
        cause.append(row[2]) #원인저장


    peopleUsageCnt = Counter(peopleUsage)
    causeCnt = Counter(cause)

    for key in peopleUsageCnt:
        if str(key)[:10] in dateList:
            location = dateList.index(str(key)[:10])
            dateCnt[location] = dateCnt[location] + peopleUsageCnt[key]
        print(str(key)[:10], peopleUsageCnt[key])
    print(dateCnt)

    #넘길데이터 : causeNameList, causeTotal
    causeNameList = ['bad_ball_joint', 'bad_brake_pad', 'engine_seizing_up',
                     'failing_water_pump', 'hole_in_muffler', 'no_problem']
    for key in causeCnt:
        if key in causeNameList:
            location = causeNameList.index(key)
            causeTotal[location] = causeCnt[key]
        print(key, causeCnt[key])
    print(causeTotal)

    print(dateCnt)

    return [dateCnt,causeTotal, dateList]


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)