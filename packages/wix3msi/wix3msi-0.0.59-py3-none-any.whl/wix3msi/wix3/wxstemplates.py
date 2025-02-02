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
		wix: Element = Element.Create("Wix")
		product: Element = Element.Create("Product")
		wix.AddChild(product)
		package: Element = Element.Create("Package")
		product.AddChild(package)
		property: Element = Element.Create("Property", { "Id": "WIXUI_INSTALLDIR", "Value": "DefaultInstallDirectory" })
		product.AddChild(property)
		mediaTemplate: Element = Element.Create("MediaTemplate", { "EmbedCab": "yes" })
		product.AddChild(mediaTemplate)
		feature: Element = Element.Create("Feauture", { "Id": "DefaultComponentGroup" })
		product.AddChild(feature)
		componentGroupRef: Element = Element.Create("ComponentGroupRef", { "Id": "DefaultComponentGroup" })
		feature.AddChild(componentGroupRef)
		wixVariable: Element = Element.Create("WixVariable", { "Id": "WixUILicenseRtf", "Value": "" })
		product.AddChild(wixVariable)
		ui: Element = Element.Create("UI")
		product.AddChild(ui)
		uiRef: Element = Element.Create("UIRef", { "Id": "WixUI_InstallDir" })
		ui.AddChild(uiRef)
		fragment: Element = Element.Create("Fragment")
		wix.AddChild(fragment)
		directroy: Element = Element.Create("Directory", { "Id": "TARGETDIR", "Name": "SourceDir" })
		fragment.AddChild(directroy)
		componentGroup = Element.Create("ComponentGroup", { "Id": "DefaultComponentGroup" })
		fragment.AddChild(componentGroup)

		document: Document = Document.Create(wix)
		wxsDocument: WXSDocument = WXSDocument(document)
		return wxsDocument
	

	#--------------------------------------------------------------------------------
	# 기본 템플릿 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Default() -> WXSDocument:
		wix: Element = Element.Create("Wix")
		product: Element = Element.Create("Product")
		wix.AddChild(product)
		package: Element = Element.Create("Package")
		product.AddChild(package)
		property: Element = Element.Create("Property", { "Id": "WIXUI_INSTALLDIR", "Value": "DefaultInstallDirectory" })
		product.AddChild(property)
		mediaTemplate: Element = Element.Create("MediaTemplate", { "EmbedCab": "yes" })
		product.AddChild(mediaTemplate)
		feature: Element = Element.Create("Feauture", { "Id": "DefaultComponentGroup" })
		product.AddChild(feature)
		componentGroupRef: Element = Element.Create("ComponentGroupRef", { "Id": "DefaultComponentGroup" })
		feature.AddChild(componentGroupRef)
		wixVariable: Element = Element.Create("WixVariable", { "Id": "WixUILicenseRtf", "Value": "" })
		product.AddChild(wixVariable)
		ui: Element = Element.Create("UI")
		product.AddChild(ui)
		uiRef: Element = Element.Create("UIRef", { "Id": "WixUI_InstallDir" })
		ui.AddChild(uiRef)
		fragment: Element = Element.Create("Fragment")
		wix.AddChild(fragment)
		directroy: Element = Element.Create("Directory", { "Id": "TARGETDIR", "Name": "SourceDir" })
		fragment.AddChild(directroy)
		componentGroup = Element.Create("ComponentGroup", { "Id": "DefaultComponentGroup" })
		fragment.AddChild(componentGroup)

		document: Document = Document.Create(wix)
		wxsDocument: WXSDocument = WXSDocument(document)
		return wxsDocument