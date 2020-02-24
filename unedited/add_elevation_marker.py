from rpw import DB, db, doc, ui

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
all_sheet_numbers = []
all_sheet_names = []
for sheet_name in sheet_names:
    for i in range(1, 5):
        all_sheet_names.append(sheet_name + "-Type {}".format(i))
        all_sheet_numbers.append(sheet_name.split("-")[0] + "." + str(i))

viewTypeId = DB.ElementId(10522069)
view_data = {"WW-ViewCategory": "Working", "WW-ViewSubCategory": "0000 Architecture"}

params = ["WW-ViewCategory", "WW-ViewSeries", "WW-ViewSubCategory"]

with db.Transaction("Add Elevation Marker"):
    for sheet_name in all_sheet_names:
        print("pick point for {}".format(sheet_name))
        pt = ui.Pick.pick_pt().unwrap()
        col = db.Collector(
            of_class="ViewSection", is_type=False, where=lambda x: sheet_name in x.Name
        )
        col = col.unwrap()
        if col.GetElementCount() < 1:
            marker = DB.ElevationMarker.CreateElevationMarker(doc, viewTypeId, pt, 20)
            viewPlanId = doc.ActiveView.Id
            for i in range(4):
                elevation = marker.CreateElevation(doc, viewPlanId, i)
                elevation.Name = sheet_name + " - Elevation {}".format(i + 1)
