import OCP.APIHeaderSection
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
import OCP.Standard
import OCP.TCollection
import OCP.TColStd
import OCP.StepData
import OCP.IFSelect
import io
import OCP.Interface
__all__  = [
"APIHeaderSection_EditHeader",
"APIHeaderSection_MakeHeader"
]
class APIHeaderSection_EditHeader(OCP.IFSelect.IFSelect_Editor, OCP.Standard.Standard_Transient):
    def Apply(self,form : OCP.IFSelect.IFSelect_EditForm,ent : OCP.Standard.Standard_Transient,model : OCP.Interface.Interface_InterfaceModel) -> bool: 
        """
        None
        """
    def DecrementRefCounter(self) -> int: 
        """
        Decrements the reference counter of this object; returns the decremented value
        """
    def Delete(self) -> None: 
        """
        Memory deallocator for transient classes
        """
    def DynamicType(self) -> OCP.Standard.Standard_Type: 
        """
        None
        """
    def EditMode(self,num : int) -> OCP.IFSelect.IFSelect_EditValue: 
        """
        Returns the edit mode of a Value
        """
    def Form(self,readonly : bool,undoable : bool=True) -> OCP.IFSelect.IFSelect_EditForm: 
        """
        Builds and Returns an EditForm, empty (no data yet) Can be redefined to return a specific type of EditForm
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    @overload
    def IsInstance(self,theTypeName : str) -> bool: 
        """
        Returns a true value if this is an instance of Type.

        Returns a true value if this is an instance of TypeName.
        """
    @overload
    def IsInstance(self,theType : OCP.Standard.Standard_Type) -> bool: ...
    @overload
    def IsKind(self,theType : OCP.Standard.Standard_Type) -> bool: 
        """
        Returns true if this is an instance of Type or an instance of any class that inherits from Type. Note that multiple inheritance is not supported by OCCT RTTI mechanism.

        Returns true if this is an instance of TypeName or an instance of any class that inherits from TypeName. Note that multiple inheritance is not supported by OCCT RTTI mechanism.
        """
    @overload
    def IsKind(self,theTypeName : str) -> bool: ...
    def IsList(self,num : int) -> bool: 
        """
        Tells if a parameter is a list
        """
    def Label(self) -> OCP.TCollection.TCollection_AsciiString: 
        """
        None
        """
    def ListEditor(self,num : int) -> OCP.IFSelect.IFSelect_ListEditor: 
        """
        Returns a ListEditor for a parameter which is a List Default returns a basic ListEditor for a List, a Null Handle if <num> is not for a List. Can be redefined
        """
    def ListValue(self,form : OCP.IFSelect.IFSelect_EditForm,num : int) -> OCP.TColStd.TColStd_HSequenceOfHAsciiString: 
        """
        Returns the value of an EditForm as a List, for a given item If not a list, a Null Handle should be returned Default returns a Null Handle, because many Editors have no list to edit. To be redefined as required
        """
    def Load(self,form : OCP.IFSelect.IFSelect_EditForm,ent : OCP.Standard.Standard_Transient,model : OCP.Interface.Interface_InterfaceModel) -> bool: 
        """
        None
        """
    def MaxList(self,num : int) -> int: 
        """
        Returns max length allowed for a list = 0 means : list with no limit < 0 means : not a list
        """
    def MaxNameLength(self,what : int) -> int: 
        """
        Returns the MaxLength of, according to what : <what> = -1 : length of short names <what> = 0 : length of complete names <what> = 1 : length of values labels
        """
    def Name(self,num : int,isshort : bool=False) -> str: 
        """
        Returns the name of a Value (complete or short) from its ident Short Name can be empty
        """
    def NameNumber(self,name : str) -> int: 
        """
        Returns the number (ident) of a Value, from its name, short or complete. If not found, returns 0
        """
    def NbValues(self) -> int: 
        """
        Returns the count of Typed Values
        """
    def PrintDefs(self,S : io.BytesIO,labels : bool=False) -> None: 
        """
        None
        """
    def PrintNames(self,S : io.BytesIO) -> None: 
        """
        None
        """
    def Recognize(self,form : OCP.IFSelect.IFSelect_EditForm) -> bool: 
        """
        None
        """
    def SetList(self,num : int,max : int=0) -> None: 
        """
        Sets a parameter to be a List max < 0 : not for a list (set when starting) max = 0 : list with no length limit (default for SetList) max > 0 : list limited to <max> items
        """
    def SetValue(self,num : int,typval : OCP.Interface.Interface_TypedValue,shortname : str='',accessmode : OCP.IFSelect.IFSelect_EditValue=IFSelect_EditValue.IFSelect_Editable) -> None: 
        """
        Sets a Typed Value for a given ident and short name, with an Edit Mode
        """
    def StringValue(self,form : OCP.IFSelect.IFSelect_EditForm,num : int) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        None
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def TypedValue(self,num : int) -> OCP.Interface.Interface_TypedValue: 
        """
        Returns a Typed Value from its ident
        """
    def Update(self,form : OCP.IFSelect.IFSelect_EditForm,num : int,newval : OCP.TCollection.TCollection_HAsciiString,enforce : bool) -> bool: 
        """
        Updates the EditForm when a parameter is modified I.E. default does nothing, can be redefined, as follows : Returns True when done (even if does nothing), False in case of refuse (for instance, if the new value is not suitable) <num> is the rank of the parameter for the EDITOR itself <enforce> True means that protected parameters can be touched
        """
    def UpdateList(self,form : OCP.IFSelect.IFSelect_EditForm,num : int,newlist : OCP.TColStd.TColStd_HSequenceOfHAsciiString,enforce : bool) -> bool: 
        """
        Acts as Update, but when the value is a list
        """
    def __init__(self) -> None: ...
    @staticmethod
    def get_type_descriptor_s() -> OCP.Standard.Standard_Type: 
        """
        None
        """
    @staticmethod
    def get_type_name_s() -> str: 
        """
        None
        """
    pass
class APIHeaderSection_MakeHeader():
    """
    This class allows to consult and prepare/edit data stored in a Step Model Header
    """
    def AddSchemaIdentifier(self,aSchemaIdentifier : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        Add a subname of schema (if not yet in the list)
        """
    def Apply(self,model : OCP.StepData.StepData_StepModel) -> None: 
        """
        Creates an empty header for a new STEP model and allows the header fields to be completed.
        """
    def Author(self) -> OCP.Interface.Interface_HArray1OfHAsciiString: 
        """
        None
        """
    def AuthorValue(self,num : int) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the value of the name attribute for the file_name entity.
        """
    def Authorisation(self) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the value of the authorization attribute for the file_name entity.
        """
    def Description(self) -> OCP.Interface.Interface_HArray1OfHAsciiString: 
        """
        None
        """
    def DescriptionValue(self,num : int) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the value of the description attribute for the file_description entity.
        """
    def FdValue(self) -> HeaderSection_FileDescription: 
        """
        Returns the file_description entity. Returns an empty entity if the file_description entity is not initialized.
        """
    def FnValue(self) -> HeaderSection_FileName: 
        """
        Returns the file_name entity. Returns an empty entity if the file_name entity is not initialized.
        """
    def FsValue(self) -> HeaderSection_FileSchema: 
        """
        Returns the file_schema entity. Returns an empty entity if the file_schema entity is not initialized.
        """
    def HasFd(self) -> bool: 
        """
        Checks whether there is a file_description entity. Returns True if there is one.
        """
    def HasFn(self) -> bool: 
        """
        Checks whether there is a file_name entity. Returns True if there is one.
        """
    def HasFs(self) -> bool: 
        """
        Checks whether there is a file_schema entity. Returns True if there is one.
        """
    def ImplementationLevel(self) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the value of the implementation_level attribute for the file_description entity.
        """
    def Init(self,nameval : str) -> None: 
        """
        Cancels the former definition and gives a FileName To be used when a Model has no well defined Header
        """
    def IsDone(self) -> bool: 
        """
        Returns True if all data have been defined (see also HasFn, HasFs, HasFd)
        """
    def Name(self) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the name attribute for the file_name entity.
        """
    def NbAuthor(self) -> int: 
        """
        Returns the number of values for the author attribute in the file_name entity.
        """
    def NbDescription(self) -> int: 
        """
        Returns the number of values for the file_description entity in the STEP file header.
        """
    def NbOrganization(self) -> int: 
        """
        Returns the number of values for the organization attribute in the file_name entity.
        """
    def NbSchemaIdentifiers(self) -> int: 
        """
        Returns the number of values for the schema_identifier attribute in the file_schema entity.
        """
    def NewModel(self,protocol : OCP.Interface.Interface_Protocol) -> OCP.StepData.StepData_StepModel: 
        """
        Builds a Header, creates a new StepModel, then applies the Header to the StepModel The Schema Name is taken from the Protocol (if it inherits from StepData, else it is left in blanks)
        """
    def Organization(self) -> OCP.Interface.Interface_HArray1OfHAsciiString: 
        """
        None
        """
    def OrganizationValue(self,num : int) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the value of attribute organization for the file_name entity.
        """
    def OriginatingSystem(self) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        None
        """
    def PreprocessorVersion(self) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the name of the preprocessor_version for the file_name entity.
        """
    def SchemaIdentifiers(self) -> OCP.Interface.Interface_HArray1OfHAsciiString: 
        """
        None
        """
    def SchemaIdentifiersValue(self,num : int) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the value of the schema_identifier attribute for the file_schema entity.
        """
    def SetAuthor(self,aAuthor : OCP.Interface.Interface_HArray1OfHAsciiString) -> None: 
        """
        None
        """
    def SetAuthorValue(self,num : int,aAuthor : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetAuthorisation(self,aAuthorisation : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetDescription(self,aDescription : OCP.Interface.Interface_HArray1OfHAsciiString) -> None: 
        """
        None
        """
    def SetDescriptionValue(self,num : int,aDescription : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetImplementationLevel(self,aImplementationLevel : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetName(self,aName : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetOrganization(self,aOrganization : OCP.Interface.Interface_HArray1OfHAsciiString) -> None: 
        """
        None
        """
    def SetOrganizationValue(self,num : int,aOrganization : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetOriginatingSystem(self,aOriginatingSystem : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetPreprocessorVersion(self,aPreprocessorVersion : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetSchemaIdentifiers(self,aSchemaIdentifiers : OCP.Interface.Interface_HArray1OfHAsciiString) -> None: 
        """
        None
        """
    def SetSchemaIdentifiersValue(self,num : int,aSchemaIdentifier : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def SetTimeStamp(self,aTimeStamp : OCP.TCollection.TCollection_HAsciiString) -> None: 
        """
        None
        """
    def TimeStamp(self) -> OCP.TCollection.TCollection_HAsciiString: 
        """
        Returns the value of the time_stamp attribute for the file_name entity.
        """
    @overload
    def __init__(self,shapetype : int=0) -> None: ...
    @overload
    def __init__(self,model : OCP.StepData.StepData_StepModel) -> None: ...
    pass
