#模組
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from unicodedata import name
import requests

#導入opendata的清單
list_url = 'https://opendata.cwb.gov.tw/api/v1/rest/dataset'
r = requests.get(list_url)
j = json.loads(r.text)
list_index = []
#篩選需要的json清單
for i in j :
    if 'F-D' in i :
        list_index.append(i)
#print(list_index)

#輸入firebase金鑰
cred = credentials.Certificate("test-firestore.json")
firebase_admin.initialize_app(cred)

#進入firebhase
db = firestore.client()

#專題第一部分全臺灣各鄉鎮市區今、明2天預報資料 
for i in list_index[0:3] : 
    r = requests.get('https://opendata.cwb.gov.tw/api/v1/rest/datastore/'+ i + '?Authorization=CWB-1A653E9C-D256-4CD8-951F-FE746BB31A60')
    b = json.loads(r.text)
    doc_ref = db.collection(i).document(b["records"]["locations"][0]["locationsName"])
    doc_ref.set({"縣市":b["records"]["locations"][0]["location"][0]["locationName"]})
    for obj_ in b["records"]["locations"][0]["location"]:
        doc_ref.update(({obj_["locationName"]:obj_["weatherElement"]}))

#b7Bagu43ACrXOUph8mBEU3cG6Bn2PddA

#專題第二部分全台各縣市每日每小時天氣預報 
num_=[["宜蘭縣", 3369296],["桃園市", 3369297], ["新竹縣", 3369298], ["苗栗縣", 3369299], ["彰化縣", 3369300], ["南投縣", 3369301], ["雲林縣", 3369302], ["嘉義縣", 3369303], ["屏東縣", 3369304], ["臺東縣", 3369305], ["花蓮縣", 3369306], ["澎湖縣", 3369307], ["基隆市", 312605], ["新竹市", 313567], ["嘉義市", 312591], ["臺北市", 315078], ["高雄市", 313812], ["新北市", 2515397], ["臺中市", 315040], ["臺南市", 314999], ["連江縣", 3369309], ["金門縣", 2332525]]

#每日
for obj in num_[0:3]:
    url_daily=("http://dataservice.accuweather.com/forecasts/v1/daily/1day/"+str(obj[1])+"?apikey=b7Bagu43ACrXOUph8mBEU3cG6Bn2PddA&language=zh-tw")
    r_daily=requests.get(url_daily).json()
    doc_ref = db.collection("每日").document(obj[0])
    doc_ref.set({"天氣":r_daily})
    
for obj in num_[0:3]:
    url_hourly=("http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/"+str(obj[1])+"?apikey=b7Bagu43ACrXOUph8mBEU3cG6Bn2PddA&language=zh-tw")
    r_houly=requests.get(url_hourly).json()
    doc_ref = db.collection("每時").document(obj[0])
    doc_ref.set({"天氣":r_houly})

print("完成囉!")