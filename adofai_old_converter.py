class old_converter:
    def convert_data(self, angle_data):
        self.converted_data = []
        angle_data = ''
        for char in angle_data:
            match char:
                case 'R':
                    self.converted_data.append(0)
                case 'L':
                    self.converted_data.append(180)
                case 'U':
                    self.converted_data.append(90)
                case 'D':
                    self.converted_data.append(-90)
                case 'E':
                    self.converted_data.append(45)
                case 'C':
                    self.converted_data.append(135)
                case 'J':
                    self.converted_data.append(30)
                case 'H':
                    self.converted_data.append(150)
                case 'N':
                    self.converted_data.append(210)
                case 'M':
                    self.converted_data.append(-30)
                case 'T':
                    self.converted_data.append(60)
                case 'G':
                    self.converted_data.append(120)
                case 'F':
                    self.converted_data.append(240)
                case 'B':
                    self.converted_data.append(-60)
                case '!':
                    self.converted_data.append(999)
        return self.converted_data


        
        
