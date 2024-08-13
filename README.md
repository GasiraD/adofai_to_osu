# adofai_to_osu


# .osu
.osu 는 osu파일 
[TimingPoints]는 bpm정하는거랑 언제 그 bpm이 적용되는지

[HitObjects]에서 64,192,200,1,0,0:0:0:0: 3번째값이 제일중요함 밀리세컨드기준으로 순차적으로 합쳐지면서 증가

64,192,200,1,0,0:0:0:0:

192,192,350,1,0,0:0:0:0:

448,192,400,1,0,0:0:0:0:


# .adofai
.adofai는 json이랑 비슷하지만 json은 아님


"angleData":

"bpm": 354,	

{ "floor": 1, "eventType": "SetSpeed" ... "beatsPerMinute": 100, "bpmMultiplier": 0.0625"}

{ "floor": 6, "eventType": "Twirl" },

bpm이 100인건 비활성화된 상태고 bpm354로 치부하면됨


decimal angle = (NextTile - ThisTile + 540) % 360;
if (Twirled) angle = 360 - angle;
if (angle == 0) angle = 360;
