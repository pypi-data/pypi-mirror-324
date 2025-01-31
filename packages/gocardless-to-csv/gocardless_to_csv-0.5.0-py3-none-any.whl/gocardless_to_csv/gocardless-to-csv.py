#!/usr/bin/env python3
# Script that pulls data from GoCardless API (formerly Nordigen) and saves it to a CSV file, suitable for parsing with hledger/ledger/...
# We are using https://github.com/nordigen/nordigen-python library to interact with the API.
import os
from datetime import datetime
import configparser
import argparse
import json
import csv

from nordigen import NordigenClient


def configure_new_connection(client, config, args):
    """
    Configure connection to a new bank via several interactive prompts
    """
    if args.sandbox:
        print("Using Sandbox Finance (SANDBOXFINANCE_SFIN0000)")
        institution={}
        institution['id']="SANDBOXFINANCE_SFIN0000"
        institution['transaction_total_days']=90
        institution['max_access_valid_for_days']=90
    else:
        country_code = input("Enter the country code in ISO 3166 format: ")

        # Get all institution by providing country code in ISO 3166 format
        institutions = client.institution.get_institutions(country_code)
        try:
            from pyfzf.pyfzf import FzfPrompt
            fzf = FzfPrompt()

            institution_name=(fzf.prompt([i['name'] for i in institutions]))[0]
        except ModuleNotFoundError:
            print("Please install pyfzf for interactive selection")
            print("pip install pyfzf")
            print("Alternatively, you can select the institution name manually from the list below")
            for i in institutions:
                print(i)
            institution_name = input("Enter the name of the institution: ")

        institution = [i for i in institutions if i['name']==institution_name][0]

        print(institution)

    your_ref = input("Name this setup (needed if you want to delete it later): ")

    # Initialize a new session
    init = client.initialize_session(
        institution_id=institution['id'],
        redirect_uri="http://localhost",
        reference_id=your_ref,
        max_historical_days=institution['transaction_total_days'], 
        access_valid_for_days=institution['max_access_valid_for_days']
    )

    # Get requisition_id and link to initiate authorization process with a bank
    link = init.link # bank authorization link
    requisition_id = init.requisition_id

    print(f"Go to this link to finish the authorization: {link}")

    # TODO: we can open a small server on a random port, put it into redict_uri and listen for the callback
    # then tell the user that everything is set up correctly

def list_accounts(client, config, args):
    """
    List account ids from all linked banks
    """
    requisitions = client.requisition.get_requisitions()
    for req in requisitions['results']:
        print(f"{req['reference']} (status={req['status']}):")
        for account in req['accounts']:
            print(f"  account: {account}")

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

def fetch(client, config, args):
    """
    Fetch transactions from all linked banks and save them into output files
    """
    # fetch transactions from existing connection
    requisitions = client.requisition.get_requisitions()
    for req in requisitions['results']:
        reference = req['reference']
        if args.reference:
            if reference != args.reference:
                continue
        print(f"Processing {reference}")
        for account in req['accounts']:
            acc = client.account_api(id=account)
            try:
                if args.year:
                    date_from = f"{args.year}-01-01"
                    current_year = datetime.now().year
                    if args.year == current_year:
                        date_to = datetime.now().strftime("%Y-%m-%d")
                    else:
                        date_to = f"{args.year}-12-31"
                elif args.month:
                    date_from = f"{args.month}-01"
                    date_to = last_day_of_month(datetime.fromisoformat(date_from))
                    today = datetime.now()
                    if date_to > today:
                        date_to = datetime.now().strftime("%Y-%m-%d")
                    else:
                        date_to = date_to.strftime("%Y-%m-%d")
                else:
                    date_from = args.start
                    date_to = args.end
                transactions = acc.get_transactions(date_from=date_from, date_to=date_to)
            except Exception as e:
                print(f"  Error fetching transactions for {account}: {e}")
                continue

            if args.debug:
                print(transactions)
            if config[account]['file']:
                if date_from:
                    # Create the filename based on the date_from, assuming filename contains strftime format specifiers
                    filename=datetime.strftime(datetime.fromisoformat(date_from), config[account]['file'])
                    dirname=os.path.dirname(filename)
                    if not os.path.exists(dirname):
                        os.makedirs(dirname)
                else:
                    filename=config[account]['file']
                with open(filename, 'w') as f:
                    json.dump(transactions,f,indent=2)
                print(f"  {account}[{date_from}..{date_to}] saved to {filename}")
            else:
                print(json.dumps(transactions,indent=2))

