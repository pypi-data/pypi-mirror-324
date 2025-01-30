import OCP.Xw
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
import OCP.Graphic3d
import OCP.Quantity
import OCP.Standard
import OCP.Aspect
import OCP.TCollection
import io
__all__  = [
"Xw_Window",
"__GLXFBConfigRec"
]
class Xw_Window(OCP.Aspect.Aspect_Window, OCP.Standard.Standard_Transient):
    """
    This class defines XLib window intended for creation of OpenGL context.This class defines XLib window intended for creation of OpenGL context.
    """
    def Background(self) -> OCP.Aspect.Aspect_Background: 
        """
        Returns the window background.
        """
    def BackgroundFillMethod(self) -> OCP.Aspect.Aspect_FillMethod: 
        """
        Returns the current image background fill mode.
        """
    def ConvertPointFromBacking(self,thePnt : OCP.Graphic3d.Graphic3d_Vec2d) -> OCP.Graphic3d.Graphic3d_Vec2d: 
        """
        Convert point from backing store units to logical units.
        """
    def ConvertPointToBacking(self,thePnt : OCP.Graphic3d.Graphic3d_Vec2d) -> OCP.Graphic3d.Graphic3d_Vec2d: 
        """
        Convert point from logical units into backing store units.
        """
    def DecrementRefCounter(self) -> int: 
        """
        Decrements the reference counter of this object; returns the decremented value
        """
    def Delete(self) -> None: 
        """
        Memory deallocator for transient classes
        """
    def DevicePixelRatio(self) -> float: 
        """
        Return device pixel ratio (logical to backing store scale factor).
        """
    def Dimensions(self) -> OCP.Graphic3d.Graphic3d_Vec2i: 
        """
        Returns window dimensions.
        """
    def DisplayConnection(self) -> OCP.Aspect.Aspect_DisplayConnection: 
        """
        Returns connection to Display or NULL.
        """
    def DoMapping(self) -> bool: 
        """
        Apply the mapping change to the window <me>
        """
    def DoResize(self) -> OCP.Aspect.Aspect_TypeOfResize: 
        """
        Applies the resizing to the window <me>
        """
    def DumpJson(self,theOStream : io.BytesIO,theDepth : int=-1) -> None: 
        """
        Dumps the content of me into the stream
        """
    def DynamicType(self) -> OCP.Standard.Standard_Type: 
        """
        None
        """
    def GetRefCount(self) -> int: 
        """
        Get the reference counter of this object
        """
    def GradientBackground(self) -> OCP.Aspect.Aspect_GradientBackground: 
        """
        Returns the window gradient background.
        """
    def IncrementRefCounter(self) -> None: 
        """
        Increments the reference counter of this object
        """
    def InvalidateContent(self,theDisp : OCP.Aspect.Aspect_DisplayConnection) -> None: 
        """
        Invalidate entire window content through generation of Expose event. This method does not aggregate multiple calls into single event - dedicated event will be sent on each call. When NULL display connection is specified, the connection specified on window creation will be used. Sending exposure messages from non-window thread would require dedicated display connection opened specifically for this working thread to avoid race conditions, since Xlib display connection is not thread-safe by default.
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
    def IsMapped(self) -> bool: 
        """
        Returns True if the window <me> is opened
        """
    def IsVirtual(self) -> bool: 
        """
        Returns True if the window <me> is virtual
        """
    def Map(self) -> None: 
        """
        Opens the window <me>
        """
    def NativeFBConfig(self) -> __GLXFBConfigRec: 
        """
        Returns native Window FB config (GLXFBConfig on Xlib)
        """
    def NativeHandle(self) -> int: 
        """
        Returns native Window handle
        """
    def NativeParentHandle(self) -> int: 
        """
        Returns parent of native Window handle
        """
    def Position(self) -> tuple[int, int, int, int]: 
        """
        Returns The Window POSITION in PIXEL
        """
    def ProcessMessage(self,theListener : OCP.Aspect.Aspect_WindowInputListener,theMsg : _XEvent) -> bool: 
        """
        Process a single window message.
        """
    def Ratio(self) -> float: 
        """
        Returns The Window RATIO equal to the physical WIDTH/HEIGHT dimensions
        """
    @overload
    def SetBackground(self,theFirstColor : OCP.Quantity.Quantity_Color,theSecondColor : OCP.Quantity.Quantity_Color,theFillMethod : OCP.Aspect.Aspect_GradientFillMethod) -> None: 
        """
        Modifies the window background.

        Modifies the window background.

        Modifies the window gradient background.

        Modifies the window gradient background.
        """
    @overload
    def SetBackground(self,theColor : OCP.Quantity.Quantity_Color) -> None: ...
    @overload
    def SetBackground(self,theBack : OCP.Aspect.Aspect_Background) -> None: ...
    @overload
    def SetBackground(self,theBackground : OCP.Aspect.Aspect_GradientBackground) -> None: ...
    def SetTitle(self,theTitle : OCP.TCollection.TCollection_AsciiString) -> None: 
        """
        Sets window title.
        """
    def SetVirtual(self,theVirtual : bool) -> None: 
        """
        Setup the virtual state
        """
    def Size(self) -> tuple[int, int]: 
        """
        Returns The Window SIZE in PIXEL
        """
    def This(self) -> OCP.Standard.Standard_Transient: 
        """
        Returns non-const pointer to this object (like const_cast). For protection against creating handle to objects allocated in stack or call from constructor, it will raise exception Standard_ProgramError if reference counter is zero.
        """
    def TopLeft(self) -> OCP.Graphic3d.Graphic3d_Vec2i: 
        """
        Returns window top-left corner.
        """
    def Unmap(self) -> None: 
        """
        Closes the window <me>
        """
    @staticmethod
    def VirtualKeyFromNative_s(theKey : int) -> int: 
        """
        Convert X11 virtual key (KeySym) into Aspect_VKey.
        """
    def XWindow(self) -> int: 
        """
        Returns native Window handle
        """
    @overload
    def __init__(self,theXDisplay : OCP.Aspect.Aspect_DisplayConnection,theTitle : str,thePxLeft : int,thePxTop : int,thePxWidth : int,thePxHeight : int) -> None: ...
    @overload
    def __init__(self,theXDisplay : OCP.Aspect.Aspect_DisplayConnection,theXWin : int,theFBConfig : __GLXFBConfigRec=None) -> None: ...
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
class __GLXFBConfigRec():
    pass
