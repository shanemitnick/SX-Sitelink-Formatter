import codecs
import os
import stat
import time
from datetime import datetime
import pandas as pd
from re import search


# FILE PATH FOR FILES TO BE FORMATTED
LOAD_PATH = "/Users/shanemitnick/Python/storexpress/NetSuite Formatter/v2/sitelink_files"

# FILE PATH FOR FORMATTED .XLS FILES TO BE PUT INTO
SAVE_PATH = "/Users/shanemitnick/Python/storexpress/NetSuite Formatter/v2/output_files"

LOC_HYP = {'L001 - STORExpress Mt. Pleasant': 'MP',  # 32937 # CHECK ABBREVIATION
           'L002 - STORExpress Turtle Creek': 'TC',  # 33507
           'L003 - STORExpress  Warren': 'WR',  # 33348 # CHECK ABBREVIATION
           'L004 - STORExpress Bridgeville': 'BV',  # 33497
           'L005 - STORExpress McKees Rocks': 'RX',  # 33807
           'L006 - STORExpress  Brinton': 'BR',  # 33876
           'L007 - STORExpress  Murrysville': 'MV',  # 33940
           'L008 - STORExpress  Robinson': 'RB',  # 34011
           'L009 - STORExpress New Kensington': 'NK',  # 34107 # CHECK ABBREVIATION
           'L010 - STORExpress Southside': 'SS',  # 34232
           'L011 - STORExpress  Etna': 'ET',  # '34305'
           'L012 - STORExpress Office Express': 'OE',  # 34306
           'L013 - Rossi\'s Pop-Up Marketplace': 'RM'  # 36357 # CHECK ABBREVIATION
           }

RECEIPTS_ACCOUNT_NUMBERS = {'Rent': 40000,
                            'Recurring': 40008,
                            'Late Fee': 40008,
                            'NSF Fee': 40008,
                            'Admin Fee': 40008,
                            'Insurance': 40009,
                            'Other': 40008,
                            'Misc Deposit': 40008,
                            'Security Deposit': 22210,
                            'Merchandise': 40010,
                            'Tax 1': 20102,
                            'Tax 2': 20102,
                            }

DEPOSIT_ACCOUNT_NUMBERS = {'L001 - STORExpress Mt. Pleasant': 10205,
                           'L002 - STORExpress Turtle Creek': 10203,
                           'L003 - STORExpress  Warren': 10015,
                           'L004 - STORExpress Bridgeville': 10202,
                           'L005 - STORExpress McKees Rocks': 10003,
                           'L007 - STORExpress  Murrysville': 10303,
                           'L006 - STORExpress  Brinton': 10207,
                           'L008 - STORExpress  Robinson': 10023,
                           'L009 - STORExpress New Kensington': 10302,
                           'L010 - STORExpress Southside': 10201,
                           'L011 - STORExpress  Etna': 10022,
                           'L012 - STORExpress Office Express': 10024,
                           'L013 - Rossi\'s Pop-Up Marketplace': 10206,
                           'green apple': 19001
                           }

SUBSIDIARY_ID = {'L001 - STORExpress Mt. Pleasant': 111,
                 'L002 - STORExpress Turtle Creek': 84,
                 'L003 - STORExpress  Warren': 100,
                 'L004 - STORExpress Bridgeville': 110,
                 'L005 - STORExpress McKees Rocks': 94,
                 'L007 - STORExpress  Murrysville': 90,
                 'L006 - STORExpress  Brinton': 97,
                 'L008 - STORExpress  Robinson': 96,
                 'L009 - STORExpress New Kensington': 80,
                 'L010 - STORExpress Southside': 71,
                 'L011 - STORExpress  Etna': 95,
                 'L012 - STORExpress Office Express': 89,
                 'L013 - Rossi\'s Pop-Up Marketplace': 116
                 }

LOCATION_ID = {'L001 - STORExpress Mt. Pleasant': 18,
               'L002 - STORExpress Turtle Creek': 3,
               'L003 - STORExpress  Warren': 4,
               'L004 - STORExpress Bridgeville': 5,
               'L005 - STORExpress McKees Rocks': 6,
               'L007 - STORExpress  Murrysville': 8,
               'L006 - STORExpress  Brinton': 7,
               'L008 - STORExpress  Robinson': 9,
               'L009 - STORExpress New Kensington': 10,
               'L010 - STORExpress Southside': 11,
               'L011 - STORExpress  Etna': 12,
               'L012 - STORExpress Office Express': 13,
               'L013 - Rossi\'s Pop-Up Marketplace': 14
               }