def convert(client,config,args):
    """
    Convert GoCardless JSON file to CSV
    """
    # Read the JSON file
    with open(args.json_file, 'r') as f:
        transactions = json.load(f)

    if args.pending:
        transactions = transactions['transactions']['pending']
    else:
        transactions = transactions['transactions']['booked']

    with open(args.csv_file, 'w') as f:
        fieldnames = ["bookingDate", "valueDate", "operation", "payee", "transactionAmount", "instructedAmount", "description", "GoCardlessRef"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for trx in transactions:
            # This is heavily based on tariochbctools
            if "transactionId" in trx:
                row = {
                    "GoCardlessRef": trx["transactionId"],
                }
            else:
                row = {}

            if "creditorName" in trx:
                row["payee"] = trx["creditorName"]
                row["operation"] = "credit"
            if "debtorName" in trx:
                row["payee"] = trx["debtorName"]
                row["operation"] = "debit"
            if "currencyExchange" in trx:
                instructedAmount = trx["currencyExchange"]["instructedAmount"]
                row["instructedAmount"] = (
                    instructedAmount["currency"] + " " + instructedAmount["amount"]
                )
            row['bookingDate'] = trx["bookingDate"]
            row['valueDate'] = trx["bookingDate"]
            description = ""
            if "remittanceInformationUnstructured" in trx:
                description += trx["remittanceInformationUnstructured"]
            if "remittanceInformationUnstructuredArray" in trx:
                description += " ".join(trx["remittanceInformationUnstructuredArray"])
            row['description'] = description
            row["transactionAmount"] = trx["transactionAmount"]["currency"] + " " + trx["transactionAmount"]["amount"]
            writer.writerow(row)

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="GoCardless fetcher/parser/CSV converter")
    parser.add_argument("--config", type=str, help="Path to the config file", default="~/.config/gocardless-to-csv/config.ini")
    parser.add_argument("--debug", action='store_true', help="Print debug output")

    subparsers = parser.add_subparsers(help='subcommand help', title="valid commands")

    parser_setup = subparsers.add_parser('setup', help='Setup a new connection to a bank')
    parser_setup.add_argument("--sandbox", action='store_true', help="Use Sandbox Finanace (provided by GoCardless for testing)")
    parser_setup.set_defaults(func=configure_new_connection)

    parser_list = subparsers.add_parser('list', help='List accounts for existing connections')
    parser_list.set_defaults(func=list_accounts)

    parser_fetch = subparsers.add_parser('fetch', help='Fetch transactions from GoCardless and save then to JSON file')
    parser_fetch.add_argument("--start", type=str, help="Start date, YYYY-MM-DD")
    parser_fetch.add_argument("--end", type=str, help="End date, YYYY-MM-DD")
    parser_fetch.add_argument("--reference", type=str, help="Process only this reference")
    parser_fetch.add_argument("--year", type=int, help="YYYY, equivalent of --start <year>-01-01 --end <year>-12-31 or current date, whichever is earler")
    parser_fetch.add_argument("--month", type=str, help="YYYY-MM, equivalent of --start <year>-01-01 --end <year>-12-31 or current date, whichever is earler")
    parser_fetch.set_defaults(func=fetch)

    parser_convert = subparsers.add_parser('convert', help='Convert GoCardless JSON file to CSV')
    parser_convert.add_argument("json_file", type=str, help="Path to the input JSON file")
    parser_convert.add_argument("csv_file", type=str, help="Path to the output CSV file")
    parser_convert.add_argument("--pending", action='store_true', help="Process pending transactions instead of booked")
    parser_convert.set_defaults(func=convert)

    args = parser.parse_args()

    # initialize Nordigen client and pass SECRET_ID and SECRET_KEY, which we read from the config file  
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(args.config))

    if not 'nordigen' in config:
        print("Please configure the Nordigen API credentials in the config file.")
        exit(1)

    client = NordigenClient(
        secret_id=config['nordigen']['SECRET_ID'],
        secret_key=config['nordigen']['SECRET_KEY']
    )
    client.generate_token()

    try:
        args.func(client, config, args)
    except AttributeError:
        parser.print_help()
