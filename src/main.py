import sender

def main():
    from data.all import data
    sender.send_data_all(data)
    create_spreadsheet(data)

def create_spreadsheet(data):
    from gdrive.main import sheet, SPREADSHEET_ID

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='A1:1').execute()

    col_names = result.get('values', [[]])[0]

    r = result['range']
    last_col_name = r[r.index(':')+1:-1]

    values = [
        [
            row.get(col_name, '')
            for col_name in col_names
        ]
        for row in data
    ]

    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
            range='A2:' + last_col_name + str(len(values) + 1),
            body={ 'values': values },
            valueInputOption='RAW').execute()

if __name__ == '__main__':
    main()