from airtable import Airtable
from rpw import DB, db, doc
from System.Net import WebClient

__fullframeengine__ = True

# getting default material and assets

provider = DB.ParameterValueProvider(DB.ElementId(DB.BuiltInParameter.MATERIAL_NAME))
rule = DB.FilterStringRule(provider, DB.FilterStringEquals(), "WWI-Generic", False)
base_filter = DB.ElementParameterFilter(rule)

basefabric = (
    DB.FilteredElementCollector(doc)
    .OfCategory(DB.BuiltInCategory.OST_Materials)
    .WherePasses(base_filter)
    .ToElements()[0]
)
basefabricA_asset = doc.GetElement(basefabric.AppearanceAssetId)
print("basefabric : " + basefabric.Name + ", asset id : " + basefabricA_asset.Name)
# basefabricR_asset = basefabricA_asset.GetRenderingAsset()

# initiate the Airtable Base - Setting the Airtable base
base_key = "somebasid"
table_name = "Fabrics_List"
api_key = "someapikey"
airtable = Airtable(base_key, table_name, api_key)
fabric_df = airtable.get_all()


folder_path = r"C:\_Local\Bulk_Images"

material_list = []
map_path = []
category_list = []

# Populating Material List and Downloading the images:
for item in fabric_df:
    image_approval = item["fields"]["Approval"]
    material_name = item["fields"]["Fabric_Code_Ref"]
    material_category = item["fields"]["Material_Type"]
    if image_approval != "Rejected":
        material_list.append(material_name)
        category_list.append(material_category)
        print("Downloading: " + material_name)
        try:
            image_url = item["fields"]["Fabric_Image"][0]["url"]
            image_ext = image_url.split("/")[-1].split(".")[-1]
            map_path.append(folder_path + "\\" + material_name + "." + image_ext)
            wc = WebClient()
            wc.DownloadFile(
                image_url, folder_path + "\\" + material_name + "." + image_ext
            )
        except KeyError:
            print("-" * 10 + material_name + " has no image")
            map_path.append(None)
    else:
        print("-" * 5 + image_approval + "-" * 5 + material_name)

# Fetching Materials
with db.Transaction("Creating Bulk Materials"):
    for i, item in enumerate(material_list):
        mat = basefabric.Duplicate(item)
        mat.AppearanceAssetId = basefabricA_asset.Duplicate(item).Id
        fabric_texture_path = map_path[i]
        mat.MaterialCategory = category_list[i][0]
        editMatScope = DB.Visual.AppearanceAssetEditScope(doc)
        editableMatAsset = editMatScope.Start(mat.AppearanceAssetId)
        # for assetprop in editableMatAsset:
        # 	allprops = assetprop.GetAllConnectedProperties()
        # 	print assetprop.Name
        # 	if len(allprops)>0:
        # 		print "connectedAsset "+ allprops.Name
        assetMatProperty = editableMatAsset["generic_diffuse"]
        connectedMatAsset = assetMatProperty.GetSingleConnectedAsset()
        texturepath = connectedMatAsset.FindByName(
            DB.Visual.UnifiedBitmap.UnifiedbitmapBitmap
        )
        if fabric_texture_path is not None:
            texturepath.Value = fabric_texture_path
        else:
            assetMatProperty.RemoveConnectedAsset()
        print("Material added: " + item)
        editMatScope.Commit(True)
