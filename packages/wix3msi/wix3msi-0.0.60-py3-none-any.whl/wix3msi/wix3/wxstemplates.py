#--------------------------------------------------------------------------------
# 참조 모듈 목록.
#--------------------------------------------------------------------------------
from __future__ import annotations
from typing import Awaitable, Callable, Final, Generic, Iterable, Iterator, Optional, Sequence, Type, TypeVar, Tuple, Union
from typing import ItemsView, KeysView, ValuesView
from typing import IO, TextIO, BinaryIO
from typing import Any, List, Dict, Set
from typing import cast, overload
import builtins
import re
from .schema import Product
from xpl import Document, Element
from .wxsdocument import WXSDocument


#--------------------------------------------------------------------------------
# WXS 간단 셋팅 템플릿.
#--------------------------------------------------------------------------------
class WXSTemplates:
	#--------------------------------------------------------------------------------
	# 최소 템플릿 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Minimal() -> WXSDocument:
		wix: Element = Element.CreateFromValue("Wix")
		product: Element = Element.CreateFromValue("Product")
		wix.AddChild(product)
		package: Element = Element.CreateFromValue("Package")
		product.AddChild(package)
		property: Element = Element.CreateFromValue("Property", { "Id": "WIXUI_INSTALLDIR", "Value": "DefaultInstallDirectory" })
		product.AddChild(property)
		mediaTemplate: Element = Element.CreateFromValue("MediaTemplate", { "EmbedCab": "yes" })
		product.AddChild(mediaTemplate)
		feature: Element = Element.CreateFromValue("Feauture", { "Id": "DefaultComponentGroup" })
		product.AddChild(feature)
		componentGroupRef: Element = Element.CreateFromValue("ComponentGroupRef", { "Id": "DefaultComponentGroup" })
		feature.AddChild(componentGroupRef)
		wixVariable: Element = Element.CreateFromValue("WixVariable", { "Id": "WixUILicenseRtf", "Value": "" })
		product.AddChild(wixVariable)
		ui: Element = Element.CreateFromValue("UI")
		product.AddChild(ui)
		uiRef: Element = Element.CreateFromValue("UIRef", { "Id": "WixUI_InstallDir" })
		ui.AddChild(uiRef)
		fragment: Element = Element.CreateFromValue("Fragment")
		wix.AddChild(fragment)
		directroy: Element = Element.CreateFromValue("Directory", { "Id": "TARGETDIR", "Name": "SourceDir" })
		fragment.AddChild(directroy)
		componentGroup = Element.CreateFromValue("ComponentGroup", { "Id": "DefaultComponentGroup" })
		fragment.AddChild(componentGroup)

		document: Document = Document.CreateFromXMLElement(wix)
		wxsDocument: WXSDocument = WXSDocument(document)
		return wxsDocument
	

	#--------------------------------------------------------------------------------
	# 기본 템플릿 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Default() -> WXSDocument:
		wix: Element = Element.CreateFromValue("Wix")
		product: Element = Element.CreateFromValue("Product")
		wix.AddChild(product)
		package: Element = Element.CreateFromValue("Package")
		product.AddChild(package)
		property: Element = Element.CreateFromValue("Property", { "Id": "WIXUI_INSTALLDIR", "Value": "DefaultInstallDirectory" })
		product.AddChild(property)
		mediaTemplate: Element = Element.CreateFromValue("MediaTemplate", { "EmbedCab": "yes" })
		product.AddChild(mediaTemplate)
		feature: Element = Element.CreateFromValue("Feauture", { "Id": "DefaultComponentGroup" })
		product.AddChild(feature)
		componentGroupRef: Element = Element.CreateFromValue("ComponentGroupRef", { "Id": "DefaultComponentGroup" })
		feature.AddChild(componentGroupRef)
		wixVariable: Element = Element.CreateFromValue("WixVariable", { "Id": "WixUILicenseRtf", "Value": "" })
		product.AddChild(wixVariable)
		ui: Element = Element.CreateFromValue("UI")
		product.AddChild(ui)
		uiRef: Element = Element.CreateFromValue("UIRef", { "Id": "WixUI_InstallDir" })
		ui.AddChild(uiRef)
		fragment: Element = Element.CreateFromValue("Fragment")
		wix.AddChild(fragment)
		directroy: Element = Element.CreateFromValue("Directory", { "Id": "TARGETDIR", "Name": "SourceDir" })
		fragment.AddChild(directroy)
		componentGroup = Element.CreateFromValue("ComponentGroup", { "Id": "DefaultComponentGroup" })
		fragment.AddChild(componentGroup)

		document: Document = Document.CreateFromXMLElement(wix)
		wxsDocument: WXSDocument = WXSDocument(document)
		return wxsDocument