def get_doc(f_path):
    """ Open doc and return as list for each line from the codecs.open function


    :param f_path: path to file that is desired to be opened
    :return doc (list): list of string of the doc
    """

    f = codecs.open(f_path, 'r', encoding="utf-16", errors="backslashreplace")
    doc = []
    for line in f:
        doc.append(line)

    return doc


def get_location_info(doc):
    """Returns the location information for the given file

    :param doc:(String) doc string list
    :return:location information
    """

    return doc[-3].split('\t')


def get_greenapple(path, deposit_filename):
    """ Gets the greenapple value from the appropriate filename

    :param path: Name of the file path to search
    :param deposit_filename: Name of the file
    :return ga_sum (float): The value of the total Green Apple line items.
    """

    # lines with green apple
    ga_lines = []
    i = 0
    doc = get_doc(path + "/" + deposit_filename)
    ga_sum = 0

    # find areas with green apple mentioned
    while i < len(doc):
        if search("Green Apple", doc[i]):
            ga_lines.append(i)
        i += 1

    # Loop thorugh lines that have green apple values
    for g in ga_lines:
        val = float(doc[g].split("\t")[-1])
        # sum values
        ga_sum += val

    # return values
    return ga_sum


def get_daily_deposit_filename_considering_location(path, ms_filename, loc):
    """ Returns the string of the path of the DailyDeposit Filename

    :param path: (str) the path of the folder to find
    :param ms_filename: (str) the complimentary management summary filename
    :param loc: (str) location ID to be considered -- 3 digit string
    :return: dd_filename(str): the filename of complimenting dailydeposit filename
    """
    # create filename to be found
    date = ms_filename[17: 26]
    fname = 'DailyDeposit' + date

    for f in os.listdir(path):
        # Not looking at hidden files
        if f[0] != '.':
            # Check if file starts with our formatted filename (DailyDeposit_ + Date)
            if f.startswith(fname):
                # get location information for this file
                doc = get_doc(path + "/" + f)
                location_info = get_location_info(doc)
                # we have location info, now be sure its the right location
                if location_info[1] == loc:
                    return f

    # No File found if at this point
    print("!!!!!! NOT MATCHING FILE FOR " + ms_filename + " COULD BE FOUND !!!!!!!!!!!")

    return None


def make_dataframe_deposits(deposits_dict, loc_info):
    """ Creates a DataFrame for deposits from the given deposits_dict. The resulting Dictionary has data for
    Memo, account, Debit, and Credit wit


    :param deposits_dict: (Dict) Dictionary of account titles and values from the given file.
    :param loc_info: (List of Strings) Location information from the Management Summary File
    :return: DataFrame of the given dictionary
    """

    formatted_dict = {'Account': [],
                      "Memo": [],
                      "Debit": [],
                      "Credit": []}

    for deposit_key in deposits_dict:
        # Green Apple Check
        if deposit_key == 'green apple':
            formatted_dict['Account'].append(DEPOSIT_ACCOUNT_NUMBERS[deposit_key])
        else:
            formatted_dict['Account'].append(DEPOSIT_ACCOUNT_NUMBERS[loc_info[1]])

        formatted_dict['Memo'].append(deposit_key)
        formatted_dict['Debit'].append(deposits_dict[deposit_key][0])
        formatted_dict['Credit'].append(deposits_dict[deposit_key][1])

    return pd.DataFrame.from_dict(formatted_dict)


def get_deposits(doc, green_apple):
    """
        This function gets the deposits from the file given

    :param doc: (list of string) List of strings of document broken down
    :param green_apple: (float) Green Apple Value from Daily Deposit Sheet
    :return: Return a dictionary containing the name of the account, and the values
            being the credit from the file, and 0 for debit
    """

    data = doc[1].split("\t")

    cash = float(data[1])
    check = float(data[2])
    credit_card = float(data[3])
    ach = float(data[4])

    deposits_dict = {}
    deposits_dict["cash & check"] = [cash + check, 0]
    deposits_dict["ACH"] = [ach, 0]
    deposits_dict["credit card"] = [credit_card - green_apple, 0]
    deposits_dict['overnight charges'] = [0, 0]
    deposits_dict["green apple"] = [green_apple, 0]

    return deposits_dict


