# importing required classes
import os
import re
import sys
from pypdf import PdfReader
import pandas as pd
from Transaction import Transaction


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# Function to parse the transaction data
def parse_transactions(data, month):
    #

    transactions = []
    i = 0

    while i < len(data):
        # Create a new Transaction instance
        new_transaction = Transaction()

        # Date
        new_transaction.date = data[i] + " " + data[i + 1]
        i += 2

        # Type: Collect elements until we reach the amount
        type_string = []
        while i < len(data) and not (isfloat(data[i][-4:])):
            type_string.append(data[i])
            i += 1

        # Combine the collected description elements
        new_transaction.type = ' '.join(type_string)

        # Amount
        if i < len(data) and '.' in data[i] and '$' not in data[i]:
            new_transaction.amount = float(''.join(data[i].split(',')))
            i += 1

        # Balance
        if i < len(data) and '.' in data[i] and '$' not in data[i]:
            balance_str = data[i].split(',')
            new_transaction.balance = float(''.join(balance_str))
            i += 1

        # Description
        description_string = []
        # pattern = re.compile(r'^\*.*')
        while i < len(data) and not (any(re.match(pattern, data[i]) for pattern in [month, "SBSAV", r'^\*'])):
            description_string.append(data[i])
            i += 1
        new_transaction.description = ' '.join(description_string)

        # Add the transaction to the list only if it has meaningful data
        if new_transaction.type != "" and new_transaction.amount > 0 and new_transaction.balance != "":
            transactions.append(new_transaction)

    return transactions


if __name__ == '__main__':
    # get the current folder
    folder_path = os.getcwd()

    # loop through each pdf file
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)

            # creating a pdf reader object
            reader = PdfReader(file_path)

            my_transactions = []

            my_dict = {
                "Date": [],
                "Type": [],
                "Description": [],
                "Amount": [],
                "Balance": []
            }

            # loop through the pages
            for p in range(0, reader.get_num_pages()):
                print("reading page: ", p)
                # creating a page object
                page = reader.pages[p]
                # create a list of strings from page
                my_list = page.extract_text().split()

                # find the month
                month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                flag = 0
                month = ""
                for i in my_list:
                    if i in month_list:
                        flag = 1
                        month = i
                        break
                    if flag == 1:
                        break

                if flag == 0:
                    print("Month not found")
                    break

                # set the last element for each page
                first = my_list.index(month)

                new_list = my_list[first:len(my_list)]

                # Parse the transactions
                my_transactions = parse_transactions(new_list, month)

                # append data into dictionary each transaction
                for transaction in my_transactions:
                    my_dict["Date"].append(transaction.date)
                    my_dict["Type"].append(transaction.type)
                    my_dict["Description"].append(transaction.description)
                    my_dict["Amount"].append(transaction.amount)
                    my_dict["Balance"].append(transaction.balance)
                    transaction.print_me()
                    print("-----")

            df = pd.DataFrame(my_dict)
            df.to_csv(f'{filename.split(".")[0]}.csv', sep=',', index=False, encoding='utf-8')
