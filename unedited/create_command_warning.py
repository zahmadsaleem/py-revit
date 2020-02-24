from rpw import UI
from rpw.ui.forms import Alert


from System import EventHandler
from Autodesk.Revit.UI.Events import BeforeExecutedEventArgs
from Autodesk.Revit.DB.Events import ElementTypeDuplicatingEventArgs


def inplace_handler(sender, args):
    Alert("You Serious??! Make some legit families instead")


def typeduplicating_handler(sender, args):
    Alert("Duplicating Types is not a good practice")


def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
    commandId = UI.RevitCommandId.LookupCommandId("ID_INPLACE_COMPONENT")
    binding = __revit__.CreateAddInCommandBinding(commandId)

    try:
        binding.BeforeExecuted += EventHandler[BeforeExecutedEventArgs](inplace_handler)
        __revit__.Application.ElementTypeDuplicating += EventHandler[
            ElementTypeDuplicatingEventArgs
        ](typeduplicating_handler)
        return True
    except Exception:
        return False
