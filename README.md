# adofai_to_osu

.osu 는 osu파일 
[TimingPoints]는 bpm정하는거랑 언제 그 bpm이 적용되는지
[HitObjects]에서 64,192,200,1,0,0:0:0:0: 단노트기준으로는
3번째값이 제일중요함 밀리세컨드기준으로 
64,192,200,1,0,0:0:0:0:
192,192,350,1,0,0:0:0:0:
448,192,400,1,0,0:0:0:0:
320,192,500,1,0,0:0:0:0:
64,192,550,1,0,0:0:0:0:
192,192,900,1,0,0:0:0:0:
이렇게 순차적으로 합쳐지면서 증가


.adofai는 유사json형식(json)은 아님

"angleData":
"bpm": 354,
{ "floor": 1, "eventType": "SetSpeed" 에서 "beatsPerMinute": 100, "bpmMultiplier": 0.0625"}
{ "floor": 6, "eventType": "Twirl" },

대신 bpm이 100인건 비활성화된 상태고 bpm354로 치부하면됨
