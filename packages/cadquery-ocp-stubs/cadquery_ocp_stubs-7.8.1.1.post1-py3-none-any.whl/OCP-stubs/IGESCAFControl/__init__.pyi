import OCP.IGESCAFControl
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
import OCP.NCollection
import OCP.TCollection
import OCP.Transfer
import OCP.TDocStd
import OCP.Interface
import OCP.XSControl
import OCP.Quantity
import OCP.Standard
import OCP.DE
import OCP.TDF
import OCP.IGESControl
import OCP.TColStd
import OCP.IGESData
import OCP.IFSelect
import io
import OCP.TopoDS
__all__  = [
"IGESCAFControl",
"IGESCAFControl_ConfigurationNode",
"IGESCAFControl_Provider",
"IGESCAFControl_Reader",
"IGESCAFControl_Writer"
]
class IGESCAFControl():
    """
    Provides high-level API to translate IGES file to and from DECAF document
    """
    @staticmethod
    def DecodeColor_s(col : int) -> OCP.Quantity.Quantity_Color: 
        """
        Provides a tool for writing IGES file Converts IGES color index to CASCADE color
        """
    @staticmethod
    def EncodeColor_s(col : OCP.Quantity.Quantity_Color) -> int: 
        """
        Tries to Convert CASCADE color to IGES color index If no corresponding color defined in IGES, returns 0
        """
    def __init__(self) -> None: ...
    pass
