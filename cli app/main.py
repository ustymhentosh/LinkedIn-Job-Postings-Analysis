import pandas as pd
from plots import Plots, create_html_file, combine_htmls
import webbrowser
import time

TITLE = r"""
    _____            __                                            __                                         
   /     |          /  |                                          /  |                                        
   $$$$$ |  ______  $$ |____          ______   _______    ______  $$ | __    __  ________   ______    ______  
      $$ | /      \ $$      \        /      \ /       \  /      \ $$ |/  |  /  |/        | /      \  /      \ 
 __   $$ |/$$$$$$  |$$$$$$$  |       $$$$$$  |$$$$$$$  | $$$$$$  |$$ |$$ |  $$ |$$$$$$$$/ /$$$$$$  |/$$$$$$  |
/  |  $$ |$$ |  $$ |$$ |  $$ |       /    $$ |$$ |  $$ | /    $$ |$$ |$$ |  $$ |  /  $$/  $$    $$ |$$ |  $$/ 
$$ \__$$ |$$ \__$$ |$$ |__$$ |      /$$$$$$$ |$$ |  $$ |/$$$$$$$ |$$ |$$ \__$$ | /$$$$/__ $$$$$$$$/ $$ |      
$$    $$/ $$    $$/ $$    $$/       $$    $$ |$$ |  $$ |$$    $$ |$$ |$$    $$ |/$$      |$$       |$$ |      
 $$$$$$/   $$$$$$/  $$$$$$$/         $$$$$$$/ $$/   $$/  $$$$$$$/ $$/  $$$$$$$ |$$$$$$$$/  $$$$$$$/ $$/       
                                                                      /  \__$$ |                              
                                                                      $$    $$/                               
                                                                       $$$$$$/                                
"""
for i in TITLE.split("\n"):
    print(i)
    time.sleep(0.05)

print(
    "Please enter all your skills seperated by commas;\n\
      ex. \033[92mData Analysis, Data Engineering, Python, PySpark, Databricks, SQL\033[0m"
)

raw_skills_string = input("> ")
skills_list = [i.strip() for i in raw_skills_string.split(",")]

### ----------------------- EDIT ----------------------- ###

# HERE some code that takes skills_list and returns job_list
# job_list example:
job_list = [
    "Chemistry Teachers, Postsecondary",
    "Police Identification and Records Officers",
    "Insulation Workers, Floor, Ceiling, and Wall",
    "Special Education Teachers, Kindergarten",
    "Civil Engineers",
    "Marriage and Family Therapists",
    "Installation, Maintenance, and Repair Workers, All Other",
    "Weighers, Measurers, Checkers, and Samplers, Recordkeeping",
    "Infantry Officers",
    "Geodetic Surveyors",
]

### ----------------------- EDIT ----------------------- ###

print("\nLoading Main Datasource... 1/4")
MAIN_DATASET_PATH = "./usa_dataset.csv"
df = pd.read_csv(MAIN_DATASET_PATH)

print("Visualizing main statistics... 2/4")
states_map = Plots.get_satates_map_for_jobs_list(df, job_list)
edu_req = Plots.get_education_req_plot_for_jobs_list(df, job_list)

print("Creation reports... 3/4 ")
states_map.write_html("states_map.html")
edu_req.write_html("jobs_education.html")

print("Creation reports... 4/4 ")
list_html = create_html_file(job_list)
combine_htmls(list_html, "./states_map.html", "./jobs_education.html", "result.html")

new = 2
webbrowser.open("result.html", new=new)
