import OCP.IMeshTools
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
import OCP.IMeshData
import OCP.GeomAbs
import OCP.Standard
import OCP.gp
import OCP.TCollection
import OCP.TColStd
import OCP.Message
import OCP.TopoDS
__all__  = [
"IMeshTools_Context",
"IMeshTools_CurveTessellator",
"IMeshTools_MeshAlgo",
"IMeshTools_MeshAlgoFactory",
"IMeshTools_MeshAlgoType",
"IMeshTools_MeshBuilder",
"IMeshTools_ModelAlgo",
"IMeshTools_ModelBuilder",
"IMeshTools_Parameters",
"IMeshTools_ShapeExplorer",
"IMeshTools_ShapeVisitor",
"IMeshTools_MeshAlgoType_DEFAULT",
"IMeshTools_MeshAlgoType_Delabella",
"IMeshTools_MeshAlgoType_Watson"
]
class IMeshTools_Context(OCP.IMeshData.IMeshData_Shape, OCP.Standard.Standard_Transient):
    """
    Interface class representing context of BRepMesh algorithm. Intended to cache discrete model and instances of tools for its processing.
    """
    def BuildModel(self) -> bool: 
        """
        Builds model using assigned model builder.
        """
    def ChangeParameters(self) -> IMeshTools_Parameters: 
        """
        Gets reference to parameters to be used for meshing.
        """
    def Clean(self) -> None: 
        """
        Cleans temporary context data.
        """
    def DecrementRefCounter(self) -> int: 
        """
        Decrements the reference counter of this object; returns the decremented value
        """
    def Delete(self) -> None: 
        """
        Memory deallocator for transient classes
        """
    def DiscretizeEdges(self) -> bool: 
        """
        Performs discretization of model edges using assigned edge discret algorithm.
        """
    def DiscretizeFaces(self,theRange : OCP.Message.Message_ProgressRange) -> bool: 
        """
        Performs meshing of faces of discrete model using assigned meshing algorithm.
        """
    def DynamicType(self) -> OCP.Standard.Standard_Type: 
        """
        None
        """
    def GetEdgeDiscret(self) -> IMeshTools_ModelAlgo: 
        """
        Gets instance of a tool to be used to discretize edges of a model.
        """
    def GetFaceDiscret(self) -> IMeshTools_ModelAlgo: 
        """
        Gets instance of meshing algorithm.
        """
    def GetModel(self) -> OCP.IMeshData.IMeshData_Model: 
        """
        Returns discrete model of a shape.
        """
    def GetModelBuilder(self) -> IMeshTools_ModelBuilder: 
        """
        Gets instance of a tool to be used to build discrete model.
        """
    def GetModelHealer(self) -> IMeshTools_ModelAlgo: 
        """
        Gets instance of a tool to be used to heal discrete model.
        """
    def GetParameters(self) -> IMeshTools_Parameters: 
        """
        Gets parameters to be used for meshing.
        """
    def GetPostProcessor(self) -> IMeshTools_ModelAlgo: 
        """
        Gets instance of post-processing algorithm.
        """
    def GetPreProcessor(self) -> IMeshTools_ModelAlgo: 
        """
        Gets instance of pre-processing algorithm.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetShape(self) -> OCP.TopoDS.TopoDS_Shape: 
        """
        Returns shape assigned to discrete shape.
        """
    def HealModel(self) -> bool: 
        """
        Performs healing of discrete model built by DiscretizeEdges() method using assigned healing algorithm.
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
    def PostProcessModel(self) -> bool: 
        """
        Performs post-processing of discrete model using assigned algorithm.
        """
    def PreProcessModel(self) -> bool: 
        """
        Performs pre-processing of discrete model using assigned algorithm. Performs auxiliary actions such as cleaning shape from old triangulation.
        """
    def SetEdgeDiscret(self,theEdgeDiscret : IMeshTools_ModelAlgo) -> None: 
        """
        Sets instance of a tool to be used to discretize edges of a model.
        """
    def SetFaceDiscret(self,theFaceDiscret : IMeshTools_ModelAlgo) -> None: 
        """
        Sets instance of meshing algorithm.
        """
    def SetModelBuilder(self,theBuilder : IMeshTools_ModelBuilder) -> None: 
        """
        Sets instance of a tool to be used to build discrete model.
        """
    def SetModelHealer(self,theModelHealer : IMeshTools_ModelAlgo) -> None: 
        """
        Sets instance of a tool to be used to heal discrete model.
        """
    def SetPostProcessor(self,thePostProcessor : IMeshTools_ModelAlgo) -> None: 
        """
        Sets instance of post-processing algorithm.
        """
    def SetPreProcessor(self,thePreProcessor : IMeshTools_ModelAlgo) -> None: 
        """
        Sets instance of pre-processing algorithm.
        """
    def SetShape(self,theShape : OCP.TopoDS.TopoDS_Shape) -> None: 
        """
        Assigns shape to discrete shape.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
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
class IMeshTools_CurveTessellator(OCP.Standard.Standard_Transient):
    """
    Interface class providing API for edge tessellation tools.
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
    def PointsNb(self) -> int: 
        """
        Returns number of tessellation points.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def Value(self,theIndex : int,thePoint : OCP.gp.gp_Pnt,theParameter : float) -> bool: 
        """
        Returns parameters of solution with the given index.
        """
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
class IMeshTools_MeshAlgo(OCP.Standard.Standard_Transient):
    """
    Interface class providing API for algorithms intended to create mesh for discrete face.
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
    def Perform(self,theDFace : OCP.IMeshData.IMeshData_Face,theParameters : IMeshTools_Parameters,theRange : OCP.Message.Message_ProgressRange) -> None: 
        """
        Performs processing of the given face.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
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
class IMeshTools_MeshAlgoFactory(OCP.Standard.Standard_Transient):
    """
    Base interface for factories producing instances of triangulation algorithms taking into account type of surface of target face.
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
    def GetAlgo(self,theSurfaceType : OCP.GeomAbs.GeomAbs_SurfaceType,theParameters : IMeshTools_Parameters) -> IMeshTools_MeshAlgo: 
        """
        Creates instance of meshing algorithm for the given type of surface.
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
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
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
class IMeshTools_MeshAlgoType():
    """
    Enumerates built-in meshing algorithms factories implementing IMeshTools_MeshAlgoFactory interface.

    Members:

      IMeshTools_MeshAlgoType_DEFAULT

      IMeshTools_MeshAlgoType_Watson

      IMeshTools_MeshAlgoType_Delabella
    """
    def __eq__(self,other : object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self,value : int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self,other : object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self,state : int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> None:
        """
        :type: None
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    IMeshTools_MeshAlgoType_DEFAULT: OCP.IMeshTools.IMeshTools_MeshAlgoType # value = <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_DEFAULT: -1>
    IMeshTools_MeshAlgoType_Delabella: OCP.IMeshTools.IMeshTools_MeshAlgoType # value = <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Delabella: 1>
    IMeshTools_MeshAlgoType_Watson: OCP.IMeshTools.IMeshTools_MeshAlgoType # value = <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Watson: 0>
    __entries: dict # value = {'IMeshTools_MeshAlgoType_DEFAULT': (<IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_DEFAULT: -1>, None), 'IMeshTools_MeshAlgoType_Watson': (<IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Watson: 0>, None), 'IMeshTools_MeshAlgoType_Delabella': (<IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Delabella: 1>, None)}
    __members__: dict # value = {'IMeshTools_MeshAlgoType_DEFAULT': <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_DEFAULT: -1>, 'IMeshTools_MeshAlgoType_Watson': <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Watson: 0>, 'IMeshTools_MeshAlgoType_Delabella': <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Delabella: 1>}
    pass
