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
from .node import Node
from .nodetype import NodeType


#--------------------------------------------------------------------------------
# 디렉토리 노드.
#--------------------------------------------------------------------------------
class DirectoryNode(Node):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__path: str # 대상 이름을 제외한 경로.
	__name: str # 대상 디렉토리 이름.
	__directories: List[Node] # 자식 디렉토리 목록.
	__files: List[Node] # 자식 파일 목록.


	#--------------------------------------------------------------------------------
	# 디렉토리 이름 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Name(thisInstance) -> str:
		return thisInstance.__name


	#--------------------------------------------------------------------------------
	# 노드 타입 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def NodeType(thisInstance) -> NodeType:
		return NodeType.DIRECTORY
	

	#--------------------------------------------------------------------------------
	# 현재 디렉토리 이름을 제외한 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Path(thisInstance) -> str:
		return thisInstance.__path
	

	#--------------------------------------------------------------------------------
	# 생성시 입력받았던 디렉토리 전체 경로 프로퍼티. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	@property
	def Value(thisInstance) -> str:
		return os.path.join(thisInstance.Path, thisInstance.Name)


	#--------------------------------------------------------------------------------
	# 자식 디렉토리 목록 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Directories(thisInstance) -> List[Node]:
		from .nodemanager import NodeManager
		thisInstance.__directories.clear()
		for directory in os.listdir(thisInstance.Value):
			targetPath: str = os.path.join(thisInstance.Value, directory)
			if not os.path.isdir(targetPath):
				continue
			node: Node = NodeManager.Instance.CreateNode(targetPath)
			if not node:
				continue
			thisInstance.__directories.append(node)
		return thisInstance.__directories


	#--------------------------------------------------------------------------------
	# 자식 파일 목록 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Files(thisInstance) -> List[Node]:
		from .nodemanager import NodeManager
		thisInstance.__files.clear()
		for directory in os.listdir(thisInstance.Value):
			targetPath: str = os.path.join(thisInstance.Value, directory)
			if not os.path.isfile(targetPath):
				continue
			node: Node = NodeManager.Instance.CreateNode(targetPath)
			if not node:
				continue
			thisInstance.__files.append(node)
		return thisInstance.__files
	

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드. (인터페이스 구현)
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance, targetPath: str) -> None:
		from .nodemanager import NodeManager
		if not NodeManager.ExistsDirectory(targetPath):
			raise FileNotFoundError(targetPath)

		thisInstance.__path: str = os.path.dirname(targetPath)
		thisInstance.__name: str = os.path.basename(targetPath)
		thisInstance.__directories = list()
		thisInstance.__files = list()


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