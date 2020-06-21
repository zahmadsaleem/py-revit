"""

"""
from rpw import db, DB, doc

# import json
# from os import path

"""
JSON schema:

{
    "name": string:name,
    "category":str:categoryId,
    "fields": list of [ScheduleFieldType,ElementId],
    "filters":list of [ScheduleFieldId,ScheduleFilterType,filter_value],
    "sorts": list of ScheduleFieldId,
    "itemized": bool:IsItemized
}
"""


def field_from_name(field_name, sched_def):
    for fieldId in sched_def.GetFieldOrder():
        if sched_def.GetField(fieldId).GetName() == field_name:
            return fieldId


def sched_to_dict(sched):
    """
    Convert schedule object to dictionary representation

    Args:
        sched (ViewSchedule): revit ViewSchedule to be converted

    Returns:
        [dict]: dictionary representation of a schedule object
    """
    sched = doc.ActiveView
    sched_def = sched.Definition
    fields = sched_def.GetFieldOrder()
    filters = sched_def.GetFilters()
    sorts = sched_def.GetSortGroupFields()

    sched_dict = {
        "name": sched.Name,
        "category": sched_def.CategoryId.IntegerValue,
        "itemized": sched_def.IsItemized,
        "fields": [],
        "filters": [],
        "sorts": [],
    }

    for fieldId in fields:
        _field = sched_def.GetField(fieldId)

        if _field.IsCombinedParameterField:
            field_paramId = []
            for param in _field.GetCombinedParameters():
                field_paramId.append(
                    [
                        param.ParamId.IntegerValue,
                        param.Prefix,
                        param.Suffix,
                        param.Separator,
                    ]
                )
        else:
            field = _field.GetSchedulableField()
            field_paramId = field.ParameterId.IntegerValue

        sched_field = {
            "combined": _field.IsCombinedParameterField,
            "hidden": sched_def.GetField(fieldId).IsHidden,
            "ScheduleFieldDisplayType": str(_field.DisplayType).split(".")[-1],
            "paramId": field_paramId,
            "fieldType": str(field.FieldType).split(".")[-1],
            "fieldIndex": _field.FieldIndex,
        }
        sched_dict["fields"].append(sched_field)

    for _filter in filters:
        _attrs = [i for i in dir(DB.ScheduleFilter) if "Is" in i and "Value" in i]
        for _attr in _attrs:
            p = getattr(DB.ScheduleFilter, _attr)
            if p.__get__(_filter):
                filter_method = getattr(DB.ScheduleFilter, "Get" + _attr[2:])
                filter_value = filter_method(_filter)
                if "Element" in _attr:
                    filter_value = [
                        doc.GetElement(filter_value).Name,
                        doc.GetElement(filter_value).Category.Name,
                    ]
                    break
                else:
                    filter_value = [filter_value]
        sched_filter = {
            "filter_field": sched_def.GetField(_filter.FieldId).GetName(),
            "filterType": str(_filter.FilterType).split(".")[-1],
            "filter_value": filter_value,
        }
        sched_dict["filters"].append(sched_filter)

    for sched_sort in sorts:
        sched_dict["sorts"].append(sched_def.GetField(sched_sort.FieldId).GetName())

    return sched_dict


def dict_to_sched(sched_dict):
    """
    Convert dictionary representation
    of a schedule to revit ViewSchedule object.
    NOTE : Need to be run within a transaction

    Args:
        sched_dict (dict): dictionary representation of a schedule object

    Returns:
        [ViewSchedule]: Revit ViewSchedule created using dictionary representation
    """
    sched = DB.ViewSchedule.CreateSchedule(doc, DB.ElementId(sched_dict["category"]))
    sched.Name = sched_dict["name"]
    sched_def = sched.Definition
    sched_def.IsItemized = sched_dict["itemized"]
    for field in sched_dict["fields"]:
        if field["combined"]:
            combined_fields = []
            for i in field["paramId"]:
                combined_field = DB.TableCellCombinedParameterData.Create()
                combined_field.ParamId = DB.ElementId(i[0])
                combined_field.Prefix, combined_field.Suffix, combined_field.Separator = i[
                    1:
                ]
                combined_fields.append(combined_field)
            sched_field = sched_def.InsertCombinedParameterField(
                combined_fields, "Combined", field["fieldIndex"]
            )
        else:
            sched_field = sched_def.AddField(
                getattr(DB.ScheduleFieldType, field["fieldType"]),
                DB.ElementId(field["paramId"]),
            )
        sched_field.IsHidden = field["hidden"]
        if not field["ScheduleFieldDisplayType"] == "Standard":
            sched_field.DisplayType = getattr(
                DB.ScheduleFieldDisplayType, field["ScheduleFieldDisplayType"]
            )

    for _filter in sched_dict["filters"]:
        if len(_filter["filter_value"]) > 1:
            col = db.Collector(
                of_category=_filter["filter_value"][1],
                is_not_type=True,
                where=lambda x: _filter["filter_value"][0] in x.Name,
            ).get_element_ids()
            el = col[0]
            sched_filter = DB.ScheduleFilter(
                field_from_name(_filter["filter_field"], sched_def),
                getattr(DB.ScheduleFilterType, _filter["filterType"]),
                el,
            )
        else:
            sched_filter = DB.ScheduleFilter(
                field_from_name(_filter["filter_field"], sched_def),
                getattr(DB.ScheduleFilterType, _filter["filterType"]),
                _filter["filter_value"][0],
            )
        sched_def.AddFilter(sched_filter)
    for field_name in sched_dict["sorts"]:
        sort_field = field_from_name(field_name, sched_def)
        sched_sort = DB.ScheduleSortGroupField(sort_field)
        sched_sort.ShowBlankLine = False
        sched_sort.ShowFooter = False
        sched_sort.ShowHeader = False
        sched_def.AddSortGroupField(sched_sort)
    return sched
