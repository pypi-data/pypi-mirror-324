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
from .nodemetaclass import NodeMetaClass
from .nodetype import NodeType


#--------------------------------------------------------------------------------
# 인터페이스.
#--------------------------------------------------------------------------------
class Node(metaclass = NodeMetaClass):
	#--------------------------------------------------------------------------------
	# 멤버 변수 목록.
	#--------------------------------------------------------------------------------
	__parent: Node
	__isDirty: bool

	def __instancecheck__(thisInstance, instance):
		import inspect
		stack = [frame.function for frame in inspect.stack()]
		if stack.count("__instancecheck__") > 1:
			raise RuntimeError("Recursive __instancecheck__ detected!")
		return hasattr(instance, "some_method")


	#--------------------------------------------------------------------------------
	# 생성 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __new__(thisClassType, *argumentList, **argumentDictionary) -> Any:
		if thisClassType is Node:
			raise TypeError("Node Instantiate Failed. (Node is Interface)")
		if not argumentDictionary.get("_from_manager", False):
			raise ValueError("Node Instantiate Failed. (Try to NodeManager)")
		base = super()
		return base.__new__(thisClassType)


	#--------------------------------------------------------------------------------
	# 생성됨 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __init__(thisInstance, targetPath: str) -> None:
		thisInstance.__parent = None
		thisInstance.__isDirty = False


	#--------------------------------------------------------------------------------
	# 동일 여부 비교 오퍼레이터.
	#--------------------------------------------------------------------------------
	def __eq__(thisInstance, targetPath: Union[Node, str]) -> bool:
		from .nodemanager import NodeManager
		return NodeManager.Equals(thisInstance, targetPath)


	# #--------------------------------------------------------------------------------
	# # 문자열 변환 오퍼레이터.
	# #--------------------------------------------------------------------------------
	# def __str__(thisInstance) -> str:
	# 	return thisInstance.Value
	

	#--------------------------------------------------------------------------------
	# 부모 디렉토리 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Parent(thisInstance) -> Node:
		if not thisInstance.Path:
			return None
		if thisInstance.__parent:
			return thisInstance.__parent
		
		from .nodemanager import NodeManager
		thisInstance.__parent = NodeManager.Instance.CreateNode(thisInstance.Path)
		return thisInstance.__parent


	#--------------------------------------------------------------------------------
	# 캐시 갱신.
	#--------------------------------------------------------------------------------
	def Dirty(thisInstance) -> None:
		if thisInstance.__isDirty:
			return

		thisInstance.OnDirty()
		thisInstance.__isDirty = True


	#--------------------------------------------------------------------------------
	# 캐시 갱신 여부.
	#--------------------------------------------------------------------------------
	def IsDirty(thisInstance) -> bool:
		return thisInstance.__isDirty


	#--------------------------------------------------------------------------------
	# 파일/디렉토리 이름 프로퍼티. (파일의 경우 확장자 제외)
	#--------------------------------------------------------------------------------
	@property
	def Name(thisInstance) -> str:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 노드 타입 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def NodeType(thisInstance) -> NodeType:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 현재 파일/디렉토리 이름을 제외한 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Path(thisInstance) -> str:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 생성시 입력받았던 파일/디렉토리 전체 경로 프로퍼티.
	#--------------------------------------------------------------------------------
	@property
	def Value(thisInstance) -> str:
		raise NotImplementedError()

	#--------------------------------------------------------------------------------
	# 초기화 라이프사이클 메서드.
	#--------------------------------------------------------------------------------
	def OnCreate(thisInstance, targetPath: str) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 파괴됨.
	#--------------------------------------------------------------------------------
	def OnDestroy(thisInstance) -> None:
		raise NotImplementedError()


	#--------------------------------------------------------------------------------
	# 캐시 갱신됨.
	#--------------------------------------------------------------------------------
	def OnDirty(thisInstance) -> None:
		raise NotImplementedError()