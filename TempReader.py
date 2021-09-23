import glob

class TempReader:

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    @staticmethod
    def readTempFile(): #Fundtion to read the value of Temperature
        
        try:
        
            file = open(TempReader.device_file, 'r') #opent the file
            lines = file.readlines() #read the lines in the file
            file.close() #close the file
                    
            trimmed_data = lines[1].find('t=') #find the "t=" in the line
                    
            if trimmed_data != -1:
                temp_string = lines[1][trimmed_data+2:] #trim the strig only to the temoerature value        
                return temp_string.strip()
            else: 
                return "US"
        except:
            return "US"
            

    @staticmethod
    def convertToDisplayFormat(inputTemp):
    
        return (inputTemp[:2] + "." + inputTemp[2:].strip() + " Celcius")
    
    @staticmethod
    def getTemp():
    
        return TempReader.readTempFile()