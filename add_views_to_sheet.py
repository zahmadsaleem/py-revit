"""
Add existing views to existing sheets.

Example: Add Views of naming series 410 to sheets

View name example:  4101 - Conference Room - Plan
                    4101 - Conference Room - RCP
                    4105 - Office Room - Elevation 1

Sheet name example: 4101 - Conference Room 
                    4105 - Office Room 
"""

from rpw import ui, db, UI, DB, doc, uidoc

# collecting views of series 410
col_plan = db.Collector(
    of_class="ViewPlan",
    is_type=False,
    where=lambda x: "410" in x.Name and "Plan" in x.Name,
).unwrap()
col_rcp = db.Collector(
    of_class="ViewPlan",
    is_type=False,
    where=lambda x: "410" in x.Name and "RCP" in x.Name,
).unwrap()
col_elev = db.Collector(
    of_class="ViewSection",
    is_type=False,
    where=lambda x: "410" in x.Name and "Elevation" in x.Name,
).unwrap()
col = col_plan.UnionWith(col_rcp.UnionWith(col_elev))

# views placed in a grid fashion
# with 2 rows and 3 columns
col1 = 0.1
col2 = 0.9
col3 = 1.8
row1 = 0.8
row2 = 2.0

# insertion point of views on sheet
items_point = {
    "Elevation 1": DB.XYZ(col2, row2, 0),
    "Elevation 2": DB.XYZ(col2, row1, 0),
    "Elevation 3": DB.XYZ(col3, row2, 0),
    "Elevation 4": DB.XYZ(col3, row1, 0),
    "RCP": DB.XYZ(col1, row1, 0),
    "Plan": DB.XYZ(col1, row2, 0),
}


with db.TransactionGroup("Add Views to Sheets"):
    for view in col.GetEnumerator():
        # get corresponding sheet
        sheet = db.Collector(
            of_class="ViewSheet",
            is_type=False,
            where=lambda x: "-".join(view.Name.split("-")[0:-1]).strip() in x.Name,
        ).get_first()
        view_item_name = view.Name.split("-")[-1].strip()
        
        # check if view is already placed on any sheet
        if not DB.Viewport.CanAddViewToSheet(doc, sheet.Id, view.Id):
            print("Sheet already placed: {}".format(view.Name))
        else:
            # add views to corresponding sheet
            with db.Transaction("Place View Port"):
                viewport = DB.Viewport.Create(
                    doc, sheet.Id, view.Id, items_point[view_item_name]
                )
            print("Added {} to sheet".format(view.Name))
