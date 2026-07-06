"Implements the utility for locating the path to a specific object."
import traceback,builtins,sys
from collections import defaultdict
from warnings import warn
try:
    from types import WrapperDescriptorType,MethodWrapperType,\
        MethodDescriptorType,ClassMethodDescriptorType,ModuleType,\
        MappingProxyType
except ImportError: # 低于3.7的版本
    from types import ModuleType
    from typing import WrapperDescriptorType,MethodWrapperType,\
        MethodDescriptorType,MappingProxyType
    ClassMethodDescriptorType = type(dict.__dict__["fromkeys"])

__all__=["make_list","make_iter","search"]
_skip=(WrapperDescriptorType, MethodWrapperType,\
       MethodDescriptorType, ClassMethodDescriptorType) #自动忽略这些类型, 加快速度
DICT_TYPES = [dict, MappingProxyType]
if sys.version_info >= (3, 13): # 3.13+
    FrameLocalsProxy = type((lambda:sys._getframe())().f_locals)
    DICT_TYPES.append(FrameLocalsProxy)
DICT_TYPES = tuple(DICT_TYPES)

# 重写Python的内置函数dir
def dir(obj):
    attrs=builtins.dir(obj)
    # __bases__属性一般不会出现在dir()的返回值中
    if hasattr(obj,"__bases__") and "__bases__" not in attrs:
        attrs.append("__bases__")
    return attrs

def _make_iter(start_obj,recursions,traversed,all=False,show_error=True):
    if id(start_obj) in traversed:return # 已经遍历过
    traversed.add(id(start_obj)) # 将对象标记为已遍历

    if recursions<=0:return
    for attr in dir(start_obj):
        if all or not attr.startswith("__"):
            try:
                obj = getattr(start_obj,attr)
            except Exception:
                if show_error:traceback.print_exc()
                continue
            if id(obj) in traversed:continue
            # 跳过method_wrapper等类型
            # 经测试, 使用obj.__class__比使用type(obj)更快
            if obj.__class__ not in _skip:
                yield obj
                yield from _make_iter(obj,recursions-1,traversed,all,show_error)
    if isinstance(start_obj,(list,tuple)):
        for item in start_obj:
            if id(item) in traversed:continue
            if item.__class__ not in _skip:
                yield item
                yield from _make_iter(item,recursions-1,traversed,all,show_error)
    if isinstance(start_obj, DICT_TYPES):
        for obj in start_obj.keys():
            if id(obj) not in traversed:
                yield obj
        for obj in start_obj.values():
            if id(obj) in traversed:continue
            if obj.__class__ not in _skip:
                yield obj
                yield from _make_iter(obj,recursions-1,traversed,all,show_error)

def make_iter(start_obj,recursions=3,all=False,show_error=True):
    """Create an iterator for an object.
start_obj: The object from which to start the search.
recursions: The maximum recursion depth, with a minimum of 1 level.
all: Whether to include attributes that start with an underscore (e.g., __init__) in the list.
show_error: Whether to output exceptions to sys.stderr when an exception occurs within getattr().\
"""
    traversed=set()
    yield from _make_iter(start_obj,recursions,traversed,all,show_error)

def make_list(start_obj,recursions=3,all=False,show_error=True):
    """Create a list containing a large number of objects.
The functionality and parameters are the same as make_list."""
    return list(make_iter(start_obj,recursions,all,show_error))

