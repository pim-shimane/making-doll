# Pythonコード使ってRoomba動かしてみた
　当レポのpythonコードのほぼ全てが[martinschaef/roomba](https://github.com/martinschaef/roomba)を参考に作られています。  
　This repo's codes are from [martinschaef/roomba](https://github.com/martinschaef/roomba). We really appreciate the awesome repo!
### 展示の際の手順

- [ここ](https://karaage.hatenadiary.jp/entry/2017/05/12/073000)で配線の最終確認。  
- Google Home Miniの設定

1.　google home mini の初期化（機器裏側の分かりにくい小さいボタンを長押し）。 ← これが一番確実  
2.　スマホの設定から、pim.shimane@gmail.comのアカウントにログイン。  
3.　GoogleHomeのスマホアプリからgoogle home mini のセットアップを行う。  

- NODE-REDの設定

4.　raspberry pi のwi-fi設定を行うために以下のコマンドを叩く。(5GHz帯では繋がらないです)
    
    wpa_passphrase [SSID] [password] > /etc/wpa_supplicant/wpa_supplicant.conf
    sudo reboot

5.　NODE-REDのスタートコマンドを叩く

    node-red-start  

### 制作中に参考にしたページ

今(2019/4月)のルンバを動かすための[プログラム等の参考資料](https://tarukosu.hatenablog.com/entry/2017/09/10/222028break)  
Serial Control Interface(SCI)で使えそうな[コード資料](http://www.jonathanleroux.org/research/micbots/pyrobot2.py)  
ROSで動かそうとしたときの[資料](https://r17u.hatenablog.com/entry/2017/06/17/222228)  
[ラズパイにubuntu16.04載せた（結局rapsbianを使ったけどね）](https://www.asrobot.me/entry/2018/07/11/001603/)  

### 技術ブログのような何かを書きました
[アツシミカン制作秘話](https://pim-shimane.com/blog/2019-10-18-%E3%82%A2%E3%83%84%E3%82%B7%E3%83%9F%E3%82%AB%E3%83%B3%E5%88%B6%E4%BD%9C%E7%A7%98%E8%A9%B1/)
