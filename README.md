# Python Roomba
Python 2.7 scripts to control the Roomba via serial cable. This work is based on the script from [this](http://cs.gmu.edu/~zduric/cs101/pmwiki.php/Main/APITutorial) course. I adjusted it a bit to get access to the light bump in the Create 2 and my Roomba 770.

### Dependencies
You need pyserial to run this script.

    pip install pyserial
    
or
    
    easy_install pyserial

### Tester
I added a file to control the roomba with the wasd-keys. For that you also need pygame installed.
Just run 

    python game.py
    
and a window with some information about the current sensor values like the one below:

![game.pu](./img/screen.png "Screenshot")

Move the Roomba around with w/a/s/d.

### Use as library

The main class is create.py which contains everything to talk to the Roomba. To use it write sth like:

    import create
    import time
    robot = create.Create(ROOMBA_PORT)
    robot.printSensors() # debug output
    wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
    print (wall_fun()) # print a sensor value.
    robot.toSafeMode()
    robot.go(0,100) # spin
    time.sleep(2.0)
    robot.close()

For more information read the original [tutorial](http://cs.gmu.edu/~zduric/cs101/pmwiki.php/Main/APITutorial). The list of all available sensors is [here](https://github.com/martinschaef/roomba/blob/master/create.py#L70).

### My setup

I tested these scripts using this [cable](http://store.irobot.com/communication-cable-create-2/product.jsp?productId=54235746) and a Roomba 770. I tested the code on a Mac and on a RaspberryPi with debian (you need to change the PORT to tty.USB0 on the Pi) If the Roomba does not connect properly, check the cable first, then check if the port is correct, and then check if the baud rate in create.py is correct.

### Known issues

The odometer data is nonsense. I assume that there are bugs in the computation because its off way too much to count it as cumulative error.

### 展示の際の手順
　■ Google Home Miniの設定

1.　google home mini の初期化（機器裏側の分かりにくい小さいボタンを長押し）。 ← これが一番確実  
2.　スマホの設定から、pim.shimane@gmail.comのアカウントにログイン。  
3.　GoogleHomeのスマホアプリからgoogle home mini のセットアップを行う。  

　■ NODE-REDの設定

5.　raspberry pi のwi-fi設定を行うために以下のコマンドを叩く。(もしかすると5GHz帯では繋がらないかも)  
    wpa_passphrase [SSID] [password] > /etc/wpa_supplicant/wpa_supplicant.conf
    sudo reboot  
6.　NODE-REDのスタートコマンドを叩く  
    node-red-start  
7.　[ここ](https://karaage.hatenadiary.jp/entry/2017/05/12/073000)で配線の最終確認。

### 参考にしたページ

今(2019/4月)のルンバを動かすための[プログラム等の参考資料](https://tarukosu.hatenablog.com/entry/2017/09/10/222028break)  
Serial Control Interface(SCI)で使えそうな[コード資料](http://www.jonathanleroux.org/research/micbots/pyrobot2.py)  
ROSで動かそうとしたときの[資料](https://r17u.hatenablog.com/entry/2017/06/17/222228)  
[ラズパイにubuntu16.04載せた（結局rapsbianを使ったけどね）](https://www.asrobot.me/entry/2018/07/11/001603/)  
