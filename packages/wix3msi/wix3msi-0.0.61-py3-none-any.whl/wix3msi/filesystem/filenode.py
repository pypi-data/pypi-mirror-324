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
import os
from xpl import Path as XPLPath
from .node import Node
from .nodetype import NodeType


#--------------------------------------------------------------------------------
# 파일 노드.
#--------------------------------------------------------------------------------
class FileNode(Node):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__path: str # 대상 이름을 제외한 경로.
	__name: str # 대상 파일 이름.
	__extension: str # 대상 파일 확장자.


	#--------------------------------------------------------------------------------
	# 이름 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Name(thisInstance) -> str:
		return thisInstance.__name


	#--------------------------------------------------------------------------------
	# 노드 타입 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def NodeType(thisInstance) -> NodeType:
		return NodeType.FILE
	
	
	#--------------------------------------------------------------------------------
	# 현재 파일 이름을 제외한 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Path(thisInstance) -> str:
		return thisInstance.__path


	#--------------------------------------------------------------------------------
	# 생성시 입력받았던 파일 전체 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Value(thisInstance) -> str:
		return os.path.join(thisInstance.Path, thisInstance.FileName)


	#--------------------------------------------------------------------------------
	# 파일 이름 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def FileName(thisInstance) -> str:
		return f"{thisInstance.Name}{thisInstance.Extension}"


	#--------------------------------------------------------------------------------
	# 확장자 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Extension(thisInstance) -> str:
		return thisInstance.__extension


	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance, targetPath: str) -> None:
		from .nodemanager import NodeManager
		if not NodeManager.ExistsFile(targetPath):
			raise FileNotFoundError(targetPath)
		
		path, name, extension = XPLPath.GetPathNameExtensionFromFileFullPath(targetPath)
		thisInstance.__path: str = path
		thisInstance.__name: str = name		
		thisInstance.__extension: str = extension


	#--------------------------------------------------------------------------------
	# 파괴됨. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 갱신됨. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	def OnDirty(thisInstance) -> None:
		pass


	#--------------------------------------------------------------------------------
	# 캐시 갱신. (오버라이드)
	#--------------------------------------------------------------------------------
	def Dirty(thisInstance) -> None:
		base = super()
		if not base.IsDirty():
			return		
		base.Dirty()