from rpw import DB, db, doc

col_marker = db.Collector(of_class="ElevationMarker", is_type=False)

with db.Transaction():
    for marker in col_marker:
        for i in range(4):
            view = doc.GetElement(marker.GetViewId(i))
            print(view.Name)
            # print(
            #     "delta X = {} delta Y = {} delta Z = {}".format(
            #         view.CropBox.Max.X - view.CropBox.Min.X,
            #         view.CropBox.Max.Y - view.CropBox.Min.Y,
            #         view.CropBox.Max.Z - view.CropBox.Min.Z,
            #     )
            # )
            deltaY = 13.3

            cropbox = DB.BoundingBoxXYZ()
            cropbox.Min = DB.XYZ(view.CropBox.Min.X, -80.315, view.CropBox.Min.Z)
            cropbox.Max = DB.XYZ(view.CropBox.Max.X, -67.015, view.CropBox.Max.Z)
            cropbox.Transform = view.CropBox.Transform
            view.CropBox = cropbox
# _________________________________________
# rpw console test script below

# from rpw import ui,db,UI,DB,doc,uidoc

# marker = ui.Selection()[0]

# with db.Transaction():
# 	for i in range(4):
# 		view =  doc.GetElement(marker.GetViewId(i))
#         print(
#             "delta X = {} delta Y = {} delta Z = {}".format(
#                 view.CropBox.Max.X - view.CropBox.Min.X,
#                 view.CropBox.Max.Y - view.CropBox.Min.Y,
#                 view.CropBox.Max.Z - view.CropBox.Min.Z,
#             )
#         )
# 		cropbox = DB.BoundingBoxXYZ()
# 		cropbox.Min =  DB.XYZ(view.CropBox.Min.X,-80.315, view.CropBox.Min.Z)
# 		cropbox.Max =  DB.XYZ(view.CropBox.Max.X,-67.015,view.CropBox.Max.Z)
# 		cropbox.Transform = view.CropBox.Transform
# 		view.CropBox = cropbox
