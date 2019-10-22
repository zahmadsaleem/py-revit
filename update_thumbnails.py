"""
Set thumbnail to a 3D View.
"""

from rpw import revit, db, ui, DB, UI, doc, uidoc
import os
from os import path

__context__ = "zerodoc"

folder = ui.forms.select_folder()
docList = [
    path.join(folder, file)
    for file in os.listdir(folder)
    if file[-3:] in ["rfa", "rvt", "rft"]
]


def getView3D(doc, viewName):
    col = DB.FilteredElementCollector(doc).OfClass(DB.View3D).ToElements()
    thumb = None
    for View3D in col:
        if View3D.Name == viewName:
            thumb = View3D
            break
    return thumb


def refreshThumb(doc, View3D, set_preview=False):
    # set to rendered view
    View3D.Parameter[DB.BuiltInParameter.MODEL_GRAPHICS_STYLE].Set(5)
    if set_preview:
        doc.GetDocumentPreviewSettings().PreviewViewId = View3D.Id
    doc.GetDocumentPreviewSettings().ForceViewUpdate(True)


def createThumbView(doc, viewName):
    col = DB.FilteredElementCollector(doc).OfClass(DB.View3D).ToElements()
    thumb = DB.View3D.CreateIsometric(doc, col[0].GetTypeId())
    thumb.Name = viewName
    return thumb


viewName = "Preview Image"

for docPath in docList:
    thisdoc = uidoc.Application.Application.OpenDocumentFile(docPath)
    PreviewViewId = thisdoc.GetDocumentPreviewSettings().PreviewViewId
    with db.Transaction("Update Thumbnail"):
        if thisdoc.GetElement(PreviewViewId).Name != viewName:
            View3D = getView3D(thisdoc, viewName)
            if View3D:
                refreshThumb(thisdoc, View3D, set_preview=True)
            else:
                refreshThumb(thisdoc, createThumbView(thisdoc, viewName))
        else:
            refreshThumb(thisdoc, doc.GetElement(PreviewViewId))

    thisdoc.Close(True)
