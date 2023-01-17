import random
import numpy
from openpyxl import Workbook, load_workbook



# workbook = load_workbook(filename="Saved translations.xlsx")
#
# sheets = workbook.sheetnames
# sheet = workbook.active
# print(f"{sheets = }")
# print(f"{sheet = }")
#
# res = sheet["C1:C50"]
# words = [x[0].value for x in res]
# print(f"{words = }")
#
# res = sheet["D1:D50"]
# translations = [x[0].value for x in res]
# print(f"{translations = }")
#
# list1 = []
#
# # for i in range(len(words)):
# #     list1.append(Words(word=words[i], translation=translations[i]))
#
# for i in range(10):
#     list1.append(Words(word=words[i], translation=translations[i]))
#
#
#
# Words.objects.bulk_create(list1)

lst1 = [1,2,3,4,5,6,7,8,9,10]
lst2 = [1,3,1,1,1,1,1,1,1,1]
lst2 = [x / sum(lst2) for x in lst2]
print([round(x, 3) for x in lst2])
count = [0,0,0,0,0,0,0,0,0,0]
for i in range(10):
    lst3 = random.choices(lst1, weights=lst2, k=4)
    lst3 = numpy.random.choice(lst1, p=lst2, size=4,replace=False)
    for j in lst3:
        count[j-1] += 1
    print(f"{list(lst3) = }")

print(lst3[0])
print(count)






# res = sheet["C1:C50"]
# # res = sheet["B"]
# # print(f"{res = }")
# res = [x[0].value for x in res]
# print(f"{res = }")
#
# res = sheet["C"]
# # print(f"{res = }")
# res = [x.value for x in res]
# print(f"{res = }")
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