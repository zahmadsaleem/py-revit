from rpw import DB, db, doc

sheet_names = [
    "4101-Small Conference",
    "4102-Small AV",
    "4103-Conversation",
    "4108-Micro AV",
    "4104-Brainstorm",
    "4105-Large AV",
    "4106-Boardroom",
    "4107-Classroom",
]

# create seet names & numbers
all_sheet_numbers = []
all_sheet_names = []
for sheet_name in sheet_names:
    for i in range(1, 5):
        all_sheet_names.append(sheet_name + "-Type {}".format(i))
        all_sheet_numbers.append(sheet_name.split("-")[0] + "." + str(i))

# get sheet parameters
data = {
    "WW-SheetCategory": "Architecture",
    "WW-SheetSeries": "4100 Conference Room Details",
    "WW-SheetSubCategory": "04 Architecture",
    "title_block": DB.ElementId(10535381),
}

params = ["WW-SheetCategory", "WW-SheetSeries", "WW-SheetSubCategory"]

with db.Transaction("Create Sheets"):
    for sheet_name, sheet_number in zip(all_sheet_names, all_sheet_numbers):
        # check if sheet exists
        col = db.Collector(
            of_class="ViewSheet", is_type=False, where=lambda x: sheet_name in x.Name
        )
        col = col.unwrap()
        if col.GetElementCount() < 1:
            # create sheet
            sheet = DB.ViewSheet.Create(doc, data["title_block"])
            # set sheet parameters
            sheet.Name = sheet_name
            sheet.SheetNumber = "A-" + sheet_number
            for param in params:
                sheet_param = sheet.LookupParameter(param)
                sheet_param.Set(data[param])
