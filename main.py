import pandas as pd
import os
from datetime import datetime
#DEFS
START_TIME = datetime.now()
def str_binary(str)->str:
    return ''.join(format(ord(i), '08b') for i in str)

class MagicChecker:

    MAGIC_NUMBERS = {}
    SCHEMA        = ["FileName", "MAGIC", "Extension", "Matches", "Time"]
    def __init__(self, magic_to_find:list, expected_ext:str) -> None:
        # wild card is valid, it ignores whatever hex value is at indicie
        self.magic_to_find = magic_to_find
        self.expected_ext  = expected_ext
        #expected extension, 
        MagicChecker.MAGIC_NUMBERS[expected_ext] = magic_to_find
        #add some extern config eventually, so that magic for x extension can be loaded easier
    def checkExtMagic(self, file)->dict:
        #checks if the magic alligns with the extension
        is_matching = True
        print("checking etx")

        return_dict = {'FileName': file.name, "MAGIC": self.magic_to_find, "Extension": self.expected_ext, "Matches":is_matching, "Time" : START_TIME}
        #This is used to populate df 
        print(f"len: {len(self.magic_to_find)}")
        str_to_parse = file.read(len(self.magic_to_find))
        print(f"parse: {str_to_parse}")
        for index, elem in enumerate(self.magic_to_find):
            print(f"ind : {index}, elm : {elem}")
            if(str_to_parse[index] == elem ):
                print("Match!")
                continue
            if (elem == '*'):
                continue
            else:
                is_matching = False
                break
        return_dict["Matches"] = is_matching
        
        return return_dict
    def checkAllMagic(self, file) ->dict:
        pass
    def getExtdf(self, optional_path = ".")->pd.DataFrame:
        #checks all magic regardless of extension at a directory of choice 
        files = [f for f in os.listdir(optional_path) ]
        df_vals = []
        for file in files:
            with open(os.path.join(optional_path, file), "rb") as file_stream:
                print(file_stream)
                upsert_data = self.checkExtMagic(file_stream)
                df_vals.append(upsert_data)
        df = pd.DataFrame.from_dict(df_vals)

        return df
    def logDf(self, df:pd.DataFrame, optional_path = "./logs/")->None:
        optional_path += str(datetime.now()) + "_MagicChecker"
        optional_path = ''.join([x for x in optional_path if x != " "])
        #uses check all magic
        print(df)
        df.to_csv(optional_path)

        pass
wav_magic_bytes = 'RIFF****WAVE'
check_for_wav = MagicChecker(wav_magic_bytes,".wav")
df            = check_for_wav.getExtdf(optional_path="/home/jetblack/Downloads/Sound")
check_for_wav.logDf(df)


#CODE
