import OCP.TColGeom
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
import OCP.Standard
import OCP.Geom
import OCP.NCollection
__all__  = [
"TColGeom_Array1OfBSplineCurve",
"TColGeom_Array1OfBezierCurve",
"TColGeom_Array1OfCurve",
"TColGeom_Array1OfSurface",
"TColGeom_Array2OfBezierSurface",
"TColGeom_Array2OfSurface",
"TColGeom_HArray1OfBSplineCurve",
"TColGeom_HArray1OfBezierCurve",
"TColGeom_HArray1OfCurve",
"TColGeom_HArray1OfSurface",
"TColGeom_HArray2OfSurface",
"TColGeom_SequenceOfBoundedCurve",
"TColGeom_SequenceOfCurve",
"TColGeom_HSequenceOfBoundedCurve",
"TColGeom_HSequenceOfCurve",
"TColGeom_SequenceOfSurface"
]
class TColGeom_Array1OfBSplineCurve():
    """
    The class NCollection_Array1 represents unidimensional arrays of fixed size known at run time. The range of the index is user defined. An array1 can be constructed with a "C array". This functionality is useful to call methods expecting an Array1. It allows to carry the bounds inside the arrays.
    """
    def Assign(self,theOther : TColGeom_Array1OfBSplineCurve) -> TColGeom_Array1OfBSplineCurve: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def Init(self,theValue : OCP.Geom.Geom_BSplineCurve) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
        """
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfBSplineCurve) -> TColGeom_Array1OfBSplineCurve: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_BSplineCurve) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_BSplineCurve: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfBSplineCurve) -> None: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theAlloc : Any,theLower : int,theUpper : int) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_BSplineCurve]: ...
    def __len__(self) -> int: ...
    pass
class TColGeom_Array1OfBezierCurve():
    """
    The class NCollection_Array1 represents unidimensional arrays of fixed size known at run time. The range of the index is user defined. An array1 can be constructed with a "C array". This functionality is useful to call methods expecting an Array1. It allows to carry the bounds inside the arrays.
    """
    def Assign(self,theOther : TColGeom_Array1OfBezierCurve) -> TColGeom_Array1OfBezierCurve: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def Init(self,theValue : OCP.Geom.Geom_BezierCurve) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
        """
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfBezierCurve) -> TColGeom_Array1OfBezierCurve: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_BezierCurve) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_BezierCurve: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfBezierCurve) -> None: ...
    @overload
    def __init__(self,theAlloc : Any,theLower : int,theUpper : int) -> None: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_BezierCurve]: ...
    def __len__(self) -> int: ...
    pass
class TColGeom_Array1OfCurve():
    """
    The class NCollection_Array1 represents unidimensional arrays of fixed size known at run time. The range of the index is user defined. An array1 can be constructed with a "C array". This functionality is useful to call methods expecting an Array1. It allows to carry the bounds inside the arrays.
    """
    def Assign(self,theOther : TColGeom_Array1OfCurve) -> TColGeom_Array1OfCurve: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def Init(self,theValue : OCP.Geom.Geom_Curve) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
        """
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfCurve) -> TColGeom_Array1OfCurve: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_Curve: ...
    @overload
    def __init__(self,theAlloc : Any,theLower : int,theUpper : int) -> None: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfCurve) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_Curve]: ...
    def __len__(self) -> int: ...
    pass
class TColGeom_Array1OfSurface():
    """
    The class NCollection_Array1 represents unidimensional arrays of fixed size known at run time. The range of the index is user defined. An array1 can be constructed with a "C array". This functionality is useful to call methods expecting an Array1. It allows to carry the bounds inside the arrays.
    """
    def Assign(self,theOther : TColGeom_Array1OfSurface) -> TColGeom_Array1OfSurface: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def Init(self,theValue : OCP.Geom.Geom_Surface) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
        """
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfSurface) -> TColGeom_Array1OfSurface: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_Surface) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_Surface: ...
    @overload
    def __init__(self,theAlloc : Any,theLower : int,theUpper : int) -> None: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfSurface) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_Surface]: ...
    def __len__(self) -> int: ...
    pass
