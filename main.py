from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append(["Colonna 1", "Colonna 2"])
ws.append(["Valore A", "Valore B"])

wb.save("test_file.xlsx")
print("✅ File salvato!")
