import openpyxl
import os
import joblib
import shutil
import numpy as np
import pandas as pd


class Excel_output:
    def __init__(self, new_file_name_finally, path_save_read, choose_type_file, already_assigned, encoder, texts, path_location_save, data_line):
        self.choose_type_file = choose_type_file
        self.encoder = encoder
        self.already_assigned = already_assigned
        self.texts = texts
        self.data_line = data_line
        self.path_location_save = path_location_save
        self.path_save_read = path_save_read
        self.path_save_plain = None
        self.new_file_name_finally = new_file_name_finally

    def Excel_Write_output(self):
        path_plain = os.path.join(self.path_save_read, "PlainText")
        if not os.path.exists(path_plain):
            os.mkdir(path_plain)

        if self.choose_type_file:
            txt_file = self.new_file_name_finally
            txt_path = os.path.join(path_plain, txt_file)
            with open(txt_path, "a", encoding='utf-8') as f:
                np.savetxt(f, self.texts, fmt="%s", delimiter=", ")

            print(f"\t- Save PlainText in: {txt_path}")
            self.path_save_plain = txt_path
            return self.path_save_plain


        else:
            df_back = pd.DataFrame(self.data_line, columns=None)
            df_back.columns = range(df_back.shape[1])

            save_path = os.path.join(path_plain, self.new_file_name_finally)
            df = df_back.applymap(lambda x: pd.to_numeric(x, errors='ignore') if isinstance(x, str) else x)
            df.to_excel(save_path, startrow=0, index=False, columns=None, header=False)

            print(f"\t- Save PlainText in: {save_path}\n")
            self.path_save_plain = save_path
            return self.path_save_plain