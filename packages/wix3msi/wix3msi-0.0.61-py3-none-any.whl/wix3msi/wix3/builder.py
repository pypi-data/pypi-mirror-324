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
from enum import Enum
import os
import re
import uuid
from ..filesystem import Node, DirectoryNode, FileNode, NodeManager
from .languagecode import LanguageCode


#--------------------------------------------------------------------------------
# 전역 상수 목록.
#--------------------------------------------------------------------------------
FILE_READTEXT: str = "rt"
FILE_WRITETEXT: str = "wt"
UTF8: str = "utf-8"
WIX: str = "wix"
WIX_NAMESPACE: str = "http://schemas.microsoft.com/wix/2006/wi"
EMPTY: str = ""
RE_REMOVE_NS0: str = "(ns0:|ns0|:ns0)"
LINEFEED: str = "\n"

DEFAULT_NAME: str = "Default Name"
DEFAULT_MANUFACTURER: str = "Default Manufacturer"
DEFAULT_GUID: str = "{A1B2C3D4-5E6F-G7H8-IJKL-1M2N3O4P5Q6R}"
DEFAULT_VERSION: str = "0.0.0"


#--------------------------------------------------------------------------------
# 기본 빌드 프로세스.
#--------------------------------------------------------------------------------
class Builder:
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__productCode: str
	__productVersion: str
	__productName: str
	__productManufacturer: str
	__productLanguague: LanguageCode


	#--------------------------------------------------------------------------------
	# 설치파일 코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductCode(thisInstance) -> str:
		return thisInstance.__productCode


	#--------------------------------------------------------------------------------
	# 설치파일 코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductCode.setter
	def ProductCode(thisInstance, value: str) -> None:
		thisInstance.__productCode = value


	#--------------------------------------------------------------------------------
	# 설치파일 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductVersion(thisInstance) -> str:
		return thisInstance.__productVersion


	#--------------------------------------------------------------------------------
	# 설치파일 버전 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductVersion.setter
	def ProductVersion(thisInstance, value: str) -> None:
		thisInstance.__productVersion = value


	#--------------------------------------------------------------------------------
	# 설치파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductName(thisInstance) -> str:
		return thisInstance.__productName


	#--------------------------------------------------------------------------------
	# 설치파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductName.setter
	def ProductName(thisInstance, value: str) -> None:
		thisInstance.__productName = value


	#--------------------------------------------------------------------------------
	# 설치파일 제조업체 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductManufacturer(thisInstance) -> str:
		return thisInstance.__productManufacturer


	#--------------------------------------------------------------------------------
	# 설치파일 제조업체 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductManufacturer.setter
	def ProductManufacturer(thisInstance, value: str) -> None:
		thisInstance.__productManufacturer = value


	#--------------------------------------------------------------------------------
	# 설치파일 언어코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def ProductLaunguage(thisInstance) -> LanguageCode:
		return thisInstance.__productLanguague


	#--------------------------------------------------------------------------------
	# 설치파일 언어코드 프로퍼티.
	#--------------------------------------------------------------------------------
	@ProductLaunguage.setter
	def ProductLaunguage(thisInstance, value: LanguageCode) -> None:
		thisInstance.__productLanguague = value


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance) -> None:
		thisInstance.__productCode = DEFAULT_GUID
		thisInstance.__productVersion = DEFAULT_VERSION
		thisInstance.__productName = "ProductName"
		thisInstance.__productManufacturer = "ProductManufacturer"
		thisInstance.__productLanguague: LanguageCode = LanguageCode.ENGLISH