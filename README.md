# SX-Sitelink-Formatter
This Python script will be used to convert SiteLink POS data to an formatted upload file for Quickbooks.

## Usage
To use this script, the user must have (at least) one management summary file and one daily deposit store for 1 store and 1 corresponding day. 
NOTE: Managment Summary and Daily Deposit files must be in .txt format, not PDF.

Python 3.7 and Pandas must be installed. 

Either navigate to the file in an IDE and run the script, or in a terminal window navigate to the folder and run 'python netsuite_formatter.py.

### How it works
This script takes 2 files (Management Summary and Daily Deposit) to create the desired file. 
NOTE: Below are the PDF views of the files for demonstration use only and can be found in the sample_files_pdfs folder.

From the management summary the ** highlighted values are used **: 
<img width="825" alt="Screen Shot 2022-07-22 at 4 30 02 PM" src="https://user-images.githubusercontent.com/10816901/180557423-eb90dea6-c2ea-4b0e-91aa-8af10238ca83.png">

From the daily deposit: 
<img width="825" alt="image" src="https://user-images.githubusercontent.com/10816901/180558118-cd66faa2-331c-43b2-87b8-dca250599d27.png">

<img width="824" alt="Screen Shot 2022-07-22 at 4 30 16 PM" src="https://user-images.githubusercontent.com/10816901/180558326-04d2b7d7-486f-4d82-8b00-388fe0e97a8b.png">

This data is matched with account infomration stored in dictionaries at the top of the python file and are used to create the follow file format: 

<img width="562" alt="Screen Shot 2022-07-22 at 4 33 24 PM" src="https://user-images.githubusercontent.com/10816901/180559075-1f1a3f77-dbea-41fb-b5eb-4afee108a0b6.png">
