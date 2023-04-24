token = "MTA5ODU1NzgwN" + "jM4NDI1NTAwNg.GBdjnu." + "UNTOnA282RIe-mmhFA2nYqIMXe12UGkZ8I1xuk"

with open("data\\video_cards.txt", mode="r", encoding="UTF-8") as f:
    video_cards = [i.replace("\n", "") for i in f.readlines()]
    print("Видеокарты считаны")

with open("data\\cpus.txt", mode="r", encoding="UTF-8") as f:
    cpus = [i.replace("\n", "") for i in f.readlines()]
    print("Процессоры считаны")



radio = ["http://radio.real-drift.ru:8000/phonk.ogg", "https://listen5.myradio24.com/atmo",
         "https://pool.anison.fm/AniSonFM(320)?nocache=0.12814255561468157",
         "https://pub0301.101.ru:8443/stream/air/mp3/256/219", "https://pub0302.101.ru:8443/stream/pro/aac/64/103",
         "https://europaplus.hostingradio.ru:8014/europaplus320.mp3"]


