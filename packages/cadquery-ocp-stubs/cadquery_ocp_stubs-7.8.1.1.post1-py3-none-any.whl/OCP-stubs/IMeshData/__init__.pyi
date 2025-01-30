import OCP.IMeshData
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
import OCP.Standard
import OCP.gp
import OCP.BRepAdaptor
import OCP.TopAbs
import OCP.TopoDS
__all__  = [
"IMeshData_ParametersList",
"IMeshData_Shape",
"IMeshData_StatusOwner",
"IMeshData_Model",
"IMeshData_PCurve",
"IMeshData_Curve",
"IMeshData_TessellatedShape",
"IMeshData_Status",
"IMeshData_Face",
"IMeshData_Edge",
"IMeshData_Wire",
"IMeshData_Failure",
"IMeshData_NoError",
"IMeshData_OpenWire",
"IMeshData_Outdated",
"IMeshData_ReMesh",
"IMeshData_Reused",
"IMeshData_SelfIntersectingWire",
"IMeshData_TooFewPoints",
"IMeshData_UnorientedWire",
"IMeshData_UserBreak"
]
class IMeshData_ParametersList(OCP.Standard.Standard_Transient):
    """
    Interface class representing list of parameters on curve.
    """
    def Clear(self,isKeepEndPoints : bool) -> None: 
        """
        Clears parameters list.
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
    def GetParameter(self,theIndex : int) -> float: 
        """
        Returns parameter with the given index.
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
    def ParametersNb(self) -> int: 
        """
        Returns number of parameters.
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
class IMeshData_Shape(OCP.Standard.Standard_Transient):
    """
    Interface class representing model with associated TopoDS_Shape. Intended for inheritance by structures and algorithms keeping reference TopoDS_Shape.
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
class IMeshData_StatusOwner():
    """
    Extension interface class providing status functionality.
    """
    def GetStatusMask(self) -> int: 
        """
        Returns complete status mask.
        """
    def IsEqual(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is strictly equal to the given value.
        """
    def IsSet(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is set.
        """
    def SetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
        """
    def UnsetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
        """
    pass
class IMeshData_Model(IMeshData_Shape, OCP.Standard.Standard_Transient):
    """
    Interface class representing discrete model of a shape.
    """
    def AddEdge(self,theEdge : OCP.TopoDS.TopoDS_Edge) -> IMeshData_Edge: 
        """
        Adds new edge to shape model.
        """
    def AddFace(self,theFace : OCP.TopoDS.TopoDS_Face) -> IMeshData_Face: 
        """
        Adds new face to shape model.
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
    def EdgesNb(self) -> int: 
        """
        Returns number of edges in discrete model.
        """
    def FacesNb(self) -> int: 
        """
        Returns number of faces in discrete model.
        """
    def GetEdge(self,theIndex : int) -> IMeshData_Edge: 
        """
        Gets model's edge with the given index.
        """
    def GetFace(self,theIndex : int) -> IMeshData_Face: 
        """
        Gets model's face with the given index.
        """
    def GetMaxSize(self) -> float: 
        """
        Returns maximum size of shape model.
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
class IMeshData_PCurve(IMeshData_ParametersList, OCP.Standard.Standard_Transient):
    """
    Interface class representing pcurve of edge associated with discrete face. Indexation of points starts from zero.
    """
    def AddPoint(self,thePoint : OCP.gp.gp_Pnt2d,theParamOnPCurve : float) -> None: 
        """
        Adds new discretization point to pcurve.
        """
    def Clear(self,isKeepEndPoints : bool) -> None: 
        """
        Clears parameters list.
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
    def GetFace(self) -> IMeshData_Face: 
        """
        Returns discrete face pcurve is associated to.
        """
    def GetIndex(self,theIndex : int) -> int: 
        """
        Returns index in mesh corresponded to discretization point with the given index.
        """
    def GetOrientation(self) -> OCP.TopAbs.TopAbs_Orientation: 
        """
        Returns orientation of the edge associated with current pcurve.
        """
    def GetParameter(self,theIndex : int) -> float: 
        """
        Returns parameter with the given index.
        """
    def GetPoint(self,theIndex : int) -> OCP.gp.gp_Pnt2d: 
        """
        Returns discretization point with the given index.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def InsertPoint(self,thePosition : int,thePoint : OCP.gp.gp_Pnt2d,theParamOnPCurve : float) -> None: 
        """
        Inserts new discretization point at the given position.
        """
    def IsForward(self) -> bool: 
        """
        Returns forward flag of this pcurve.
        """
    @overload
    def IsInstance(self,theTypeName : str) -> bool: 
        """
        Returns a true value if this is an instance of Type.

        Returns a true value if this is an instance of TypeName.
        """
    @overload
    def IsInstance(self,theType : OCP.Standard.Standard_Type) -> bool: ...
    def IsInternal(self) -> bool: 
        """
        Returns internal flag of this pcurve.
        """
    @overload
    def IsKind(self,theType : OCP.Standard.Standard_Type) -> bool: 
        """
        Returns true if this is an instance of Type or an instance of any class that inherits from Type. Note that multiple inheritance is not supported by OCCT RTTI mechanism.

        Returns true if this is an instance of TypeName or an instance of any class that inherits from TypeName. Note that multiple inheritance is not supported by OCCT RTTI mechanism.
        """
    @overload
    def IsKind(self,theTypeName : str) -> bool: ...
    def ParametersNb(self) -> int: 
        """
        Returns number of parameters.
        """
    def RemovePoint(self,theIndex : int) -> None: 
        """
        Removes point with the given index.
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
class IMeshData_Curve(IMeshData_ParametersList, OCP.Standard.Standard_Transient):
    """
    Interface class representing discrete 3d curve of edge. Indexation of points starts from zero.
    """
    def AddPoint(self,thePoint : OCP.gp.gp_Pnt,theParamOnCurve : float) -> None: 
        """
        Adds new discretization point to curve.
        """
    def Clear(self,isKeepEndPoints : bool) -> None: 
        """
        Clears parameters list.
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
    def GetParameter(self,theIndex : int) -> float: 
        """
        Returns parameter with the given index.
        """
    def GetPoint(self,theIndex : int) -> OCP.gp.gp_Pnt: 
        """
        Returns discretization point with the given index.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def InsertPoint(self,thePosition : int,thePoint : OCP.gp.gp_Pnt,theParamOnPCurve : float) -> None: 
        """
        Inserts new discretization point at the given position.
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
    def ParametersNb(self) -> int: 
        """
        Returns number of parameters.
        """
    def RemovePoint(self,theIndex : int) -> None: 
        """
        Removes point with the given index.
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
class IMeshData_TessellatedShape(IMeshData_Shape, OCP.Standard.Standard_Transient):
    """
    Interface class representing shaped model with deflection.
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
    def GetDeflection(self) -> float: 
        """
        Gets deflection value for the discrete model.
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
    def SetDeflection(self,theValue : float) -> None: 
        """
        Sets deflection value for the discrete model.
        """
    def SetShape(self,theShape : OCP.TopoDS.TopoDS_Shape) -> None: 
        """
        Assigns shape to discrete shape.
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
class IMeshData_Status():
    """
    Enumerates statuses used to notify state of discrete model.

    Members:

      IMeshData_NoError

      IMeshData_OpenWire

      IMeshData_SelfIntersectingWire

      IMeshData_Failure

      IMeshData_ReMesh

      IMeshData_UnorientedWire

      IMeshData_TooFewPoints

      IMeshData_Outdated

      IMeshData_Reused

      IMeshData_UserBreak
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
    IMeshData_Failure: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_Failure: 4>
    IMeshData_NoError: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_NoError: 0>
    IMeshData_OpenWire: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_OpenWire: 1>
    IMeshData_Outdated: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_Outdated: 64>
    IMeshData_ReMesh: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_ReMesh: 8>
    IMeshData_Reused: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_Reused: 128>
    IMeshData_SelfIntersectingWire: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_SelfIntersectingWire: 2>
    IMeshData_TooFewPoints: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_TooFewPoints: 32>
    IMeshData_UnorientedWire: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_UnorientedWire: 16>
    IMeshData_UserBreak: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_UserBreak: 256>
    __entries: dict # value = {'IMeshData_NoError': (<IMeshData_Status.IMeshData_NoError: 0>, None), 'IMeshData_OpenWire': (<IMeshData_Status.IMeshData_OpenWire: 1>, None), 'IMeshData_SelfIntersectingWire': (<IMeshData_Status.IMeshData_SelfIntersectingWire: 2>, None), 'IMeshData_Failure': (<IMeshData_Status.IMeshData_Failure: 4>, None), 'IMeshData_ReMesh': (<IMeshData_Status.IMeshData_ReMesh: 8>, None), 'IMeshData_UnorientedWire': (<IMeshData_Status.IMeshData_UnorientedWire: 16>, None), 'IMeshData_TooFewPoints': (<IMeshData_Status.IMeshData_TooFewPoints: 32>, None), 'IMeshData_Outdated': (<IMeshData_Status.IMeshData_Outdated: 64>, None), 'IMeshData_Reused': (<IMeshData_Status.IMeshData_Reused: 128>, None), 'IMeshData_UserBreak': (<IMeshData_Status.IMeshData_UserBreak: 256>, None)}
    __members__: dict # value = {'IMeshData_NoError': <IMeshData_Status.IMeshData_NoError: 0>, 'IMeshData_OpenWire': <IMeshData_Status.IMeshData_OpenWire: 1>, 'IMeshData_SelfIntersectingWire': <IMeshData_Status.IMeshData_SelfIntersectingWire: 2>, 'IMeshData_Failure': <IMeshData_Status.IMeshData_Failure: 4>, 'IMeshData_ReMesh': <IMeshData_Status.IMeshData_ReMesh: 8>, 'IMeshData_UnorientedWire': <IMeshData_Status.IMeshData_UnorientedWire: 16>, 'IMeshData_TooFewPoints': <IMeshData_Status.IMeshData_TooFewPoints: 32>, 'IMeshData_Outdated': <IMeshData_Status.IMeshData_Outdated: 64>, 'IMeshData_Reused': <IMeshData_Status.IMeshData_Reused: 128>, 'IMeshData_UserBreak': <IMeshData_Status.IMeshData_UserBreak: 256>}
    pass
class IMeshData_Face(IMeshData_TessellatedShape, IMeshData_Shape, OCP.Standard.Standard_Transient, IMeshData_StatusOwner):
    """
    Interface class representing discrete model of a face. Face model contains one or several wires. First wire is always outer one.
    """
    def AddWire(self,theWire : OCP.TopoDS.TopoDS_Wire,theEdgeNb : int=0) -> IMeshData_Wire: 
        """
        Adds wire to discrete model of face.
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
    def GetDeflection(self) -> float: 
        """
        Gets deflection value for the discrete model.
        """
    def GetFace(self) -> OCP.TopoDS.TopoDS_Face: 
        """
        Returns TopoDS_Face attached to model.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetShape(self) -> OCP.TopoDS.TopoDS_Shape: 
        """
        Returns shape assigned to discrete shape.
        """
    def GetStatusMask(self) -> int: 
        """
        Returns complete status mask.
        """
    def GetSurface(self) -> OCP.BRepAdaptor.BRepAdaptor_Surface: 
        """
        Returns face's surface.
        """
    def GetWire(self,theIndex : int) -> IMeshData_Wire: 
        """
        Returns discrete edge with the given index.
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def IsEqual(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is strictly equal to the given value.
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
    def IsSet(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is set.
        """
    def IsValid(self) -> bool: 
        """
        Returns whether the face discrete model is valid.
        """
    def SetDeflection(self,theValue : float) -> None: 
        """
        Sets deflection value for the discrete model.
        """
    def SetShape(self,theShape : OCP.TopoDS.TopoDS_Shape) -> None: 
        """
        Assigns shape to discrete shape.
        """
    def SetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UnsetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
        """
    def WiresNb(self) -> int: 
        """
        Returns number of wires.
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
class IMeshData_Edge(IMeshData_TessellatedShape, IMeshData_Shape, OCP.Standard.Standard_Transient, IMeshData_StatusOwner):
    """
    Interface class representing discrete model of an edge.
    """
    def Clear(self,isKeepEndPoints : bool) -> None: 
        """
        Clears curve and all pcurves assigned to the edge from discretization.
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
    def GetAngularDeflection(self) -> float: 
        """
        Gets value of angular deflection for the discrete model.
        """
    def GetCurve(self) -> IMeshData_Curve: 
        """
        Returns 3d curve associated with current edge.
        """
    def GetDeflection(self) -> float: 
        """
        Gets deflection value for the discrete model.
        """
    def GetDegenerated(self) -> bool: 
        """
        Returns degenerative flag. By default equals to flag stored in topological shape.
        """
    def GetEdge(self) -> OCP.TopoDS.TopoDS_Edge: 
        """
        Returns TopoDS_Edge attached to model.
        """
    def GetPCurve(self,theIndex : int) -> IMeshData_PCurve: 
        """
        Returns pcurve with the given index.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetSameParam(self) -> bool: 
        """
        Returns same param flag. By default equals to flag stored in topological shape.
        """
    def GetSameRange(self) -> bool: 
        """
        Returns same range flag. By default equals to flag stored in topological shape.
        """
    def GetShape(self) -> OCP.TopoDS.TopoDS_Shape: 
        """
        Returns shape assigned to discrete shape.
        """
    def GetStatusMask(self) -> int: 
        """
        Returns complete status mask.
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def IsEqual(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is strictly equal to the given value.
        """
    def IsFree(self) -> bool: 
        """
        Returns true in case if the edge is free one, i.e. it does not have pcurves.
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
    def IsSet(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is set.
        """
    def PCurvesNb(self) -> int: 
        """
        Returns number of pcurves assigned to current edge.
        """
    def SetAngularDeflection(self,theValue : float) -> None: 
        """
        Sets value of angular deflection for the discrete model.
        """
    def SetCurve(self,theCurve : IMeshData_Curve) -> None: 
        """
        Sets 3d curve associated with current edge.
        """
    def SetDeflection(self,theValue : float) -> None: 
        """
        Sets deflection value for the discrete model.
        """
    def SetDegenerated(self,theValue : bool) -> None: 
        """
        Updates degenerative flag.
        """
    def SetSameParam(self,theValue : bool) -> None: 
        """
        Updates same param flag.
        """
    def SetSameRange(self,theValue : bool) -> None: 
        """
        Updates same range flag.
        """
    def SetShape(self,theShape : OCP.TopoDS.TopoDS_Shape) -> None: 
        """
        Assigns shape to discrete shape.
        """
    def SetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UnsetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
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
class IMeshData_Wire(IMeshData_TessellatedShape, IMeshData_Shape, OCP.Standard.Standard_Transient, IMeshData_StatusOwner):
    """
    Interface class representing discrete model of a wire. Wire should represent an ordered set of edges.
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
    def EdgesNb(self) -> int: 
        """
        Returns number of edges.
        """
    def GetDeflection(self) -> float: 
        """
        Gets deflection value for the discrete model.
        """
    def GetEdge(self,theIndex : int) -> IMeshData_Edge: 
        """
        Returns discrete edge with the given index.
        """
    def GetEdgeOrientation(self,theIndex : int) -> OCP.TopAbs.TopAbs_Orientation: 
        """
        Returns True if orientation of discrete edge with the given index is forward.
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetShape(self) -> OCP.TopoDS.TopoDS_Shape: 
        """
        Returns shape assigned to discrete shape.
        """
    def GetStatusMask(self) -> int: 
        """
        Returns complete status mask.
        """
    def GetWire(self) -> OCP.TopoDS.TopoDS_Wire: 
        """
        Returns TopoDS_Face attached to model.
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def IsEqual(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is strictly equal to the given value.
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
    def IsSet(self,theValue : IMeshData_Status) -> bool: 
        """
        Returns true in case if status is set.
        """
    def SetDeflection(self,theValue : float) -> None: 
        """
        Sets deflection value for the discrete model.
        """
    def SetShape(self,theShape : OCP.TopoDS.TopoDS_Shape) -> None: 
        """
        Assigns shape to discrete shape.
        """
    def SetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UnsetStatus(self,theValue : IMeshData_Status) -> None: 
        """
        Adds status to status flags of a face.
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
IMeshData_Failure: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_Failure: 4>
IMeshData_NoError: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_NoError: 0>
IMeshData_OpenWire: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_OpenWire: 1>
IMeshData_Outdated: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_Outdated: 64>
IMeshData_ReMesh: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_ReMesh: 8>
IMeshData_Reused: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_Reused: 128>
IMeshData_SelfIntersectingWire: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_SelfIntersectingWire: 2>
IMeshData_TooFewPoints: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_TooFewPoints: 32>
IMeshData_UnorientedWire: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_UnorientedWire: 16>
IMeshData_UserBreak: OCP.IMeshData.IMeshData_Status # value = <IMeshData_Status.IMeshData_UserBreak: 256>
