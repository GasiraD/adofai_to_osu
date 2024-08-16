import json
import os
import re
from itertools import cycle
import math

DSET = ['R', 'p', 'J', 'E', 'T', 'o', 'U', 'q', 'G', 'Q', 'H', 'W', 'L', 'x',
 'N', 'Z', 'F', 'V', 'D', 'Y', 'B', 'C', 'M', 'A', 'R', 'p', 'J',
 'E', 'T', 'o', 'U', 'q', 'G', 'Q', 'H', 'W', 'L', 'x', 'N', 'Z',
 'F', 'V', 'D', 'Y', 'B', 'C', 'M', 'A'] # 이건모름




class AdoFaiParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.results = []
        self.bpm_dict = {}
        self.bpmmulti_dict = {}
        self.twirl_dict = {}
        self._parse_file()
        self.bpm = 354 ## 후에 이 부분 수정
        self.final_results = []

    def _parse_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            adofai_data = file.read()
        lines = adofai_data.splitlines()

        for line in lines:
            if "angleData" in line:
                self._parse_angle_data(line)
            elif '"eventType": "SetSpeed"' in line:
                self._parse_set_speed(line)
            elif '"eventType": "Twirl"' in line:
                self._parse_twirl(line)
            elif "bpm" in line:
                self._parse_bpm(line)

    def _parse_angle_data(self, line):
        line = '{' + line.strip().rstrip(',') + '}'
        data = json.loads(line)
        angle_data = data.get("angleData", [])
        for index, value in enumerate(angle_data, start=1):
            self.results.append([index, value, None, False])

    def _parse_set_speed(self, line):
        line = line.strip().rstrip(',')
        data = json.loads(line)
        floor_data = data.get("floor")

        bpm= data.get("beatsPerMinute", [])
        bpmmulti = float(data.get("bpmMultiplier", []))

        if bpm is not None:
            self.bpm_dict[floor_data] = bpm

        if bpmmulti is not None:
            self.bpmmulti_dict[floor_data] = bpmmulti

    def _parse_twirl(self, line):
        line = line.strip().rstrip(',')
        data = json.loads(line)
        floor_data = data.get("floor")
        self.twirl_dict[floor_data] = True
     
    def _parse_bpm(self, line):
        line = line.strip().rstrip(',')
        data = json.loads(line)
        self.bpm = data.get("bpm")

    def get_final_results(self):
        bpm_value = float(self.bpm)
        tw = 0
        for result in self.results:
            floor = result[0]
            angle_value = result[1]

            bpm = self.bpm_dict.get(floor, [])
            bpmmulti = self.bpmmulti_dict.get(floor, [])

            if bpm != 100 and bpm != []:
                bpm_value = bpm
                bpmmulti = 1

            if bpmmulti != []:
                bpm_value = bpm_value * bpmmulti
                prev_bpm_value = bpm_value

            elif bpmmulti == []:
                bpm_value = prev_bpm_value


            twirl_value = self.twirl_dict.get(floor, [])
            if twirl_value is True:
                tw +=1
            else:
                pass

            self.final_results.append([floor, angle_value, bpm_value, tw])
        return self.final_results
    
    def write_final_results(self):
        self.final_results = self.get_final_results()
        with open("final_results", "w", encoding="utf-8") as file:
            for result in self.final_results:  # self.final_results 사용
                file.write(f"{result}\n")



#([floor, angle_value, round(bpm_value), twirl_value])

class TimingCalculator:
    def __init__(self, final_results):
        self.final_results = final_results
        self.coordinates_list = [64, 192, 448, 320]
        self.coordinates_cycle = cycle(self.coordinates_list)
        self.osu_timing = 0
        self.total_milisec = 0
        self.current_list = self.extract_second_values(final_results)
        self.next_list = self.rearrange_list(self.extract_second_values(final_results))

    def extract_second_values(self, data):
        second_values = [sublist[1] for sublist in data]
        return second_values
    
    def rearrange_list(self, data):
        if data: 
            data.append(data.pop(0))
        return data

    def calculate_timing(self, data):
 
        bpm = data[2]
        angle_current = self.current_list[data[0] - 1]
        angle_next = self.next_list[data[0] - 1]

        if angle_next == 999:
            angle_current
            angle_next = self.next_list[data[0]]
            movementz = (angle_current - angle_next) % 360
            if movementz < 0:
                movementz = (movementz + 360) % 360

            if data[3] % 2:
                movementz = 360 - movementz

            if movementz == 0:
                movementz = 360

            milliseconds_osu = (60000 / bpm) * (movementz / 180)
            #milliseconds_osu = round((1000 * movement) / (3 * bpm))

            return milliseconds_osu

        if angle_current == 999:
            return 0

        movement = 360-((angle_next - angle_current + 540) % 360)



        if data[3] % 2:
            movement = 360 - movement

        if movement == 0:
            movement = 360

        milliseconds_osu = (60000 / bpm) * (movement / 180)
        #milliseconds_osu = round((1000 * movement) / (3 * bpm))

        return milliseconds_osu
    

    def calculate_angle(self, data):

        angle_current = self.current_list[data[0] - 1]
        angle_next = self.next_list[data[0] - 1]

        if angle_next == 999:
            angle_current
            angle_next = self.next_list[data[0]]
            movementz = (angle_current - angle_next) % 360
            if movementz < 0:
                movementz = (movementz + 360) % 360

            return movementz
        
        if angle_current == 999:
            return 0
        

        movement = 360-((angle_next - angle_current + 540) % 360)


        if data[3] % 2:
            movement = 360 - movement

        if movement == 0:
            movement = 360


        return movement
    

    def write_osu_results(self):
        osu_timing = 0
        with open('osu_results', 'w', encoding='utf-8') as file:
            for t in self.final_results:
                timing = self.calculate_timing(t)
                osu_timing += timing
                coordinates = next(self.coordinates_cycle)
                if self.calculate_angle(t) == 0:
                    continue
                file.write(f"{coordinates},192,{round(osu_timing)},1,0,0:0:0:0:\n")
                  

    def write_osu_results_info(self):
        osu_timing = 0
        with open('osu_results_info', 'w', encoding='utf-8') as file:
            for t in self.final_results:
                timing = self.calculate_timing(t)
                osu_timing += timing
                if self.calculate_angle(t) == 0:
                    continue
                file.write(f"floor{t[0]}, 현재타일은{self.current_list[t[0] - 1]}, 다음타일은{self.next_list[t[0] - 1]} , angle은 {self.calculate_angle(t)}, 밀리초기준은 {round(timing)}, bpm은 {round(t[2])}, 회전여부는 {t[3]}, 총{round(osu_timing)}\n")
 


def main():
    adofai_parser = AdoFaiParser('main.adofai')
    final_results = adofai_parser.get_final_results()

    timing_calculator = TimingCalculator(final_results)
    #adofai_parser.write_final_results()
    timing_calculator.write_osu_results()
    timing_calculator.write_osu_results_info()


if __name__ == "__main__":
    main()
