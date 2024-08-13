import re
import math

class TileLib:
    TileAngle = {
        "L": 360,
        "Q": 45,
        "U": 90,
        "E": 135,
        "R": 180,
        "C": 225,
        "D": 270,
        "Z": 315,
        "H": 30,
        "G": 60,
        "T": 120,
        "J": 150,
        "M": 210,
        "B": 240,
        "F": 300,
        "N": 330,
        "S5": 108,
        "S6": 252,
        "S7": 900 / 7,
        "S8": 1620 / 7
    }

    @staticmethod
    def get_angle_by_code(code):
        # Special tile types 5 ~ 8
        if re.fullmatch(r'[5-8]+', code):
            stack5 = len(re.findall(r'5', code)) % 5
            stack6 = len(re.findall(r'6', code)) % 5
            stack7 = len(re.findall(r'7', code)) % 5
            stack8 = len(re.findall(r'8', code)) % 5
            return ((72 * stack5) + (288 * stack6) + (900 / 7 * stack7) + (1620 / 7 * stack8)) % 360
        
        # Normal tile types
        return TileLib.TileAngle.get(code, 0)

    @staticmethod
    def get_relative_angle(ThisTile, NextTile, Twirled):
        result = (NextTile - ThisTile + 540) % 360
        if Twirled:
            result = 360 - result
        return result if result != 0 else 360

    @staticmethod
    def get_milliseconds_between(BPM, Angle):
        return (1000 * Angle) / (3 * BPM)


# Example Usage
def calculate_timing(this_tile_code, next_tile_code, bpm, twirled=False):
    ThisTileAngle = TileLib.get_angle_by_code(this_tile_code)
    NextTileAngle = TileLib.get_angle_by_code(next_tile_code)
    
    RelativeAngle = TileLib.get_relative_angle(ThisTileAngle, NextTileAngle, twirled)
    milliseconds = TileLib.get_milliseconds_between(bpm, RelativeAngle)
    
    return {
        "ThisTileAngle": ThisTileAngle,
        "NextTileAngle": NextTileAngle,
        "RelativeAngle": RelativeAngle,
        "Milliseconds": milliseconds
    }

# Example
result = calculate_timing("U", "R", 120, False)
print(result)