from pprint import pprint
from openpyxl import load_workbook

class XlsxImport:
    def import_into_list(self, file_name):
        wb2 = load_workbook(file_name)
        sheet = wb2.active
        rows = sheet.max_row
        # cols = sheet.max_column
        items = []
        for i in range(7, rows + 1):
            items_vals = []

            for j in [7,8,13,14]:
                u = sheet.cell(row=i, column=j).value
                if (j == 13 and str(u) == '-'):
                    items_vals.append(sheet.cell(row=i, column=15).value)
                    continue
                if (j == 14 and str(u) == '-'):
                    items_vals.append(sheet.cell(row=i, column=16).value)
                    continue
                items_vals.append(sheet.cell(row=i, column=j).value)

            items.append(items_vals)
        items.pop(-1)
        for i in items:
            i.append(round(i[3]/i[2], 2))
        return items

if __name__ == "__main__":
    i = XlsxImport()
    pprint(i.import_into_list('obor.xlsx'))