def _search(target,start_obj,recursions,traversed,search_str=False,
            verbose=True,show_error=True):
    if recursions<=0:return []
    search_str=search_str and isinstance(target,str) # 如果启用搜索子串，则target必须是字符串
    results=[]
    for attr in dir(start_obj):
        if not verbose and attr.startswith("_"):
            continue
        name="."+attr
        if search_str and target in attr: # 搜索字符串的子串
            results.append(name)

        try:
            obj=getattr(start_obj,attr)
        except AttributeError:continue
        except Exception: # 忽略getattr()返回的AttributeError
            if show_error:
                traceback.print_exc()
            continue

        if target == obj: # ==是为了处理数字、字符串等对象
            results.append(name)
        if obj.__class__ not in _skip: # 如果不忽略
            if traversed.get(id(obj),0)>=recursions:continue
            traversed[id(obj)] = recursions
            result=_search(target,obj,recursions-1,traversed,search_str,
                            verbose,show_error)
            for path in result:
                results.append(name+path)

    if isinstance(start_obj,(list,tuple)): # 进一步搜索列表、元组项
        for i,obj in enumerate(start_obj):
            name="[%d]"%i
            if target == obj:
                results.append(name)
            if obj.__class__ not in _skip:
                if traversed.get(id(obj),0)>=recursions:continue
                traversed[id(obj)] = recursions
                result=_search(target,obj,recursions-1,traversed,search_str,
                               verbose,show_error)
                for path in result:
                    results.append(name+path)

    if isinstance(start_obj,dict): # 进一步搜索字典项
        for key in list(start_obj.keys()): # list：字典大小可能改变
            if (search_str and isinstance(key, str) and target in key) or target == key:
                results.append(" (dictionary key %s)"%repr(key))
            name="[%s]"%repr(key)
            obj=start_obj[key]
            if target == obj:
                results.append(name)
            if obj.__class__ not in _skip:
                if traversed.get(id(obj),0)>=recursions:continue
                traversed[id(obj)] = recursions
                result=_search(target,obj,recursions-1,traversed,search_str,
                               verbose,show_error)
                for path in result:
                    results.append(name+path)

    return results

def search(obj,start,recursions=3,search_str=True,
           verbose=True,show_error=True):
    """Search for an object starting from a given point.
obj: The target object to search for.
start: The starting object from which to begin the search.
recursions: The maximum recursion depth, with a minimum of 1 level.
search_str: Whether to search substrings within strings.
verbose: Whether to search for attributes that start with an underscore, such as __init__.
show_error: Whether to output exceptions to sys.stderr when an exception occurs within getattr().
"""
    name=getattr(start,"__name__","obj") # 也可导入使用objectname函数
    traversed = {}
    results=_search(obj,start,recursions,traversed,
                    search_str,verbose,show_error)
    for i in range(len(results)):
        results[i]=name+results[i]
    return results


def test_search():
    import dis
    print(search(dis,sys,4))

def _format_size(size):
    units = ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]
    base = 1024
    i = 0
    while size >= base and i < len(units) - 1:
        size /= base
        i += 1
    return "{:.2f} {}B".format(size,units[i])

def _iter_module(module, traversed):
    for attr in dir(module):
        obj = getattr(module,attr)
        if isinstance(obj,ModuleType): # 跳过其他的模块
            continue
        yield from _make_iter(obj,1,traversed,all=True,show_error=False)
def test_calc_total_memory():
    lst = []
    traversed = set()
    for mod_name in sorted(list(sys.modules)):
        if mod_name == "sys":continue
        print("Processing %s" % mod_name, end="  ", flush=True)
        lst.extend(_iter_module(sys.modules[mod_name], traversed))
        print("Set length: %d" % (len(traversed)), flush=True)
    total_mem=0
    for obj in lst:
        total_mem+=sys.getsizeof(obj)
    print("Total memory usage of loaded modules: %s" % _format_size(total_mem))

    count = defaultdict(int); types = {}
    for obj in lst:
        cls = type(obj)
        count[id(cls)] += sys.getsizeof(obj)
        types[id(cls)] = cls
    limit = 20
    for i, (id_, size) in enumerate(sorted(
        count.items(), key=lambda item:item[1], reverse=True)):
        print("%s - %r" % (_format_size(size), types[id_]))
        if i >= limit: break

if __name__=="__main__":
    test_search()
    test_calc_total_memory()
