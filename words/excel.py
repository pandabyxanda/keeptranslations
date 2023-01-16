from openpyxl import Workbook, load_workbook

workbook = load_workbook(filename="English words.xlsx")

sheets = workbook.sheetnames
sheet = workbook.active
print(f"{sheets = }")
print(f"{sheet = }")
res = sheet["B2:B3"]
res = sheet["B"]
# print(f"{res = }")
res = [x.value for x in res]
print(f"{res = }")

res = sheet["C"]
# print(f"{res = }")
res = [x.value for x in res]
print(f"{res = }")
# wb = Workbook()
#
# # grab the active worksheet
# ws = wb.active
#
# # Data can be assigned directly to cells
# ws['A1'] = 42
#
# # Rows can also be appended
# ws.append([1, 2, 3])
#
# # Python types will automatically be converted
# import datetime
# ws['A2'] = datetime.datetime.now()
#
# # Save the file
# wb.save("sample.xlsx")