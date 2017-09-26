# group4-smzl -座席決定さん-

### 動作環境
- Python 3.4(PyQt)
- Python 2.7(RaspberryPy)
- PyQt5
- chainer 2.0.2
- dlib 19.4
- OpenCV 3.2.0

### 使用機器
- RaspberryPi3
- カメラ: logcool C922
- Felica: RC-S320

### 環境準備
brew等でインストール

### シーケンス図
@startuml

!define Target 来訪者

participant "MotionSensor" as Sensor
participant "RaspberryPi" as RasPi
participant "結果表示用PC" as PC
participant "CammeraSensor" as Cammera
participant "FelicaReader" as Felica
participant "Target" as Human

Sensor  -> RasPi    : 接近・離脱を検知する
RasPi   -> PC       : Socket使います
RasPi   <- PC       : 受け入れます
RasPi   -> PC       : 画像送信
PC      -> Human    : あなたは〜ですか
Human   -> Zaseki   : 席に移動
RasPi   -> Felica   : Felicaを読み取り
RasPi   <- Felica   : あなたは〜ですね

@enduml
