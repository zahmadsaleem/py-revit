import json
from os import path

from rpw import DB, db, doc

jsonfile = r"C:\_Local\Bulk_Images_Test\newImgPath.json"
with open(jsonfile, "r") as f:
    newPathDict = json.load(f)


allmaterials = db.Collector(of_category="OST_Materials")
allmaterials = [i for i in allmaterials if i.Name[:3] == "WWI"]

# newPath = r"B:\Content\WWAS\Families\India\Furniture\Bulk"
newPath = r"B:\Content\WWAS\Materials\India"


def getAssetPath(mat):
    editMatScope = DB.Visual.AppearanceAssetEditScope(doc)
    editableMatAsset = editMatScope.Start(mat.AppearanceAssetId)
    assetMatProperty = editableMatAsset["generic_diffuse"]
    connectedMatAsset = assetMatProperty.GetSingleConnectedAsset()
    if connectedMatAsset:
        texturepath = connectedMatAsset.FindByName(
            DB.Visual.UnifiedBitmap.UnifiedbitmapBitmap
        )
        return editMatScope, texturepath


for mat in allmaterials:
    editMatScope, texturepath = getAssetPath(mat)
    if texturepath:
        with db.Transaction():
            texturepath.Value = path.join(
                newPath, newPathDict[path.basename(texturepath.Value)]
            )
            editMatScope.Commit(False)
        print(texturepath.Value)
