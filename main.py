from typing import List
import os 

import pandas as pd 
from pypdf import PdfMerger 
from tqdm import tqdm 

from util.helper_func import * 
from var.program_var import * 


if __name__ == "__main__":
    print("- Please input the directory where the files located.")
    files_dir = input("Directory: ") 
    files_dir = files_dir.replace("\\", "/") 
    
    if files_dir[-1] == "/": 
        files_dir = files_dir[:-2]

    if os.path.isdir(files_dir) is False: 
        raise NotADirectoryError("!!! That ain't no a legit directory dawg !!!") 

    print("""
- Please choose the file type. 
[1] - CSV 
[2] - Excel (Only the first sheet would be chosen) 
[3] - Why not both (CSV and Excel) 
[4] - PDF""")
    files_type = input("Option number: ") 

    try: 
        files_type = int(files_type) 
        
    except: 
        raise ValueError("!!! That ain't no a number dawg !!!") 
        
    if files_type < 1 or files_type > 4: 
        raise ValueError(f"!!! That ain't no option {files_type} dawg !!!") 

    if 1 <= files_type <= 3: 
        print(f"""
- Do you want to add the source file path into the output file? 
E.g. The output file will have a new column called "SourcePath" and the files in {files_dir}/<subfolder>/files will have the value "<subfolder>/files" in that column. """)
        source_path_option = input("Please input Y or N (Yes or No): ") 

    else: 
        source_path_option = "N" 
        
    if source_path_option.upper() == "Y": 
        source_path_mode = True 

    elif source_path_option.upper() == "N": 
        source_path_mode = False 

    else: 
        raise ValueError("!!! Please just input Y or N (Y means Yes and N means No) dawg !!!")  

    file_path_list = [] 
    file_path_all_file_list = get_all_file_paths(files_dir)
    for extension in FILE_TYPE_DICT[files_type]["extension"]: 
        file_path_list.extend([p for p in file_path_all_file_list if extension in p and "TableStacker_Mathless/" not in p]) 
    print(f"""
{len(file_path_list)} files found in {files_dir}""")

    output_df = pd.DataFrame() 
    fail_list = [] 
    match files_type: 
        case 1: 
            for file_path in tqdm(file_path_list): 
                try: 
                    if source_path_mode: 
                        if len(file_path.replace(files_dir, "").split("/")) > 1: 
                            source_path = file_path.replace(files_dir, "")
                            
                        df = pd.read_csv(file_path) 
                        df["SourcePath"] = source_path 
                    
                    else: 
                        df = pd.read_csv(file_path) 
                    
                    output_df = pd.concat([output_df, df]) 
                
                except: 
                    fail_list.append(file_path)

        case 2: 
            for file_path in tqdm(file_path_list): 
                try: 
                    if source_path_mode: 
                        if len(file_path.replace(files_dir, "").split("/")) > 1: 
                            source_path = file_path.replace(files_dir, "")
                            
                        try: 
                            df = pd.read_excel(file_path, header=None, sheet_name=0) 
                        except: 
                            df = pd.read_excel(file_path, header=None)
                            
                        df = df.dropna(how='all').dropna(how='all', axis=1) 
                        headers = df.iloc[0]
                        df = pd.DataFrame(df.values[1:], columns=headers) 
            
                        df["SourcePath"] = source_path  
    
                    else: 
                        try: 
                            df = pd.read_excel(file_path, header=None, sheet_name=0) 
                        except: 
                            df = pd.read_excel(file_path, header=None)
                            
                        df = df.dropna(how='all').dropna(how='all', axis=1) 
                        headers = df.iloc[0]
                        df = pd.DataFrame(df.values[1:], columns=headers)
                    
                    output_df = pd.concat([output_df, df]) 
                
                except: 
                    fail_list.append(file_path) 

        case 3: 
            for file_path in tqdm(file_path_list): 
                if ".csv" in file_path.split("/")[-1]: 
                    for file_path in file_path_list: 
                        try: 
                            if source_path_mode: 
                                if len(file_path.replace(files_dir, "").split("/")) > 1: 
                                    source_path = file_path.replace(files_dir, "")
                                    
                                df = pd.read_csv(file_path) 
                                df["SourcePath"] = source_path 
                            
                            else: 
                                df = pd.read_csv(file_path) 
                            
                            output_df = pd.concat([output_df, df]) 
                        
                        except: 
                            fail_list.append(file_path)
                        
                elif ".xls" in file_path.split("/")[-1]: 
                    try: 
                        if source_path_mode: 
                            if len(file_path.replace(files_dir, "").split("/")) > 1: 
                                source_path = file_path.replace(files_dir, "")
                            
                            try: 
                                df = pd.read_excel(file_path, header=None, sheet_name=0) 
                            except: 
                                df = pd.read_excel(file_path, header=None)
                                
                            df = df.dropna(how='all').dropna(how='all', axis=1) 
                            headers = df.iloc[0]
                            df = pd.DataFrame(df.values[1:], columns=headers) 
                
                            df["SourcePath"] = source_path 
                        
                        else: 
                            try: 
                                df = pd.read_excel(file_path, header=None, sheet_name=0) 
                            except: 
                                df = pd.read_excel(file_path, header=None)
                                
                            df = df.dropna(how='all').dropna(how='all', axis=1) 
                            headers = df.iloc[0]
                            df = pd.DataFrame(df.values[1:], columns=headers)
                        
                        output_df = pd.concat([output_df, df]) 
                    
                    except: 
                        fail_list.append(file_path) 
        
        case 4: 
            pdf_merger = PdfMerger() 

            for file_path in tqdm(file_path_list): 
                try: 
                    pdf_merger.append(file_path) 
                
                except: 
                    fail_list.append(file_path) 
            
            if not os.path.exists(f"{files_dir}/TableStacker_Mathless/"):
                os.mkdir(f"{files_dir}/TableStacker_Mathless/")
                
            pdf_merger.write(f"{files_dir}/TableStacker_Mathless/result.pdf")
            pdf_merger.close() 

    if files_type != 4: 
        if not os.path.exists(f"{files_dir}/TableStacker_Mathless/"):
            os.mkdir(f"{files_dir}/TableStacker_Mathless/")
                
        output_df.to_csv(f"{files_dir}/TableStacker_Mathless/result.csv", index=False) 
        

    fail_file_df = pd.DataFrame(
        {"FailedFile": fail_list}, 
        index=[i for i in range(len(fail_list))]
    ) 
    fail_file_df.to_csv(f"{files_dir}/TableStacker_Mathless/fail_log.csv", index=False) 

    print(f"""
Done. 
Output file and fail log are in {files_dir}/TableStacker_Mathless/.""")
    exit_stdin = input("""
Press Enter to exit...""") 
    print("Peace.") 
    