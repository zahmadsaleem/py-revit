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

# create seet names & numbers
all_sheet_numbers = []
all_sheet_names = []
for sheet_name in sheet_names:
    for i in range(1, 5):
        all_sheet_names.append(sheet_name + "-Type {}".format(i))
        all_sheet_numbers.append(sheet_name.split("-")[0] + "." + str(i))

plan_view = doc.GetElement(DB.ElementId(11335718))
rcp_view = doc.GetElement(DB.ElementId(11632340))


def duplicate_view(view, cropbox, name_suffix):
    duplicate_plan = doc.GetElement(view.Duplicate(DB.ViewDuplicateOption.AsDependent))
    duplicate_plan.Name = sheet_name + name_suffix
    duplicate_plan.CropBoxActive = True
    duplicate_plan.CropBox = cropbox
    duplicate_plan.CropBoxVisible = False
    return duplicate_plan


with db.Transaction("Duplicate View"):
    for sheet_name in all_sheet_names:
        # check if duplicate exists
        col_plan = db.Collector(
            of_class="ViewPlan",
            is_type=False,
            where=lambda x: sheet_name + "-Plan" in x.Name,
        ).unwrap()
        col_rcp = db.Collector(
            of_class="ViewPlan",
            is_type=False,
            where=lambda x: sheet_name + "-RCP" in x.Name,
        ).unwrap()
        # get cropbox region
        cropbox = DB.BoundingBoxXYZ()
        bbmin, bbmax = ui.Pick.pick_box(sheet_name)
        cropbox.Min = bbmin.unwrap()
        cropbox.Max = bbmax.unwrap()

        if col_plan.GetElementCount() < 1:
            # create duplicate
            duplicate_plan = duplicate_view(plan_view, cropbox, "-Plan")
        if col_rcp.GetElementCount() < 1:
            # create duplicate
            duplicate_rcp = duplicate_view(rcp_view, cropbox, "-RCP")
