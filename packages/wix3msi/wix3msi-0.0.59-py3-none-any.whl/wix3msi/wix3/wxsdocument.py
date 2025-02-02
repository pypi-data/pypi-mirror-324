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


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"


#--------------------------------------------------------------------------------
# WindowsInstaller XML Schema 문서.
#--------------------------------------------------------------------------------
class WXSDocument:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__document: Document


	#--------------------------------------------------------------------------------
	# 문서 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Document(thisInstance) -> Document:
		return thisInstance.__document
	

	#--------------------------------------------------------------------------------
	# 네임스페이스 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Namespaces(thisInstance) -> Dict[str, str]:
		return thisInstance.__namespaces


	#--------------------------------------------------------------------------------
	# WXS XML 루트 요소 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def RootElement(thisInstance) -> Element:
		element = Element.Create(thisInstance.Document.RootXMLElement)
		return element


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, document: Document = None) -> None:
		thisInstance.__document = document
		thisInstance.__namespaces = dict()
		thisInstance.__namespaces["wix"] = "http://schemas.microsoft.com/wix/2006/wi"


	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	def LoadFromWXSFile(thisInstance, wxsFilePath: str) -> bool:
		if not thisInstance.__document.LoadFromXMLFile(wxsFilePath):
			return False
		return True


	#--------------------------------------------------------------------------------
	# 저장하기.
	#--------------------------------------------------------------------------------
	def SaveToWXSFile(thisInstance, wxsFilePath: str) -> bool:
		xmlString: str = thisInstance.Document.SaveToString()
		with builtins.open(wxsFilePath, FILE_WRITETEXT, encoding = UTF8) as outputFile:
			outputFile.write(xmlString)


	#--------------------------------------------------------------------------------
	# 생성.
	#--------------------------------------------------------------------------------
	@staticmethod
	def Create() -> WXSDocument:
		wix: Element = Element.Create("Wix")
		document: Document = Document.Create(wix)
		wxsDocument: WXSDocument = WXSDocument(document)
		return wxsDocument
	

	#--------------------------------------------------------------------------------
	# 불러오기.
	#--------------------------------------------------------------------------------
	@staticmethod
	def CreateFromWXSFile(wxsFilePath: str) -> WXSDocument:
		wxsDocument = WXSDocument.Create()
		if not wxsDocument.LoadFromWXSFile(wxsFilePath):
			raise Exception()
		return wxsDocument


	#--------------------------------------------------------------------------------
	# 프로덕트 설정.
	#--------------------------------------------------------------------------------
	def SetProduct(thisInstance, product: Product) -> None:
		# productElement: Element = thisInstance.RootElement.Find(".//wix:Product", thisInstance.Namespaces)
		productElement: Element = thisInstance.RootElement.Find(".//wix:Product", thisInstance.Namespaces)
		if productElement:
			productElement.AddOrSetAttribute("Id", product.Id)
			productElement.AddOrSetAttribute("Name", product.Name)
			productElement.AddOrSetAttribute("Manufacturer", product.Manufacturer)
			productElement.AddOrSetAttribute("UpgradeCode", product.UpgradeCode)
			productElement.AddOrSetAttribute("Version", product.Version)
			productElement.AddOrSetAttribute("Language", product.Language)
		else:
			raise Exception("[wix3msi] Not found Product")