class IMeshTools_MeshBuilder(OCP.Message.Message_Algorithm, OCP.Standard.Standard_Transient):
    """
    Builds mesh for each face of shape without triangulation. In case if some faces of shape have already been triangulated checks deflection of existing polygonal model and re-uses it if deflection satisfies the specified parameter. Otherwise nullifies existing triangulation and build triangulation anew.
    """
    @overload
    def AddStatus(self,theStatus : OCP.Message.Message_ExecStatus,theOther : OCP.Message.Message_Algorithm) -> None: 
        """
        Add statuses to this algorithm from other algorithm (including messages)

        Add statuses to this algorithm from other algorithm, but only those items are moved that correspond to statuses set in theStatus
        """
    @overload
    def AddStatus(self,theOther : OCP.Message.Message_Algorithm) -> None: ...
    def ChangeStatus(self) -> OCP.Message.Message_ExecStatus: 
        """
        Returns exec status of algorithm

        Returns exec status of algorithm
        """
    def ClearStatus(self) -> None: 
        """
        Clear exec status of algorithm
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
    def GetContext(self) -> IMeshTools_Context: 
        """
        Gets context of algorithm.
        """
    def GetMessageNumbers(self,theStatus : OCP.Message.Message_Status) -> OCP.TColStd.TColStd_HPackedMapOfInteger: 
        """
        Return the numbers associated with the indicated status; Null handle if no such status or no numbers associated with it
        """
    def GetMessageStrings(self,theStatus : OCP.Message.Message_Status) -> OCP.TColStd.TColStd_HSequenceOfHExtendedString: 
        """
        Return the strings associated with the indicated status; Null handle if no such status or no strings associated with it
        """
    def GetMessenger(self) -> OCP.Message.Message_Messenger: 
        """
        Returns messenger of algorithm. The returned handle is always non-null and can be used for sending messages.

        Returns messenger of algorithm. The returned handle is always non-null and can be used for sending messages.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetStatus(self) -> OCP.Message.Message_ExecStatus: 
        """
        Returns copy of exec status of algorithm

        Returns copy of exec status of algorithm
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
    def Perform(self,theRange : OCP.Message.Message_ProgressRange) -> None: 
        """
        Performs meshing to the shape using current context.
        """
    @staticmethod
    @overload
    def PrepareReport_s(theReportSeq : OCP.TColStd.TColStd_SequenceOfHExtendedString,theMaxCount : int) -> OCP.TCollection.TCollection_ExtendedString: 
        """
        Prepares a string containing a list of integers contained in theError map, but not more than theMaxCount

        Prepares a string containing a list of names contained in theReportSeq sequence, but not more than theMaxCount
        """
    @staticmethod
    @overload
    def PrepareReport_s(theError : OCP.TColStd.TColStd_HPackedMapOfInteger,theMaxCount : int) -> OCP.TCollection.TCollection_ExtendedString: ...
    def SendMessages(self,theTraceLevel : OCP.Message.Message_Gravity=Message_Gravity.Message_Warning,theMaxCount : int=20) -> None: 
        """
        Convenient variant of SendStatusMessages() with theFilter having defined all WARN, ALARM, and FAIL (but not DONE) status flags
        """
    def SendStatusMessages(self,theFilter : OCP.Message.Message_ExecStatus,theTraceLevel : OCP.Message.Message_Gravity=Message_Gravity.Message_Warning,theMaxCount : int=20) -> None: 
        """
        Print messages for all status flags that have been set during algorithm execution, excluding statuses that are NOT set in theFilter.
        """
    def SetContext(self,theContext : IMeshTools_Context) -> None: 
        """
        Sets context for algorithm.
        """
    def SetMessenger(self,theMsgr : OCP.Message.Message_Messenger) -> None: 
        """
        Sets messenger to algorithm
        """
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_ExtendedString,noRepetitions : bool) -> None: 
        """
        Sets status with no parameter

        Sets status with integer parameter

        Sets status with string parameter. If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with preformatted message. This message will be used directly to report the status; automatic generation of status messages will be disabled for it.

        Sets status with string parameter. If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag
        """
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theInt : int) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_ExtendedString,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_AsciiString,noRepetitions : bool) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : str,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : str,noRepetitions : bool) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theMsg : OCP.Message.Message_Msg) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_HAsciiString,noRepetitions : bool) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_HExtendedString,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_AsciiString,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_HAsciiString,noRepetitions : bool=True) -> None: ...
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    @overload
    def __init__(self,theContext : IMeshTools_Context) -> None: ...
    @overload
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
class IMeshTools_ModelAlgo(OCP.Standard.Standard_Transient):
    """
    Interface class providing API for algorithms intended to update or modify discrete model.
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
    def Perform(self,theModel : OCP.IMeshData.IMeshData_Model,theParameters : IMeshTools_Parameters,theRange : OCP.Message.Message_ProgressRange) -> bool: 
        """
        Exceptions protected processing of the given model.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
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
class IMeshTools_ModelBuilder(OCP.Message.Message_Algorithm, OCP.Standard.Standard_Transient):
    """
    Interface class represents API for tool building discrete model.
    """
    @overload
    def AddStatus(self,theStatus : OCP.Message.Message_ExecStatus,theOther : OCP.Message.Message_Algorithm) -> None: 
        """
        Add statuses to this algorithm from other algorithm (including messages)

        Add statuses to this algorithm from other algorithm, but only those items are moved that correspond to statuses set in theStatus
        """
    @overload
    def AddStatus(self,theOther : OCP.Message.Message_Algorithm) -> None: ...
    def ChangeStatus(self) -> OCP.Message.Message_ExecStatus: 
        """
        Returns exec status of algorithm

        Returns exec status of algorithm
        """
    def ClearStatus(self) -> None: 
        """
        Clear exec status of algorithm
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
    def GetMessageNumbers(self,theStatus : OCP.Message.Message_Status) -> OCP.TColStd.TColStd_HPackedMapOfInteger: 
        """
        Return the numbers associated with the indicated status; Null handle if no such status or no numbers associated with it
        """
    def GetMessageStrings(self,theStatus : OCP.Message.Message_Status) -> OCP.TColStd.TColStd_HSequenceOfHExtendedString: 
        """
        Return the strings associated with the indicated status; Null handle if no such status or no strings associated with it
        """
    def GetMessenger(self) -> OCP.Message.Message_Messenger: 
        """
        Returns messenger of algorithm. The returned handle is always non-null and can be used for sending messages.

        Returns messenger of algorithm. The returned handle is always non-null and can be used for sending messages.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetStatus(self) -> OCP.Message.Message_ExecStatus: 
        """
        Returns copy of exec status of algorithm

        Returns copy of exec status of algorithm
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
    def Perform(self,theShape : OCP.TopoDS.TopoDS_Shape,theParameters : IMeshTools_Parameters) -> OCP.IMeshData.IMeshData_Model: 
        """
        Exceptions protected method to create discrete model for the given shape. Returns nullptr in case of failure.
        """
    @staticmethod
    @overload
    def PrepareReport_s(theReportSeq : OCP.TColStd.TColStd_SequenceOfHExtendedString,theMaxCount : int) -> OCP.TCollection.TCollection_ExtendedString: 
        """
        Prepares a string containing a list of integers contained in theError map, but not more than theMaxCount

        Prepares a string containing a list of names contained in theReportSeq sequence, but not more than theMaxCount
        """
    @staticmethod
    @overload
    def PrepareReport_s(theError : OCP.TColStd.TColStd_HPackedMapOfInteger,theMaxCount : int) -> OCP.TCollection.TCollection_ExtendedString: ...
    def SendMessages(self,theTraceLevel : OCP.Message.Message_Gravity=Message_Gravity.Message_Warning,theMaxCount : int=20) -> None: 
        """
        Convenient variant of SendStatusMessages() with theFilter having defined all WARN, ALARM, and FAIL (but not DONE) status flags
        """
    def SendStatusMessages(self,theFilter : OCP.Message.Message_ExecStatus,theTraceLevel : OCP.Message.Message_Gravity=Message_Gravity.Message_Warning,theMaxCount : int=20) -> None: 
        """
        Print messages for all status flags that have been set during algorithm execution, excluding statuses that are NOT set in theFilter.
        """
    def SetMessenger(self,theMsgr : OCP.Message.Message_Messenger) -> None: 
        """
        Sets messenger to algorithm
        """
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_ExtendedString,noRepetitions : bool) -> None: 
        """
        Sets status with no parameter

        Sets status with integer parameter

        Sets status with string parameter. If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with preformatted message. This message will be used directly to report the status; automatic generation of status messages will be disabled for it.

        Sets status with string parameter. If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag

        Sets status with string parameter If noRepetitions is True, the parameter will be added only if it has not been yet recorded for the same status flag
        """
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theInt : int) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_ExtendedString,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_AsciiString,noRepetitions : bool) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : str,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : str,noRepetitions : bool) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theMsg : OCP.Message.Message_Msg) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_HAsciiString,noRepetitions : bool) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_HExtendedString,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_AsciiString,noRepetitions : bool=True) -> None: ...
    @overload
    def SetStatus(self,theStat : OCP.Message.Message_Status,theStr : OCP.TCollection.TCollection_HAsciiString,noRepetitions : bool=True) -> None: ...
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
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
class IMeshTools_Parameters():
    """
    Structure storing meshing parameters
    """
    @staticmethod
    def RelMinSize_s() -> float: 
        """
        Returns factor used to compute default value of MinSize (minimum mesh edge length) from deflection
        """
    def __init__(self) -> None: ...
    @property
    def AdjustMinSize(self) -> bool:
        """
        :type: bool
        """
    @AdjustMinSize.setter
    def AdjustMinSize(self, arg0: bool) -> None:
        pass
    @property
    def AllowQualityDecrease(self) -> bool:
        """
        :type: bool
        """
    @AllowQualityDecrease.setter
    def AllowQualityDecrease(self, arg0: bool) -> None:
        pass
    @property
    def Angle(self) -> float:
        """
        :type: float
        """
    @Angle.setter
    def Angle(self, arg0: float) -> None:
        pass
    @property
    def AngleInterior(self) -> float:
        """
        :type: float
        """
    @AngleInterior.setter
    def AngleInterior(self, arg0: float) -> None:
        pass
    @property
    def CleanModel(self) -> bool:
        """
        :type: bool
        """
    @CleanModel.setter
    def CleanModel(self, arg0: bool) -> None:
        pass
    @property
    def ControlSurfaceDeflection(self) -> bool:
        """
        :type: bool
        """
    @ControlSurfaceDeflection.setter
    def ControlSurfaceDeflection(self, arg0: bool) -> None:
        pass
    @property
    def Deflection(self) -> float:
        """
        :type: float
        """
    @Deflection.setter
    def Deflection(self, arg0: float) -> None:
        pass
    @property
    def DeflectionInterior(self) -> float:
        """
        :type: float
        """
    @DeflectionInterior.setter
    def DeflectionInterior(self, arg0: float) -> None:
        pass
    @property
    def EnableControlSurfaceDeflectionAllSurfaces(self) -> bool:
        """
        :type: bool
        """
    @EnableControlSurfaceDeflectionAllSurfaces.setter
    def EnableControlSurfaceDeflectionAllSurfaces(self, arg0: bool) -> None:
        pass
    @property
    def ForceFaceDeflection(self) -> bool:
        """
        :type: bool
        """
    @ForceFaceDeflection.setter
    def ForceFaceDeflection(self, arg0: bool) -> None:
        pass
    @property
    def InParallel(self) -> bool:
        """
        :type: bool
        """
    @InParallel.setter
    def InParallel(self, arg0: bool) -> None:
        pass
    @property
    def InternalVerticesMode(self) -> bool:
        """
        :type: bool
        """
    @InternalVerticesMode.setter
    def InternalVerticesMode(self, arg0: bool) -> None:
        pass
    @property
    def MeshAlgo(self) -> IMeshTools_MeshAlgoType:
        """
        :type: IMeshTools_MeshAlgoType
        """
    @MeshAlgo.setter
    def MeshAlgo(self, arg0: IMeshTools_MeshAlgoType) -> None:
        pass
    @property
    def MinSize(self) -> float:
        """
        :type: float
        """
    @MinSize.setter
    def MinSize(self, arg0: float) -> None:
        pass
    @property
    def Relative(self) -> bool:
        """
        :type: bool
        """
    @Relative.setter
    def Relative(self, arg0: bool) -> None:
        pass
    pass