def get_receipts(doc):
    """
        This function is for getting the receipts section of the document. Pulls data from management summary
    document (which is given as list of strings) and returns in a dictionary.

    :param doc: (list of Strings) The Management Summary broken down to be processed.
    :return receipts (Dict): The title of the account with a credit of 0 and a debit value found in the file as a float.
    """
    receipts = {}
    # section from doc that has raw data
    raw_data = doc[5:17]

    # process raw data and split values to title and value
    for row in raw_data:
        split_row = row.split('\t')
        row_title = split_row[1]
        daily_val = split_row[3]

        receipts[row_title] = [0, float(daily_val)]

    return receipts


def make_dataframe_receipts(receipts_dict):
    """ Convert the given receipts dict to a properly formatted DataFrame.

    :param receipts_dict: (dict) Dictionary of receipts to be converted to DataFrame. Pulling Account numbers from
        RECEIPTS_ACCOUNT_NUMBERS dictionary.
    :return: DataFrame of the given dictionary
    """

    formatted_dict = {'Account': [],
                      "Memo": [],
                      "Debit": [],
                      "Credit": []}

    for k in receipts_dict:
        formatted_dict['Account'].append(RECEIPTS_ACCOUNT_NUMBERS[k])
        formatted_dict['Memo'].append(k)
        formatted_dict['Debit'].append(receipts_dict[k][0])
        formatted_dict['Credit'].append(receipts_dict[k][1])

    return pd.DataFrame.from_dict(formatted_dict)


def get_date(external_id):
    """ Get the current date from the external_id string and place in datetime format

    :param external_id: (String) external_id string for a store - ET03132021
    :return: Date object of date
    """

    date = external_id[2:]

    dt = datetime.strptime(date, "%m%d%Y")

    return dt.strftime("%m/%d/%Y")


def get_external_id(ms_filename, loc_info):

    """ Returns formateed Extrenal ID

    :param ms_filename: (string) File name to extract date from
    :param loc_info: (list) location information to refer to abbreviation in LOC_HYP in
    :return: formatted external ID -- ex. "ET06212020" -- 'SXDDMMYYYY'
    """

    date = ms_filename.split("_")

    day = date[1][-2:]
    month = date[1][-4:-2]
    year = date[1][0:4]

    return LOC_HYP[loc_info[1]] + month + day + year


def process_document(path, ms_filename, dd_filename):
    """ Returns a processed document that brings together accounts from the given Management Summary File
    and given Daily Deopsit file. It is assume these files go together

    :param path: (String) The Path where the string filename can be found.
    :param ms_filename: (String) The string of the filename and extension of the Management Summary file.
    :param dd_filename: (String) The stirng of the filename and extension of the Daily Deposit file
        -- The ms_filename and dd_filename should be a pair (same store for same day)
    :return netsuite_df: DataFrame of completed document, formatted for Netsuite file upload.
    """

    ms_doc = get_doc(path + "/" + ms_filename)
    location_info = get_location_info(ms_doc)

    # Get Green Apple Value
    greenapple_value = get_greenapple(path, dd_filename)

    # Get Receipts into a Dictionary
    receipts_dict = get_receipts(ms_doc)
    deposit_dict = get_deposits(ms_doc, greenapple_value)

    # Create those Dictionaries into DataFrames
    receipts_df = make_dataframe_receipts(receipts_dict)
    deposit_df = make_dataframe_deposits(deposit_dict, location_info)

    # Combine those DataFrames and produce a netsuite_df
    netsuit_df = pd.concat([receipts_df, deposit_df])
    netsuit_df.reset_index(drop=True, inplace=True)
    external_id = get_external_id(ms_filename, location_info)
    # set columns that do not change
    netsuit_df['External ID'] = external_id
    netsuit_df['Date'] = get_date(external_id)
    netsuit_df['Subsidiary ID'] = SUBSIDIARY_ID[location_info[1]]
    netsuit_df['Location ID'] = LOCATION_ID[location_info[1]]

    # reordering of columns
    column_order = ['External ID', 'Date', 'Account', 'Memo', 'Debit', 'Credit', 'Subsidiary ID', 'Location ID']
    netsuit_df = netsuit_df.reindex(columns=column_order)

    #  Print check for netsuite_df to be sure it balances
    print(f'Check for {external_id}: ')
    print(f'Green Apple Charge: {greenapple_value}')
    print(f'Debit Sum: {netsuit_df["Debit"].sum():2f}')
    print(f'Credit Sum: {netsuit_df["Credit"].sum():2f}')
    print("\n")

    return netsuit_df