class TColGeom_Array2OfBezierSurface():
    """
    Purpose: The class Array2 represents bi-dimensional arrays of fixed size known at run time. The ranges of indices are user defined.
    """
    def Assign(self,theOther : TColGeom_Array2OfBezierSurface) -> TColGeom_Array2OfBezierSurface: 
        """
        Assignment
        """
    @staticmethod
    def BeginPosition_s(theRowLower : int,arg1 : int,theColLower : int,theColUpper : int) -> int: 
        """
        None
        """
    def ColLength(self) -> int: 
        """
        Returns length of the column, i.e. number of rows
        """
    @staticmethod
    def LastPosition_s(theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> int: 
        """
        None
        """
    def Length(self) -> int: ...
    def LowerCol(self) -> int: 
        """
        LowerCol
        """
    def LowerRow(self) -> int: 
        """
        LowerRow
        """
    def Move(self,theOther : TColGeom_Array2OfBezierSurface) -> TColGeom_Array2OfBezierSurface: 
        """
        Move assignment. This array will borrow all the data from theOther. The moved object will be left uninitialized and should not be used anymore.
        """
    def NbColumns(self) -> int: 
        """
        Returns number of columns
        """
    def NbRows(self) -> int: 
        """
        Returns number of rows
        """
    def Resize(self,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def RowLength(self) -> int: 
        """
        Returns length of the row, i.e. number of columns
        """
    def SetValue(self,theRow : int,theCol : int,theItem : OCP.Geom.Geom_BezierSurface) -> None: 
        """
        SetValue
        """
    def Size(self) -> int: ...
    def UpperCol(self) -> int: 
        """
        UpperCol
        """
    def UpperRow(self) -> int: 
        """
        UpperRow
        """
    def __call__(self,theRow : int,theCol : int) -> OCP.Geom.Geom_BezierSurface: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_Array2OfBezierSurface) -> None: ...
    @overload
    def __init__(self,theAlloc : Any,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> None: ...
    @overload
    def __init__(self,theBegin : OCP.Geom.Geom_BezierSurface,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> None: ...
    def __len__(self) -> int: ...
    pass
class TColGeom_Array2OfSurface():
    """
    Purpose: The class Array2 represents bi-dimensional arrays of fixed size known at run time. The ranges of indices are user defined.
    """
    def Assign(self,theOther : TColGeom_Array2OfSurface) -> TColGeom_Array2OfSurface: 
        """
        Assignment
        """
    @staticmethod
    def BeginPosition_s(theRowLower : int,arg1 : int,theColLower : int,theColUpper : int) -> int: 
        """
        None
        """
    def ColLength(self) -> int: 
        """
        Returns length of the column, i.e. number of rows
        """
    @staticmethod
    def LastPosition_s(theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> int: 
        """
        None
        """
    def Length(self) -> int: ...
    def LowerCol(self) -> int: 
        """
        LowerCol
        """
    def LowerRow(self) -> int: 
        """
        LowerRow
        """
    def Move(self,theOther : TColGeom_Array2OfSurface) -> TColGeom_Array2OfSurface: 
        """
        Move assignment. This array will borrow all the data from theOther. The moved object will be left uninitialized and should not be used anymore.
        """
    def NbColumns(self) -> int: 
        """
        Returns number of columns
        """
    def NbRows(self) -> int: 
        """
        Returns number of rows
        """
    def Resize(self,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def RowLength(self) -> int: 
        """
        Returns length of the row, i.e. number of columns
        """
    def SetValue(self,theRow : int,theCol : int,theItem : OCP.Geom.Geom_Surface) -> None: 
        """
        SetValue
        """
    def Size(self) -> int: ...
    def UpperCol(self) -> int: 
        """
        UpperCol
        """
    def UpperRow(self) -> int: 
        """
        UpperRow
        """
    def __call__(self,theRow : int,theCol : int) -> OCP.Geom.Geom_Surface: ...
    @overload
    def __init__(self,theAlloc : Any,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> None: ...
    @overload
    def __init__(self,theBegin : OCP.Geom.Geom_Surface,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_Array2OfSurface) -> None: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> None: ...
    def __len__(self) -> int: ...
    pass
class TColGeom_HArray1OfBSplineCurve(TColGeom_Array1OfBSplineCurve, OCP.Standard.Standard_Transient):
    def Array1(self) -> TColGeom_Array1OfBSplineCurve: 
        """
        None
        """
    def Assign(self,theOther : TColGeom_Array1OfBSplineCurve) -> TColGeom_Array1OfBSplineCurve: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def ChangeArray1(self) -> TColGeom_Array1OfBSplineCurve: 
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
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def Init(self,theValue : OCP.Geom.Geom_BSplineCurve) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
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
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfBSplineCurve) -> TColGeom_Array1OfBSplineCurve: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_BSplineCurve) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_BSplineCurve: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfBSplineCurve) -> None: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theBegin : OCP.Geom.Geom_BSplineCurve,theLower : int,theUpper : int,arg4 : bool) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int,theValue : OCP.Geom.Geom_BSplineCurve) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_BSplineCurve]: ...
    def __len__(self) -> int: ...
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
class TColGeom_HArray1OfBezierCurve(TColGeom_Array1OfBezierCurve, OCP.Standard.Standard_Transient):
    def Array1(self) -> TColGeom_Array1OfBezierCurve: 
        """
        None
        """
    def Assign(self,theOther : TColGeom_Array1OfBezierCurve) -> TColGeom_Array1OfBezierCurve: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def ChangeArray1(self) -> TColGeom_Array1OfBezierCurve: 
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
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def Init(self,theValue : OCP.Geom.Geom_BezierCurve) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
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
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfBezierCurve) -> TColGeom_Array1OfBezierCurve: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_BezierCurve) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_BezierCurve: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfBezierCurve) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int,theValue : OCP.Geom.Geom_BezierCurve) -> None: ...
    @overload
    def __init__(self,theBegin : OCP.Geom.Geom_BezierCurve,theLower : int,theUpper : int,arg4 : bool) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_BezierCurve]: ...
    def __len__(self) -> int: ...
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
class TColGeom_HArray1OfCurve(TColGeom_Array1OfCurve, OCP.Standard.Standard_Transient):
    def Array1(self) -> TColGeom_Array1OfCurve: 
        """
        None
        """
    def Assign(self,theOther : TColGeom_Array1OfCurve) -> TColGeom_Array1OfCurve: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def ChangeArray1(self) -> TColGeom_Array1OfCurve: 
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
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def Init(self,theValue : OCP.Geom.Geom_Curve) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
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
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfCurve) -> TColGeom_Array1OfCurve: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_Curve: ...
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfCurve) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int,theValue : OCP.Geom.Geom_Curve) -> None: ...
    @overload
    def __init__(self,theBegin : OCP.Geom.Geom_Curve,theLower : int,theUpper : int,arg4 : bool) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_Curve]: ...
    def __len__(self) -> int: ...
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
class TColGeom_HArray1OfSurface(TColGeom_Array1OfSurface, OCP.Standard.Standard_Transient):
    def Array1(self) -> TColGeom_Array1OfSurface: 
        """
        None
        """
    def Assign(self,theOther : TColGeom_Array1OfSurface) -> TColGeom_Array1OfSurface: 
        """
        Copies data of theOther array to this. This array should be pre-allocated and have the same length as theOther; otherwise exception Standard_DimensionMismatch is thrown.
        """
    def ChangeArray1(self) -> TColGeom_Array1OfSurface: 
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
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def Init(self,theValue : OCP.Geom.Geom_Surface) -> None: 
        """
        Initialise the items with theValue
        """
    def IsDeletable(self) -> bool: 
        """
        None
        """
    def IsEmpty(self) -> bool: 
        """
        Return TRUE if array has zero length.
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
    def Length(self) -> int: 
        """
        Length query (the same)
        """
    def Lower(self) -> int: 
        """
        Lower bound
        """
    def Move(self,theOther : TColGeom_Array1OfSurface) -> TColGeom_Array1OfSurface: 
        """
        None
        """
    def Resize(self,theLower : int,theUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_Surface) -> None: 
        """
        Set value
        """
    def Size(self) -> int: 
        """
        Size query
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UpdateLowerBound(self,theLower : int) -> None: 
        """
        Changes the lowest bound. Do not move data
        """
    def UpdateUpperBound(self,theUpper : int) -> None: 
        """
        Changes the upper bound. Do not move data
        """
    def Upper(self) -> int: 
        """
        Upper bound
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_Surface: ...
    @overload
    def __init__(self,theLower : int,theUpper : int,theValue : OCP.Geom.Geom_Surface) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_Array1OfSurface) -> None: ...
    @overload
    def __init__(self,theLower : int,theUpper : int) -> None: ...
    @overload
    def __init__(self,theBegin : OCP.Geom.Geom_Surface,theLower : int,theUpper : int,arg4 : bool) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_Surface]: ...
    def __len__(self) -> int: ...
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
class TColGeom_HArray2OfSurface(TColGeom_Array2OfSurface, OCP.Standard.Standard_Transient):
    def Array2(self) -> TColGeom_Array2OfSurface: 
        """
        None
        """
    def Assign(self,theOther : TColGeom_Array2OfSurface) -> TColGeom_Array2OfSurface: 
        """
        Assignment
        """
    @staticmethod
    def BeginPosition_s(theRowLower : int,arg1 : int,theColLower : int,theColUpper : int) -> int: 
        """
        None
        """
    def ChangeArray2(self) -> TColGeom_Array2OfSurface: 
        """
        None
        """
    def ColLength(self) -> int: 
        """
        Returns length of the column, i.e. number of rows
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
    @staticmethod
    def LastPosition_s(theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int) -> int: 
        """
        None
        """
    def Length(self) -> int: ...
    def LowerCol(self) -> int: 
        """
        LowerCol
        """
    def LowerRow(self) -> int: 
        """
        LowerRow
        """
    def Move(self,theOther : TColGeom_Array2OfSurface) -> TColGeom_Array2OfSurface: 
        """
        Move assignment. This array will borrow all the data from theOther. The moved object will be left uninitialized and should not be used anymore.
        """
    def NbColumns(self) -> int: 
        """
        Returns number of columns
        """
    def NbRows(self) -> int: 
        """
        Returns number of rows
        """
    def Resize(self,theRowLower : int,theRowUpper : int,theColLower : int,theColUpper : int,theToCopyData : bool) -> None: 
        """
        Resizes the array to specified bounds. No re-allocation will be done if length of array does not change, but existing values will not be discarded if theToCopyData set to FALSE.
        """
    def RowLength(self) -> int: 
        """
        Returns length of the row, i.e. number of columns
        """
    def SetValue(self,theRow : int,theCol : int,theItem : OCP.Geom.Geom_Surface) -> None: 
        """
        SetValue
        """
    def Size(self) -> int: ...
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UpperCol(self) -> int: 
        """
        UpperCol
        """
    def UpperRow(self) -> int: 
        """
        UpperRow
        """
    def __call__(self,theRow : int,theCol : int) -> OCP.Geom.Geom_Surface: ...
    @overload
    def __init__(self,theRowLow : int,theRowUpp : int,theColLow : int,theColUpp : int,theValue : OCP.Geom.Geom_Surface) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_Array2OfSurface) -> None: ...
    @overload
    def __init__(self,theRowLow : int,theRowUpp : int,theColLow : int,theColUpp : int) -> None: ...
    def __len__(self) -> int: ...
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
class TColGeom_SequenceOfBoundedCurve(OCP.NCollection.NCollection_BaseSequence):
    """
    Purpose: Definition of a sequence of elements indexed by an Integer in range of 1..n
    """
    def Allocator(self) -> OCP.NCollection.NCollection_BaseAllocator: 
        """
        Returns attached allocator
        """
    @overload
    def Append(self,theItem : OCP.Geom.Geom_BoundedCurve) -> None: 
        """
        Append one item

        Append another sequence (making it empty)
        """
    @overload
    def Append(self,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: ...
    def Assign(self,theOther : TColGeom_SequenceOfBoundedCurve) -> TColGeom_SequenceOfBoundedCurve: 
        """
        Replace this sequence by the items of theOther. This method does not change the internal allocator.
        """
    def ChangeFirst(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        First item access
        """
    def ChangeLast(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Last item access
        """
    def ChangeValue(self,theIndex : int) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Variable item access by theIndex
        """
    def Clear(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator=None) -> None: 
        """
        Clear the items out, take a new allocator if non null
        """
    def Exchange(self,I : int,J : int) -> None: 
        """
        Exchange two members
        """
    def First(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        First item access
        """
    @overload
    def InsertAfter(self,theIndex : int,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: 
        """
        InsertAfter theIndex another sequence (making it empty)

        InsertAfter theIndex theItem
        """
    @overload
    def InsertAfter(self,theIndex : int,theItem : OCP.Geom.Geom_BoundedCurve) -> None: ...
    @overload
    def InsertBefore(self,theIndex : int,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: 
        """
        InsertBefore theIndex theItem

        InsertBefore theIndex another sequence (making it empty)
        """
    @overload
    def InsertBefore(self,theIndex : int,theItem : OCP.Geom.Geom_BoundedCurve) -> None: ...
    def IsEmpty(self) -> bool: 
        """
        Empty query
        """
    def Last(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Last item access
        """
    def Length(self) -> int: 
        """
        Number of items
        """
    def Lower(self) -> int: 
        """
        Method for consistency with other collections.
        """
    @overload
    def Prepend(self,theItem : OCP.Geom.Geom_BoundedCurve) -> None: 
        """
        Prepend one item

        Prepend another sequence (making it empty)
        """
    @overload
    def Prepend(self,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: ...
    @overload
    def Remove(self,theIndex : int) -> None: 
        """
        Remove one item

        Remove range of items
        """
    @overload
    def Remove(self,theFromIndex : int,theToIndex : int) -> None: ...
    def Reverse(self) -> None: 
        """
        Reverse sequence
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_BoundedCurve) -> None: 
        """
        Set item value by theIndex
        """
    def Size(self) -> int: 
        """
        Number of items
        """
    def Split(self,theIndex : int,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: 
        """
        Split in two sequences
        """
    def Upper(self) -> int: 
        """
        Method for consistency with other collections.
        """
    def Value(self,theIndex : int) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Constant item access by theIndex
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Constant operator()

        Variable operator()
        """
    @overload
    def __init__(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_SequenceOfBoundedCurve) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_BoundedCurve]: ...
    def __len__(self) -> int: ...
    @staticmethod
    def delNode_s(theNode : NCollection_SeqNode,theAl : OCP.NCollection.NCollection_BaseAllocator) -> None: 
        """
        Static deleter to be passed to BaseSequence
        """
    pass
class TColGeom_SequenceOfCurve(OCP.NCollection.NCollection_BaseSequence):
    """
    Purpose: Definition of a sequence of elements indexed by an Integer in range of 1..n
    """
    def Allocator(self) -> OCP.NCollection.NCollection_BaseAllocator: 
        """
        Returns attached allocator
        """
    @overload
    def Append(self,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        Append one item

        Append another sequence (making it empty)
        """
    @overload
    def Append(self,theSeq : TColGeom_SequenceOfCurve) -> None: ...
    def Assign(self,theOther : TColGeom_SequenceOfCurve) -> TColGeom_SequenceOfCurve: 
        """
        Replace this sequence by the items of theOther. This method does not change the internal allocator.
        """
    def ChangeFirst(self) -> OCP.Geom.Geom_Curve: 
        """
        First item access
        """
    def ChangeLast(self) -> OCP.Geom.Geom_Curve: 
        """
        Last item access
        """
    def ChangeValue(self,theIndex : int) -> OCP.Geom.Geom_Curve: 
        """
        Variable item access by theIndex
        """
    def Clear(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator=None) -> None: 
        """
        Clear the items out, take a new allocator if non null
        """
    def Exchange(self,I : int,J : int) -> None: 
        """
        Exchange two members
        """
    def First(self) -> OCP.Geom.Geom_Curve: 
        """
        First item access
        """
    @overload
    def InsertAfter(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        InsertAfter theIndex another sequence (making it empty)

        InsertAfter theIndex theItem
        """
    @overload
    def InsertAfter(self,theIndex : int,theSeq : TColGeom_SequenceOfCurve) -> None: ...
    @overload
    def InsertBefore(self,theIndex : int,theSeq : TColGeom_SequenceOfCurve) -> None: 
        """
        InsertBefore theIndex theItem

        InsertBefore theIndex another sequence (making it empty)
        """
    @overload
    def InsertBefore(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: ...
    def IsEmpty(self) -> bool: 
        """
        Empty query
        """
    def Last(self) -> OCP.Geom.Geom_Curve: 
        """
        Last item access
        """
    def Length(self) -> int: 
        """
        Number of items
        """
    def Lower(self) -> int: 
        """
        Method for consistency with other collections.
        """
    @overload
    def Prepend(self,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        Prepend one item

        Prepend another sequence (making it empty)
        """
    @overload
    def Prepend(self,theSeq : TColGeom_SequenceOfCurve) -> None: ...
    @overload
    def Remove(self,theFromIndex : int,theToIndex : int) -> None: 
        """
        Remove one item

        Remove range of items
        """
    @overload
    def Remove(self,theIndex : int) -> None: ...
    def Reverse(self) -> None: 
        """
        Reverse sequence
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        Set item value by theIndex
        """
    def Size(self) -> int: 
        """
        Number of items
        """
    def Split(self,theIndex : int,theSeq : TColGeom_SequenceOfCurve) -> None: 
        """
        Split in two sequences
        """
    def Upper(self) -> int: 
        """
        Method for consistency with other collections.
        """
    def Value(self,theIndex : int) -> OCP.Geom.Geom_Curve: 
        """
        Constant item access by theIndex
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_Curve: 
        """
        Constant operator()

        Variable operator()
        """
    @overload
    def __init__(self,theOther : TColGeom_SequenceOfCurve) -> None: ...
    @overload
    def __init__(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_Curve]: ...
    def __len__(self) -> int: ...
    @staticmethod
    def delNode_s(theNode : NCollection_SeqNode,theAl : OCP.NCollection.NCollection_BaseAllocator) -> None: 
        """
        Static deleter to be passed to BaseSequence
        """
    pass
class TColGeom_HSequenceOfBoundedCurve(TColGeom_SequenceOfBoundedCurve, OCP.NCollection.NCollection_BaseSequence, OCP.Standard.Standard_Transient):
    def Allocator(self) -> OCP.NCollection.NCollection_BaseAllocator: 
        """
        Returns attached allocator
        """
    @overload
    def Append(self,theSequence : TColGeom_SequenceOfBoundedCurve) -> None: 
        """
        None

        None
        """
    @overload
    def Append(self,theItem : OCP.Geom.Geom_BoundedCurve) -> None: ...
    def Assign(self,theOther : TColGeom_SequenceOfBoundedCurve) -> TColGeom_SequenceOfBoundedCurve: 
        """
        Replace this sequence by the items of theOther. This method does not change the internal allocator.
        """
    def ChangeFirst(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        First item access
        """
    def ChangeLast(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Last item access
        """
    def ChangeSequence(self) -> TColGeom_SequenceOfBoundedCurve: 
        """
        None
        """
    def ChangeValue(self,theIndex : int) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Variable item access by theIndex
        """
    def Clear(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator=None) -> None: 
        """
        Clear the items out, take a new allocator if non null
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
    def Exchange(self,I : int,J : int) -> None: 
        """
        Exchange two members
        """
    def First(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        First item access
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
    def InsertAfter(self,theIndex : int,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: 
        """
        InsertAfter theIndex another sequence (making it empty)

        InsertAfter theIndex theItem
        """
    @overload
    def InsertAfter(self,theIndex : int,theItem : OCP.Geom.Geom_BoundedCurve) -> None: ...
    @overload
    def InsertBefore(self,theIndex : int,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: 
        """
        InsertBefore theIndex theItem

        InsertBefore theIndex another sequence (making it empty)
        """
    @overload
    def InsertBefore(self,theIndex : int,theItem : OCP.Geom.Geom_BoundedCurve) -> None: ...
    def IsEmpty(self) -> bool: 
        """
        Empty query
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
    def Last(self) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Last item access
        """
    def Length(self) -> int: 
        """
        Number of items
        """
    def Lower(self) -> int: 
        """
        Method for consistency with other collections.
        """
    @overload
    def Prepend(self,theItem : OCP.Geom.Geom_BoundedCurve) -> None: 
        """
        Prepend one item

        Prepend another sequence (making it empty)
        """
    @overload
    def Prepend(self,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: ...
    @overload
    def Remove(self,theIndex : int) -> None: 
        """
        Remove one item

        Remove range of items
        """
    @overload
    def Remove(self,theFromIndex : int,theToIndex : int) -> None: ...
    def Reverse(self) -> None: 
        """
        Reverse sequence
        """
    def Sequence(self) -> TColGeom_SequenceOfBoundedCurve: 
        """
        None
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_BoundedCurve) -> None: 
        """
        Set item value by theIndex
        """
    def Size(self) -> int: 
        """
        Number of items
        """
    def Split(self,theIndex : int,theSeq : TColGeom_SequenceOfBoundedCurve) -> None: 
        """
        Split in two sequences
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def Upper(self) -> int: 
        """
        Method for consistency with other collections.
        """
    def Value(self,theIndex : int) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Constant item access by theIndex
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_BoundedCurve: 
        """
        Constant operator()

        Variable operator()
        """
    @overload
    def __init__(self,theOther : TColGeom_SequenceOfBoundedCurve) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_BoundedCurve]: ...
    def __len__(self) -> int: ...
    @staticmethod
    def delNode_s(theNode : NCollection_SeqNode,theAl : OCP.NCollection.NCollection_BaseAllocator) -> None: 
        """
        Static deleter to be passed to BaseSequence
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
class TColGeom_HSequenceOfCurve(TColGeom_SequenceOfCurve, OCP.NCollection.NCollection_BaseSequence, OCP.Standard.Standard_Transient):
    def Allocator(self) -> OCP.NCollection.NCollection_BaseAllocator: 
        """
        Returns attached allocator
        """
    @overload
    def Append(self,theSequence : TColGeom_SequenceOfCurve) -> None: 
        """
        None

        None
        """
    @overload
    def Append(self,theItem : OCP.Geom.Geom_Curve) -> None: ...
    def Assign(self,theOther : TColGeom_SequenceOfCurve) -> TColGeom_SequenceOfCurve: 
        """
        Replace this sequence by the items of theOther. This method does not change the internal allocator.
        """
    def ChangeFirst(self) -> OCP.Geom.Geom_Curve: 
        """
        First item access
        """
    def ChangeLast(self) -> OCP.Geom.Geom_Curve: 
        """
        Last item access
        """
    def ChangeSequence(self) -> TColGeom_SequenceOfCurve: 
        """
        None
        """
    def ChangeValue(self,theIndex : int) -> OCP.Geom.Geom_Curve: 
        """
        Variable item access by theIndex
        """
    def Clear(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator=None) -> None: 
        """
        Clear the items out, take a new allocator if non null
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
    def Exchange(self,I : int,J : int) -> None: 
        """
        Exchange two members
        """
    def First(self) -> OCP.Geom.Geom_Curve: 
        """
        First item access
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
    def InsertAfter(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        InsertAfter theIndex another sequence (making it empty)

        InsertAfter theIndex theItem
        """
    @overload
    def InsertAfter(self,theIndex : int,theSeq : TColGeom_SequenceOfCurve) -> None: ...
    @overload
    def InsertBefore(self,theIndex : int,theSeq : TColGeom_SequenceOfCurve) -> None: 
        """
        InsertBefore theIndex theItem

        InsertBefore theIndex another sequence (making it empty)
        """
    @overload
    def InsertBefore(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: ...
    def IsEmpty(self) -> bool: 
        """
        Empty query
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
    def Last(self) -> OCP.Geom.Geom_Curve: 
        """
        Last item access
        """
    def Length(self) -> int: 
        """
        Number of items
        """
    def Lower(self) -> int: 
        """
        Method for consistency with other collections.
        """
    @overload
    def Prepend(self,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        Prepend one item

        Prepend another sequence (making it empty)
        """
    @overload
    def Prepend(self,theSeq : TColGeom_SequenceOfCurve) -> None: ...
    @overload
    def Remove(self,theFromIndex : int,theToIndex : int) -> None: 
        """
        Remove one item

        Remove range of items
        """
    @overload
    def Remove(self,theIndex : int) -> None: ...
    def Reverse(self) -> None: 
        """
        Reverse sequence
        """
    def Sequence(self) -> TColGeom_SequenceOfCurve: 
        """
        None
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_Curve) -> None: 
        """
        Set item value by theIndex
        """
    def Size(self) -> int: 
        """
        Number of items
        """
    def Split(self,theIndex : int,theSeq : TColGeom_SequenceOfCurve) -> None: 
        """
        Split in two sequences
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def Upper(self) -> int: 
        """
        Method for consistency with other collections.
        """
    def Value(self,theIndex : int) -> OCP.Geom.Geom_Curve: 
        """
        Constant item access by theIndex
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_Curve: 
        """
        Constant operator()

        Variable operator()
        """
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_SequenceOfCurve) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_Curve]: ...
    def __len__(self) -> int: ...
    @staticmethod
    def delNode_s(theNode : NCollection_SeqNode,theAl : OCP.NCollection.NCollection_BaseAllocator) -> None: 
        """
        Static deleter to be passed to BaseSequence
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
class TColGeom_SequenceOfSurface(OCP.NCollection.NCollection_BaseSequence):
    """
    Purpose: Definition of a sequence of elements indexed by an Integer in range of 1..n
    """
    def Allocator(self) -> OCP.NCollection.NCollection_BaseAllocator: 
        """
        Returns attached allocator
        """
    @overload
    def Append(self,theSeq : TColGeom_SequenceOfSurface) -> None: 
        """
        Append one item

        Append another sequence (making it empty)
        """
    @overload
    def Append(self,theItem : OCP.Geom.Geom_Surface) -> None: ...
    def Assign(self,theOther : TColGeom_SequenceOfSurface) -> TColGeom_SequenceOfSurface: 
        """
        Replace this sequence by the items of theOther. This method does not change the internal allocator.
        """
    def ChangeFirst(self) -> OCP.Geom.Geom_Surface: 
        """
        First item access
        """
    def ChangeLast(self) -> OCP.Geom.Geom_Surface: 
        """
        Last item access
        """
    def ChangeValue(self,theIndex : int) -> OCP.Geom.Geom_Surface: 
        """
        Variable item access by theIndex
        """
    def Clear(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator=None) -> None: 
        """
        Clear the items out, take a new allocator if non null
        """
    def Exchange(self,I : int,J : int) -> None: 
        """
        Exchange two members
        """
    def First(self) -> OCP.Geom.Geom_Surface: 
        """
        First item access
        """
    @overload
    def InsertAfter(self,theIndex : int,theSeq : TColGeom_SequenceOfSurface) -> None: 
        """
        InsertAfter theIndex another sequence (making it empty)

        InsertAfter theIndex theItem
        """
    @overload
    def InsertAfter(self,theIndex : int,theItem : OCP.Geom.Geom_Surface) -> None: ...
    @overload
    def InsertBefore(self,theIndex : int,theSeq : TColGeom_SequenceOfSurface) -> None: 
        """
        InsertBefore theIndex theItem

        InsertBefore theIndex another sequence (making it empty)
        """
    @overload
    def InsertBefore(self,theIndex : int,theItem : OCP.Geom.Geom_Surface) -> None: ...
    def IsEmpty(self) -> bool: 
        """
        Empty query
        """
    def Last(self) -> OCP.Geom.Geom_Surface: 
        """
        Last item access
        """
    def Length(self) -> int: 
        """
        Number of items
        """
    def Lower(self) -> int: 
        """
        Method for consistency with other collections.
        """
    @overload
    def Prepend(self,theSeq : TColGeom_SequenceOfSurface) -> None: 
        """
        Prepend one item

        Prepend another sequence (making it empty)
        """
    @overload
    def Prepend(self,theItem : OCP.Geom.Geom_Surface) -> None: ...
    @overload
    def Remove(self,theIndex : int) -> None: 
        """
        Remove one item

        Remove range of items
        """
    @overload
    def Remove(self,theFromIndex : int,theToIndex : int) -> None: ...
    def Reverse(self) -> None: 
        """
        Reverse sequence
        """
    def SetValue(self,theIndex : int,theItem : OCP.Geom.Geom_Surface) -> None: 
        """
        Set item value by theIndex
        """
    def Size(self) -> int: 
        """
        Number of items
        """
    def Split(self,theIndex : int,theSeq : TColGeom_SequenceOfSurface) -> None: 
        """
        Split in two sequences
        """
    def Upper(self) -> int: 
        """
        Method for consistency with other collections.
        """
    def Value(self,theIndex : int) -> OCP.Geom.Geom_Surface: 
        """
        Constant item access by theIndex
        """
    def __bool__(self) -> bool: ...
    def __call__(self,theIndex : int) -> OCP.Geom.Geom_Surface: 
        """
        Constant operator()

        Variable operator()
        """
    @overload
    def __init__(self,theAllocator : OCP.NCollection.NCollection_BaseAllocator) -> None: ...
    @overload
    def __init__(self,theOther : TColGeom_SequenceOfSurface) -> None: ...
    @overload
    def __init__(self) -> None: ...
    def __iter__(self) -> Iterator[OCP.Geom.Geom_Surface]: ...
    def __len__(self) -> int: ...
    @staticmethod
    def delNode_s(theNode : NCollection_SeqNode,theAl : OCP.NCollection.NCollection_BaseAllocator) -> None: 
        """
        Static deleter to be passed to BaseSequence
        """
    pass