class IMeshTools_ShapeExplorer(OCP.IMeshData.IMeshData_Shape, OCP.Standard.Standard_Transient):
    """
    Explores TopoDS_Shape for parts to be meshed - faces and free edges.
    """
    def Accept(self,theVisitor : IMeshTools_ShapeVisitor) -> None: 
        """
        Starts exploring of a shape.
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
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetShape(self) -> OCP.TopoDS.TopoDS_Shape: 
        """
        Returns shape assigned to discrete shape.
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
    def SetShape(self,theShape : OCP.TopoDS.TopoDS_Shape) -> None: 
        """
        Assigns shape to discrete shape.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def __init__(self,theShape : OCP.TopoDS.TopoDS_Shape) -> None: ...
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
class IMeshTools_ShapeVisitor(OCP.Standard.Standard_Transient):
    """
    Interface class for shape visitor.
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
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    @overload
    def Visit(self,theEdge : OCP.TopoDS.TopoDS_Edge) -> None: 
        """
        Handles TopoDS_Face object.

        Handles TopoDS_Edge object.
        """
    @overload
    def Visit(self,theFace : OCP.TopoDS.TopoDS_Face) -> None: ...
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
IMeshTools_MeshAlgoType_DEFAULT: OCP.IMeshTools.IMeshTools_MeshAlgoType # value = <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_DEFAULT: -1>
IMeshTools_MeshAlgoType_Delabella: OCP.IMeshTools.IMeshTools_MeshAlgoType # value = <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Delabella: 1>
IMeshTools_MeshAlgoType_Watson: OCP.IMeshTools.IMeshTools_MeshAlgoType # value = <IMeshTools_MeshAlgoType.IMeshTools_MeshAlgoType_Watson: 0>