class IGESCAFControl_ConfigurationNode(OCP.DE.DE_ConfigurationNode, OCP.Standard.Standard_Transient):
    """
    The purpose of this class is to configure the transfer process for IGES format Stores the necessary settings for IGESCAFControl_Provider. Configures and creates special provider to transfer IGES files.
    """
    class ReadMode_BSplineContinuity_e():
        """
        None

        Members:

          ReadMode_BSplineContinuity_C0

          ReadMode_BSplineContinuity_C1

          ReadMode_BSplineContinuity_C2
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
        ReadMode_BSplineContinuity_C0: OCP.IGESCAFControl.ReadMode_BSplineContinuity_e # value = <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C0: 0>
        ReadMode_BSplineContinuity_C1: OCP.IGESCAFControl.ReadMode_BSplineContinuity_e # value = <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C1: 1>
        ReadMode_BSplineContinuity_C2: OCP.IGESCAFControl.ReadMode_BSplineContinuity_e # value = <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C2: 2>
        __entries: dict # value = {'ReadMode_BSplineContinuity_C0': (<ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C0: 0>, None), 'ReadMode_BSplineContinuity_C1': (<ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C1: 1>, None), 'ReadMode_BSplineContinuity_C2': (<ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C2: 2>, None)}
        __members__: dict # value = {'ReadMode_BSplineContinuity_C0': <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C0: 0>, 'ReadMode_BSplineContinuity_C1': <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C1: 1>, 'ReadMode_BSplineContinuity_C2': <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C2: 2>}
        pass
    class ReadMode_MaxPrecision_e():
        """
        None

        Members:

          ReadMode_MaxPrecision_Preferred

          ReadMode_MaxPrecision_Forced
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
        ReadMode_MaxPrecision_Forced: OCP.IGESCAFControl.ReadMode_MaxPrecision_e # value = <ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Forced: 1>
        ReadMode_MaxPrecision_Preferred: OCP.IGESCAFControl.ReadMode_MaxPrecision_e # value = <ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Preferred: 0>
        __entries: dict # value = {'ReadMode_MaxPrecision_Preferred': (<ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Preferred: 0>, None), 'ReadMode_MaxPrecision_Forced': (<ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Forced: 1>, None)}
        __members__: dict # value = {'ReadMode_MaxPrecision_Preferred': <ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Preferred: 0>, 'ReadMode_MaxPrecision_Forced': <ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Forced: 1>}
        pass
    class ReadMode_Precision_e():
        """
        None

        Members:

          ReadMode_Precision_File

          ReadMode_Precision_User
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
        ReadMode_Precision_File: OCP.IGESCAFControl.ReadMode_Precision_e # value = <ReadMode_Precision_e.ReadMode_Precision_File: 0>
        ReadMode_Precision_User: OCP.IGESCAFControl.ReadMode_Precision_e # value = <ReadMode_Precision_e.ReadMode_Precision_User: 1>
        __entries: dict # value = {'ReadMode_Precision_File': (<ReadMode_Precision_e.ReadMode_Precision_File: 0>, None), 'ReadMode_Precision_User': (<ReadMode_Precision_e.ReadMode_Precision_User: 1>, None)}
        __members__: dict # value = {'ReadMode_Precision_File': <ReadMode_Precision_e.ReadMode_Precision_File: 0>, 'ReadMode_Precision_User': <ReadMode_Precision_e.ReadMode_Precision_User: 1>}
        pass
    class ReadMode_SurfaceCurve_e():
        """
        None

        Members:

          ReadMode_SurfaceCurve_Default

          ReadMode_SurfaceCurve_2DUse_Preferred

          ReadMode_SurfaceCurve_2DUse_Forced

          ReadMode_SurfaceCurve_3DUse_Preferred

          ReadMode_SurfaceCurve_3DUse_Forced
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
        ReadMode_SurfaceCurve_2DUse_Forced: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Forced: -2>
        ReadMode_SurfaceCurve_2DUse_Preferred: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Preferred: 2>
        ReadMode_SurfaceCurve_3DUse_Forced: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Forced: -3>
        ReadMode_SurfaceCurve_3DUse_Preferred: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Preferred: 3>
        ReadMode_SurfaceCurve_Default: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_Default: 0>
        __entries: dict # value = {'ReadMode_SurfaceCurve_Default': (<ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_Default: 0>, None), 'ReadMode_SurfaceCurve_2DUse_Preferred': (<ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Preferred: 2>, None), 'ReadMode_SurfaceCurve_2DUse_Forced': (<ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Forced: -2>, None), 'ReadMode_SurfaceCurve_3DUse_Preferred': (<ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Preferred: 3>, None), 'ReadMode_SurfaceCurve_3DUse_Forced': (<ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Forced: -3>, None)}
        __members__: dict # value = {'ReadMode_SurfaceCurve_Default': <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_Default: 0>, 'ReadMode_SurfaceCurve_2DUse_Preferred': <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Preferred: 2>, 'ReadMode_SurfaceCurve_2DUse_Forced': <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Forced: -2>, 'ReadMode_SurfaceCurve_3DUse_Preferred': <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Preferred: 3>, 'ReadMode_SurfaceCurve_3DUse_Forced': <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Forced: -3>}
        pass
    class WriteMode_BRep_e():
        """
        None

        Members:

          WriteMode_BRep_Faces

          WriteMode_BRep_BRep
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
        WriteMode_BRep_BRep: OCP.IGESCAFControl.WriteMode_BRep_e # value = <WriteMode_BRep_e.WriteMode_BRep_BRep: 1>
        WriteMode_BRep_Faces: OCP.IGESCAFControl.WriteMode_BRep_e # value = <WriteMode_BRep_e.WriteMode_BRep_Faces: 0>
        __entries: dict # value = {'WriteMode_BRep_Faces': (<WriteMode_BRep_e.WriteMode_BRep_Faces: 0>, None), 'WriteMode_BRep_BRep': (<WriteMode_BRep_e.WriteMode_BRep_BRep: 1>, None)}
        __members__: dict # value = {'WriteMode_BRep_Faces': <WriteMode_BRep_e.WriteMode_BRep_Faces: 0>, 'WriteMode_BRep_BRep': <WriteMode_BRep_e.WriteMode_BRep_BRep: 1>}
        pass
    class WriteMode_ConvertSurface_e():
        """
        None

        Members:

          WriteMode_ConvertSurface_Off

          WriteMode_ConvertSurface_On
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
        WriteMode_ConvertSurface_Off: OCP.IGESCAFControl.WriteMode_ConvertSurface_e # value = <WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_Off: 0>
        WriteMode_ConvertSurface_On: OCP.IGESCAFControl.WriteMode_ConvertSurface_e # value = <WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_On: 1>
        __entries: dict # value = {'WriteMode_ConvertSurface_Off': (<WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_Off: 0>, None), 'WriteMode_ConvertSurface_On': (<WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_On: 1>, None)}
        __members__: dict # value = {'WriteMode_ConvertSurface_Off': <WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_Off: 0>, 'WriteMode_ConvertSurface_On': <WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_On: 1>}
        pass
    class WriteMode_PlaneMode_e():
        """
        None

        Members:

          WriteMode_PlaneMode_Plane

          WriteMode_PlaneMode_BSpline
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
        WriteMode_PlaneMode_BSpline: OCP.IGESCAFControl.WriteMode_PlaneMode_e # value = <WriteMode_PlaneMode_e.WriteMode_PlaneMode_BSpline: 1>
        WriteMode_PlaneMode_Plane: OCP.IGESCAFControl.WriteMode_PlaneMode_e # value = <WriteMode_PlaneMode_e.WriteMode_PlaneMode_Plane: 0>
        __entries: dict # value = {'WriteMode_PlaneMode_Plane': (<WriteMode_PlaneMode_e.WriteMode_PlaneMode_Plane: 0>, None), 'WriteMode_PlaneMode_BSpline': (<WriteMode_PlaneMode_e.WriteMode_PlaneMode_BSpline: 1>, None)}
        __members__: dict # value = {'WriteMode_PlaneMode_Plane': <WriteMode_PlaneMode_e.WriteMode_PlaneMode_Plane: 0>, 'WriteMode_PlaneMode_BSpline': <WriteMode_PlaneMode_e.WriteMode_PlaneMode_BSpline: 1>}
        pass
    class WriteMode_PrecisionMode_e():
        """
        None

        Members:

          WriteMode_PrecisionMode_Least

          WriteMode_PrecisionMode_Average

          WriteMode_PrecisionMode_Greatest

          WriteMode_PrecisionMode_Session
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
        WriteMode_PrecisionMode_Average: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Average: 0>
        WriteMode_PrecisionMode_Greatest: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Greatest: 1>
        WriteMode_PrecisionMode_Least: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Least: -1>
        WriteMode_PrecisionMode_Session: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Session: 2>
        __entries: dict # value = {'WriteMode_PrecisionMode_Least': (<WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Least: -1>, None), 'WriteMode_PrecisionMode_Average': (<WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Average: 0>, None), 'WriteMode_PrecisionMode_Greatest': (<WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Greatest: 1>, None), 'WriteMode_PrecisionMode_Session': (<WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Session: 2>, None)}
        __members__: dict # value = {'WriteMode_PrecisionMode_Least': <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Least: -1>, 'WriteMode_PrecisionMode_Average': <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Average: 0>, 'WriteMode_PrecisionMode_Greatest': <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Greatest: 1>, 'WriteMode_PrecisionMode_Session': <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Session: 2>}
        pass
    def BuildProvider(self) -> OCP.DE.DE_Provider: 
        """
        Creates new provider for the own format
        """
    def CheckContent(self,theBuffer : OCP.NCollection.NCollection_Buffer) -> bool: 
        """
        Checks the file content to verify a format
        """
    def CheckExtension(self,theExtension : OCP.TCollection.TCollection_AsciiString) -> bool: 
        """
        Checks the file extension to verify a format
        """
    def Copy(self) -> OCP.DE.DE_ConfigurationNode: 
        """
        Copies values of all fields
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
    def GetExtensions(self) -> OCP.TColStd.TColStd_ListOfAsciiString: 
        """
        Gets list of supported file extensions
        """
    def GetFormat(self) -> OCP.TCollection.TCollection_AsciiString: 
        """
        Gets CAD format name of associated provider
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetVendor(self) -> OCP.TCollection.TCollection_AsciiString: 
        """
        Gets provider's vendor name of associated provider
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def IsEnabled(self) -> bool: 
        """
        Gets the provider loading status
        """
    def IsExportSupported(self) -> bool: 
        """
        Checks the export supporting
        """
    def IsImportSupported(self) -> bool: 
        """
        Checks the import supporting
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
    def Load(self,theResource : OCP.DE.DE_ConfigurationContext) -> bool: 
        """
        Updates values according the resource
        """
    def Save(self) -> OCP.TCollection.TCollection_AsciiString: 
        """
        Writes configuration to the string
        """
    def SetEnabled(self,theIsLoaded : bool) -> None: 
        """
        Sets the provider loading status
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def UpdateLoad(self,theToImport : bool,theToKeep : bool) -> bool: 
        """
        Update loading status. Checking for the ability to read and write.
        """
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theNode : IGESCAFControl_ConfigurationNode) -> None: ...
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
    ReadMode_BSplineContinuity_C0: OCP.IGESCAFControl.ReadMode_BSplineContinuity_e # value = <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C0: 0>
    ReadMode_BSplineContinuity_C1: OCP.IGESCAFControl.ReadMode_BSplineContinuity_e # value = <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C1: 1>
    ReadMode_BSplineContinuity_C2: OCP.IGESCAFControl.ReadMode_BSplineContinuity_e # value = <ReadMode_BSplineContinuity_e.ReadMode_BSplineContinuity_C2: 2>
    ReadMode_MaxPrecision_Forced: OCP.IGESCAFControl.ReadMode_MaxPrecision_e # value = <ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Forced: 1>
    ReadMode_MaxPrecision_Preferred: OCP.IGESCAFControl.ReadMode_MaxPrecision_e # value = <ReadMode_MaxPrecision_e.ReadMode_MaxPrecision_Preferred: 0>
    ReadMode_Precision_File: OCP.IGESCAFControl.ReadMode_Precision_e # value = <ReadMode_Precision_e.ReadMode_Precision_File: 0>
    ReadMode_Precision_User: OCP.IGESCAFControl.ReadMode_Precision_e # value = <ReadMode_Precision_e.ReadMode_Precision_User: 1>
    ReadMode_SurfaceCurve_2DUse_Forced: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Forced: -2>
    ReadMode_SurfaceCurve_2DUse_Preferred: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_2DUse_Preferred: 2>
    ReadMode_SurfaceCurve_3DUse_Forced: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Forced: -3>
    ReadMode_SurfaceCurve_3DUse_Preferred: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_3DUse_Preferred: 3>
    ReadMode_SurfaceCurve_Default: OCP.IGESCAFControl.ReadMode_SurfaceCurve_e # value = <ReadMode_SurfaceCurve_e.ReadMode_SurfaceCurve_Default: 0>
    WriteMode_BRep_BRep: OCP.IGESCAFControl.WriteMode_BRep_e # value = <WriteMode_BRep_e.WriteMode_BRep_BRep: 1>
    WriteMode_BRep_Faces: OCP.IGESCAFControl.WriteMode_BRep_e # value = <WriteMode_BRep_e.WriteMode_BRep_Faces: 0>
    WriteMode_ConvertSurface_Off: OCP.IGESCAFControl.WriteMode_ConvertSurface_e # value = <WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_Off: 0>
    WriteMode_ConvertSurface_On: OCP.IGESCAFControl.WriteMode_ConvertSurface_e # value = <WriteMode_ConvertSurface_e.WriteMode_ConvertSurface_On: 1>
    WriteMode_PlaneMode_BSpline: OCP.IGESCAFControl.WriteMode_PlaneMode_e # value = <WriteMode_PlaneMode_e.WriteMode_PlaneMode_BSpline: 1>
    WriteMode_PlaneMode_Plane: OCP.IGESCAFControl.WriteMode_PlaneMode_e # value = <WriteMode_PlaneMode_e.WriteMode_PlaneMode_Plane: 0>
    WriteMode_PrecisionMode_Average: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Average: 0>
    WriteMode_PrecisionMode_Greatest: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Greatest: 1>
    WriteMode_PrecisionMode_Least: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Least: -1>
    WriteMode_PrecisionMode_Session: OCP.IGESCAFControl.WriteMode_PrecisionMode_e # value = <WriteMode_PrecisionMode_e.WriteMode_PrecisionMode_Session: 2>
    pass
class IGESCAFControl_Provider(OCP.DE.DE_Provider, OCP.Standard.Standard_Transient):
    """
    The class to transfer IGES files. Reads and Writes any IGES files into/from OCCT. Each operation needs configuration node.
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
    def GetFormat(self) -> OCP.TCollection.TCollection_AsciiString: 
        """
        Gets CAD format name of associated provider
        """
    def GetNode(self) -> OCP.DE.DE_ConfigurationNode: 
        """
        Gets internal configuration node
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GetVendor(self) -> OCP.TCollection.TCollection_AsciiString: 
        """
        Gets provider's vendor name of associated provider
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
    @overload
    def Read(self,thePath : OCP.TCollection.TCollection_AsciiString,theShape : OCP.TopoDS.TopoDS_Shape,theWS : OCP.XSControl.XSControl_WorkSession,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Reads a CAD file, according internal configuration

        Reads a CAD file, according internal configuration

        Reads a CAD file, according internal configuration

        Reads a CAD file, according internal configuration
        """
    @overload
    def Read(self,thePath : OCP.TCollection.TCollection_AsciiString,theDocument : OCP.TDocStd.TDocStd_Document,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    @overload
    def Read(self,thePath : OCP.TCollection.TCollection_AsciiString,theShape : OCP.TopoDS.TopoDS_Shape,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    @overload
    def Read(self,thePath : OCP.TCollection.TCollection_AsciiString,theDocument : OCP.TDocStd.TDocStd_Document,theWS : OCP.XSControl.XSControl_WorkSession,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    def SetNode(self,theNode : OCP.DE.DE_ConfigurationNode) -> None: 
        """
        Sets internal configuration node
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    @overload
    def Write(self,thePath : OCP.TCollection.TCollection_AsciiString,theShape : OCP.TopoDS.TopoDS_Shape,theWS : OCP.XSControl.XSControl_WorkSession,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Writes a CAD file, according internal configuration

        Writes a CAD file, according internal configuration

        Writes a CAD file, according internal configuration

        Writes a CAD file, according internal configuration
        """
    @overload
    def Write(self,thePath : OCP.TCollection.TCollection_AsciiString,theDocument : OCP.TDocStd.TDocStd_Document,theWS : OCP.XSControl.XSControl_WorkSession,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    @overload
    def Write(self,thePath : OCP.TCollection.TCollection_AsciiString,theShape : OCP.TopoDS.TopoDS_Shape,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    @overload
    def Write(self,thePath : OCP.TCollection.TCollection_AsciiString,theDocument : OCP.TDocStd.TDocStd_Document,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    @overload
    def __init__(self,theNode : OCP.DE.DE_ConfigurationNode) -> None: ...
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
class IGESCAFControl_Reader(OCP.IGESControl.IGESControl_Reader, OCP.XSControl.XSControl_Reader):
    """
    Provides a tool to read IGES file and put it into DECAF document. Besides transfer of shapes (including assemblies) provided by IGESControl, supports also colors and part names IGESCAFControl_Reader reader; Methods for translation of an IGES file: reader.ReadFile("filename"); reader.Transfer(Document); or reader.Perform("filename",doc); Methods for managing reading attributes. Colors reader.SetColorMode(colormode); Standard_Boolean colormode = reader.GetColorMode(); Layers reader.SetLayerMode(layermode); Standard_Boolean layermode = reader.GetLayerMode(); Names reader.SetNameMode(namemode); Standard_Boolean namemode = reader.GetNameMode();
    """
    def ClearShapes(self) -> None: 
        """
        Clears the list of shapes that may have accumulated in calls to TransferOne or TransferRoot.C
        """
    def GetColorMode(self) -> bool: 
        """
        None
        """
    def GetLayerMode(self) -> bool: 
        """
        None
        """
    def GetNameMode(self) -> bool: 
        """
        None
        """
    def GetReadVisible(self) -> bool: 
        """
        None

        None
        """
    def GetStatsTransfer(self,list : OCP.TColStd.TColStd_HSequenceOfTransient) -> tuple[int, int, int]: 
        """
        Gives statistics about Transfer
        """
    @overload
    def GiveList(self,first : str='',second : str='') -> OCP.TColStd.TColStd_HSequenceOfTransient: 
        """
        Returns a list of entities from the IGES or STEP file according to the following rules: - if first and second are empty strings, the whole file is selected. - if first is an entity number or label, the entity referred to is selected. - if first is a list of entity numbers/labels separated by commas, the entities referred to are selected, - if first is the name of a selection in the worksession and second is not defined, the list contains the standard output for that selection. - if first is the name of a selection and second is defined, the criterion defined by second is applied to the result of the first selection. A selection is an operator which computes a list of entities from a list given in input according to its type. If no list is specified, the selection computes its list of entities from the whole model. A selection can be: - A predefined selection (xst-transferrable-mode) - A filter based on a signature A Signature is an operator which returns a string from an entity according to its type. For example: - "xst-type" (CDL) - "iges-level" - "step-type". For example, if you wanted to select only the advanced_faces in a STEP file you would use the following code: Example Reader.GiveList("xst-transferrable-roots","step-type(ADVANCED_FACE)"); Warning If the value given to second is incorrect, it will simply be ignored.

        Computes a List of entities from the model as follows <first> being a Selection, <ent> being an entity or a list of entities (as a HSequenceOfTransient) : the standard result of this selection applied to this list if <first> is erroneous, a null handle is returned
        """
    @overload
    def GiveList(self,first : str,ent : OCP.Standard.Standard_Transient) -> OCP.TColStd.TColStd_HSequenceOfTransient: ...
    def IGESModel(self) -> OCP.IGESData.IGESData_IGESModel: 
        """
        Returns the model as a IGESModel. It can then be consulted (header, product)
        """
    def Model(self) -> OCP.Interface.Interface_InterfaceModel: 
        """
        Returns the model. It can then be consulted (header, product)
        """
    def NbRootsForTransfer(self) -> int: 
        """
        Determines the list of root entities from Model which are candidate for a transfer to a Shape (type of entities is PRODUCT) <theReadOnlyVisible> is taken into account to define roots
        """
    def NbShapes(self) -> int: 
        """
        Returns the number of shapes produced by translation.
        """
    def OneShape(self) -> OCP.TopoDS.TopoDS_Shape: 
        """
        Returns all of the results in a single shape which is: - a null shape if there are no results, - a shape if there is one result, - a compound containing the resulting shapes if there are more than one.
        """
    @overload
    def Perform(self,theFileName : OCP.TCollection.TCollection_AsciiString,theDoc : OCP.TDocStd.TDocStd_Document,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        None

        Translate IGES file given by filename into the document Return True if succeeded, and False in case of fail
        """
    @overload
    def Perform(self,theFileName : str,theDoc : OCP.TDocStd.TDocStd_Document,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    @overload
    def PrintCheckLoad(self,failsonly : bool,mode : OCP.IFSelect.IFSelect_PrintCount) -> None: 
        """
        Prints the check list attached to loaded data, on the Standard Trace File (starts at std::cout) All messages or fails only, according to <failsonly> mode = 0 : per entity, prints messages mode = 1 : per message, just gives count of entities per check mode = 2 : also gives entity numbers

        Prints the check list attached to loaded data.
        """
    @overload
    def PrintCheckLoad(self,theStream : io.BytesIO,failsonly : bool,mode : OCP.IFSelect.IFSelect_PrintCount) -> None: ...
    @overload
    def PrintCheckTransfer(self,failsonly : bool,mode : OCP.IFSelect.IFSelect_PrintCount) -> None: 
        """
        Displays check results for the last translation of IGES or STEP entities to Open CASCADE entities. Only fail messages are displayed if failsonly is true. All messages are displayed if failsonly is false. mode determines the contents and the order of the messages according to the terms of the IFSelect_PrintCount enumeration.

        Displays check results for the last translation of IGES or STEP entities to Open CASCADE entities.
        """
    @overload
    def PrintCheckTransfer(self,theStream : io.BytesIO,failsonly : bool,mode : OCP.IFSelect.IFSelect_PrintCount) -> None: ...
    @overload
    def PrintStatsTransfer(self,theStream : io.BytesIO,what : int,mode : int=0) -> None: 
        """
        Displays the statistics for the last translation. what defines the kind of statistics that are displayed as follows: - 0 gives general statistics (number of translated roots, number of warnings, number of fail messages), - 1 gives root results, - 2 gives statistics for all checked entities, - 3 gives the list of translated entities, - 4 gives warning and fail messages, - 5 gives fail messages only. The use of mode depends on the value of what. If what is 0, mode is ignored. If what is 1, 2 or 3, mode defines the following: - 0 lists the numbers of IGES or STEP entities in the respective model - 1 gives the number, identifier, type and result type for each IGES or STEP entity and/or its status (fail, warning, etc.) - 2 gives maximum information for each IGES or STEP entity (i.e. checks) - 3 gives the number of entities per type of IGES or STEP entity - 4 gives the number of IGES or STEP entities per result type and/or status - 5 gives the number of pairs (IGES or STEP or result type and status) - 6 gives the number of pairs (IGES or STEP or result type and status) AND the list of entity numbers in the IGES or STEP model. If what is 4 or 5, mode defines the warning and fail messages as follows: - if mode is 0 all warnings and checks per entity are returned - if mode is 2 the list of entities per warning is returned. If mode is not set, only the list of all entities per warning is given.

        Displays the statistics for the last translation.
        """
    @overload
    def PrintStatsTransfer(self,what : int,mode : int=0) -> None: ...
    def PrintTransferInfo(self,failwarn : OCP.IFSelect.IFSelect_PrintFail,mode : OCP.IFSelect.IFSelect_PrintCount) -> None: 
        """
        Prints Statistics and check list for Transfer
        """
    def ReadFile(self,filename : str) -> OCP.IFSelect.IFSelect_ReturnStatus: 
        """
        Loads a file and returns the read status Zero for a Model which compies with the Controller
        """
    def ReadStream(self,theName : str,theIStream : io.BytesIO) -> OCP.IFSelect.IFSelect_ReturnStatus: 
        """
        Loads a file from stream and returns the read status
        """
    def RootForTransfer(self,num : int=1) -> OCP.Standard.Standard_Transient: 
        """
        Returns an IGES or STEP root entity for translation. The entity is identified by its rank in a list.
        """
    def SetColorMode(self,theMode : bool) -> None: 
        """
        Set ColorMode for indicate read Colors or not.
        """
    def SetLayerMode(self,theMode : bool) -> None: 
        """
        Set LayerMode for indicate read Layers or not.
        """
    def SetNameMode(self,theMode : bool) -> None: 
        """
        Set NameMode for indicate read Name or not.
        """
    def SetNorm(self,norm : str) -> bool: 
        """
        Sets a specific norm to <me> Returns True if done, False if <norm> is not available
        """
    def SetReadVisible(self,ReadRoot : bool) -> None: 
        """
        Set the transion of ALL Roots (if theReadOnlyVisible is False) or of Visible Roots (if theReadOnlyVisible is True)

        Set the transion of ALL Roots (if theReadOnlyVisible is False) or of Visible Roots (if theReadOnlyVisible is True)
        """
    def SetWS(self,WS : OCP.XSControl.XSControl_WorkSession,scratch : bool=True) -> None: 
        """
        Sets a specific session to <me>
        """
    def Shape(self,num : int=1) -> OCP.TopoDS.TopoDS_Shape: 
        """
        Returns the shape resulting from a translation and identified by the rank num. num equals 1 by default. In other words, the first shape resulting from the translation is returned.
        """
    def Transfer(self,theDoc : OCP.TDocStd.TDocStd_Document,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Translates currently loaded IGES file into the document Returns True if succeeded, and False in case of fail
        """
    def TransferEntity(self,start : OCP.Standard.Standard_Transient,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Translates an IGES or STEP entity in the model. true is returned if a shape is produced; otherwise, false is returned.
        """
    def TransferList(self,list : OCP.TColStd.TColStd_HSequenceOfTransient,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> int: 
        """
        Translates a list of entities. Returns the number of IGES or STEP entities that were successfully translated. The list can be produced with GiveList. Warning - This function does not clear the existing output shapes.
        """
    def TransferOne(self,num : int,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Translates an IGES or STEP entity identified by the rank num in the model. false is returned if no shape is produced.
        """
    def TransferOneRoot(self,num : int=1,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Translates a root identified by the rank num in the model. false is returned if no shape is produced.
        """
    def TransferRoots(self,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> int: 
        """
        Translates all translatable roots and returns the number of successful translations. Warning - This function clears existing output shapes first.
        """
    def WS(self) -> OCP.XSControl.XSControl_WorkSession: 
        """
        Returns the session used in <me>
        """
    @overload
    def __init__(self) -> None: ...
    @overload
    def __init__(self,theWS : OCP.XSControl.XSControl_WorkSession,FromScratch : bool=True) -> None: ...
    pass
class IGESCAFControl_Writer(OCP.IGESControl.IGESControl_Writer):
    """
    Provides a tool to write DECAF document to the IGES file. Besides transfer of shapes (including assemblies) provided by IGESControl, supports also colors and part names IGESCAFControl_Writer writer(); Methods for writing IGES file: writer.Transfer (Document); writer.Write("filename") or writer.Write(OStream) or writer.Perform(Document,"filename"); Methods for managing the writing of attributes. Colors writer.SetColorMode(colormode); Standard_Boolean colormode = writer.GetColorMode(); Layers writer.SetLayerMode(layermode); Standard_Boolean layermode = writer.GetLayerMode(); Names writer.SetNameMode(namemode); Standard_Boolean namemode = writer.GetNameMode();
    """
    def AddEntity(self,ent : OCP.IGESData.IGESData_IGESEntity) -> bool: 
        """
        Adds an IGES entity (and the ones it references) to the model
        """
    def AddGeom(self,geom : OCP.Standard.Standard_Transient) -> bool: 
        """
        Translates a Geometry (Surface or Curve) to IGES Entities and adds them to the model Returns True if done, False if geom is neither a Surface or a Curve suitable for IGES or is null
        """
    def AddShape(self,sh : OCP.TopoDS.TopoDS_Shape,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Translates a Shape to IGES Entities and adds them to the model Returns True if done, False if Shape not suitable for IGES or null
        """
    def ComputeModel(self) -> None: 
        """
        Computes the entities found in the model, which is ready to be written. This contrasts with the default computation of headers only.
        """
    def GetColorMode(self) -> bool: 
        """
        None
        """
    def GetLayerMode(self) -> bool: 
        """
        None
        """
    def GetNameMode(self) -> bool: 
        """
        None
        """
    def Model(self) -> OCP.IGESData.IGESData_IGESModel: 
        """
        Returns the IGES model to be written in output.
        """
    @overload
    def Perform(self,doc : OCP.TDocStd.TDocStd_Document,filename : OCP.TCollection.TCollection_AsciiString,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        None

        Transfers a document and writes it to a IGES file Returns True if translation is OK
        """
    @overload
    def Perform(self,doc : OCP.TDocStd.TDocStd_Document,filename : str,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    def SetColorMode(self,colormode : bool) -> None: 
        """
        Set ColorMode for indicate write Colors or not.
        """
    def SetLayerMode(self,layermode : bool) -> None: 
        """
        Set LayerMode for indicate write Layers or not.
        """
    def SetNameMode(self,namemode : bool) -> None: 
        """
        Set NameMode for indicate write Name or not.
        """
    def SetTransferProcess(self,TP : OCP.Transfer.Transfer_FinderProcess) -> None: 
        """
        Returns/Sets the TransferProcess : it contains final results and if some, check messages
        """
    @overload
    def Transfer(self,labels : OCP.TDF.TDF_LabelSequence,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: 
        """
        Transfers a document to a IGES model Returns True if translation is OK

        Transfers labels to a IGES model Returns True if translation is OK

        Transfers label to a IGES model Returns True if translation is OK
        """
    @overload
    def Transfer(self,doc : OCP.TDocStd.TDocStd_Document,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    @overload
    def Transfer(self,label : OCP.TDF.TDF_Label,theProgress : OCP.Message.Message_ProgressRange=OCP.Message.Message_ProgressRange) -> bool: ...
    def TransferProcess(self) -> OCP.Transfer.Transfer_FinderProcess: 
        """
        None
        """
    @overload
    def Write(self,file : str,fnes : bool=False) -> bool: 
        """
        Computes then writes the model to an OStream Returns True when done, false in case of error

        Prepares and writes an IGES model either to an OStream, S or to a file name,CString. Returns True if the operation was performed correctly and False if an error occurred (for instance, if the processor could not create the file).
        """
    @overload
    def Write(self,S : io.BytesIO,fnes : bool=False) -> bool: ...
    @overload
    def __init__(self,WS : OCP.XSControl.XSControl_WorkSession,scratch : bool=True) -> None: ...
    @overload
    def __init__(self) -> None: ...
    pass