def add_doc_to_master_dict(all_docs, netsuite_doc, loc_info):
    """
    Add the netsuite doc to the master list

    :param all_docs: (dict) dict of all documents with locations as key
    :param netsuite_doc: (DataFrame) The DataFrame to be added to the master list of processed documents.
    :param loc_info: The location info the be used -- the key to store it under
    :return: null -- master dict (all_documents) is updated.
    """

    if loc_info[1] in all_docs:
        all_docs[loc_info[1]].append(netsuite_doc)
    else:
        all_docs[loc_info[1]] = [netsuite_doc]

def create_document_title(loc_hyp):
    """ Returns the file name in the format :

    :param loc_hyp:
    :return:
    """


def delete_files(path):
    """ This will delete all files in a path. PERMANENT BE CAREFUL!

    :param path: (String) File path to be deleted.
    :return: null - folder is deleted
    """
    for f in os.listdir(path):
        # if not a hidden file
        if f[0] != ".":
            os.remove(path + "/" + f)




def process_docs(load_path):
    """ Process Documents from the given file path.

    :param load_path: (string) The Path to folder where Management Summary and Daily Deposits are.
    :return all_documents: (dict) Dictionary of documents by location
    """
    all_documents = {}

    # Keep Track of Error Messages to tell user what may of gone wrong
    error_messages = []

    print("PROCESSING DOCS -----------")
    files_sorted_by_date = []

    # create list of of files in order of creation, to loop through in order.
    filepaths = [os.path.join(load_path, file) for file in os.listdir(load_path)]
    file_statuses = [(os.stat(filepath), filepath) for filepath in filepaths]
    files = ((status[stat.ST_CTIME], filepath) for status, filepath in file_statuses if
             stat.S_ISREG(status[stat.ST_MODE]))

    ordered_filenames = []

    for creation_time, filepath in sorted(files):
        file = filepath.split("/")[-1]
        if file[0] != ".":
            ordered_filenames.append(file)

    print("BREAK  \n\n")

    for file in ordered_filenames:
        # avoiding hidden files
        if file[0] != ".":
            if file.startswith("ManagementSummary"):
                print("-------------------------------------- Opening: " + file + "--------------------------------------")
                # Open Doc and get Location information for each management summary file
                ms_doc = get_doc(load_path + "/" + file)
                loc_info = get_location_info(ms_doc)
                print(loc_info)

                # Daily Deposit // Green Apple Value Retrevial
                try:
                    daily_deposit_filename = get_daily_deposit_filename_considering_location(load_path, file, loc_info[1])
                    print("using daily deposit file: " + daily_deposit_filename + " for file " + file)
                    greenapple_value = get_greenapple(load_path, daily_deposit_filename)

                    netsuite_doc = process_document(load_path, file, daily_deposit_filename)

                    add_doc_to_master_dict(all_documents, netsuite_doc, loc_info)

                except TypeError:
                    # Getting Date Information to Show User
                    external_id = get_external_id(file, loc_info)
                    date = get_date(external_id)
                    message = "!!!!!!!!!!! NO DEPOSITE FILE FOR " + loc_info[1] + " ON DATE " + date + " !!!!!!!!!!!!!"
                    error_messages.append(message)
                    print(message)
                    pass

                print("\n\n")

    return all_documents, error_messages

def save_docs(all_documents):
    """ Save all documents in the given dictionary to the save path.

    :param all_documents: (dict) Dictionary of all documents.
    :param save_path:
    :return:
    """
    print('saving docs ---------------')
    # save dictionaries to file
    for key in all_documents.keys():
        now = datetime.today()
        title = LOC_HYP[key] + "_ending_" + now.strftime('%m_%d_%y')

        list_of_docs = all_documents[key]

        filename = "etna_test"
        store_file_df = pd.concat(list_of_docs)
        store_file_df.to_csv(f'{SAVE_PATH}/{title}.csv', index=False)


def print_errors(errors):
    """ Prints out all errors that have been found and are in the list of given errors.

    :param errors: (list) The list of errors that want to be printed
    :return: null - printed errors to screen
    """
    # check if list is emtpy
    if len(errors) == 0:
        print('no errors found')
        return

    for e in errors:
        print(e)


def driver_code():
    # process and save DataFrames into documents dictionary
    documents, error_messages = process_docs(LOAD_PATH)

    print_errors(error_messages)
    # save DataFrames to excel sheets by each store
    save_docs(documents)
    # delete the files in the save path
    # delete_files(LOAD_PATH)
    # place all files in a folder for storage.

driver_code()