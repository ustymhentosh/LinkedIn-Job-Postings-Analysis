# LinkedIn-Job-Postings-Analysis

Analysis of a big dataset of job postings scraped from LinkedIn. Big Data course project.

Data: https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024?select=job_summary.csv

### Сontent

`./data`

- contains three additional files that were used in analysis. Due to repository limitations main source files with LinkedIn scraped data are not included.

- <span style="color:red">**!**</span> If you want to run code from this repo be sure to include files from kaggle into data folder.

`./`

- `master.ipynb` - one of the main data processing notebooks containing Geographical Analysis, Occupation Type analysis, Education Level Requirements analysis, States Ranking, Education statistics for Jobs.
- `education.ipynb` - small notebok that extracts education type from _job_summary.csv_ Generates files needed for master.ipynb.
- `job_titles.ipynb` - notebook for maping job titles from _linkedin_job_postings.csv_ into predefined number of jobs. Generates _result_mini_llm_v0.json_ needed for master.ipynb.
- `education_dct.json, result_mini_llm_v0.json` - help files for education and job title processing.

`./cli app`

- contains files for small terminal script that creates report based on your skills.
