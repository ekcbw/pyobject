"""A multifunctional all-in-one utility tool for managing internal Python \
objects, compatible with nearly all Python 3 versions.
一个多功能合一的提供操作Python对象底层工具的Python包, 支持几乎所有Python 3版本。
"""
import sys, types
from warnings import warn
from pprint import pprint
from inspect import isfunction,ismethod
try:
    from types import WrapperDescriptorType,MethodWrapperType,\
                      MethodDescriptorType,ClassMethodDescriptorType
except ImportError: # 低于3.7的版本
    from typing import WrapperDescriptorType,MethodWrapperType,\
                       MethodDescriptorType
    ClassMethodDescriptorType = type(dict.__dict__['fromkeys'])

__version__="1.3.3"

__all__=["objectname","bases","describe","desc"]
_always_ignored_names=["__builtins__","__doc__"]

MAXLENGTH=150

def isfunc(obj):
    # 判断一个对象是否为函数或方法
    if isfunction(obj) or ismethod(obj):return True
    # 使用typing而不用types.WrapperDescriptorType是为了与旧版本兼容
    func_types=[types.LambdaType,types.BuiltinFunctionType,
                types.BuiltinMethodType,WrapperDescriptorType,
                MethodWrapperType,MethodDescriptorType,
                ClassMethodDescriptorType]
    for type_ in func_types:
        if isinstance(obj,type_):
            return True
    return False

def objectname(obj):
    # 返回对象的全名，类似__qualname__属性
    # if hasattr(obj,"__qualname__"):return obj.__qualname__
    if not obj.__class__==type:obj=obj.__class__
    if not hasattr(obj,"__module__") or obj.__module__=="__main__":
        return obj.__name__
    return "{}.{}".format(obj.__module__,obj.__name__)

def bases(obj,level=0,tab=4):
    # 打印对象的基类
    if not obj.__class__==type:obj=obj.__class__
    if obj.__bases__:
        if level:print(' '*(level*tab),end='')
        print(*obj.__bases__,sep=',')
        for cls in obj.__bases__:
            bases(cls,level,tab)

_trans_table=str.maketrans("\n\t","  ") # 替换特殊字符为空格
def shortrepr(obj,maxlength=None,repr_func=None):
    if repr_func is None:repr_func = repr
    if maxlength is None:maxlength = MAXLENGTH
    result=repr_func(obj).translate(_trans_table)
    if len(result)>maxlength:
        return result[:maxlength]+"..."
    return result

def describe(obj,level=0,maxlevel=1,tab=4,verbose=False,file=None,
             maxlength=None,ignore_funcs=False):
    '''"Describe" an object by printing its attributes.
Parameters:
maxlevel: The number of levels to print the object's attributes.
tab: The number of spaces for indentation, default is 4.
verbose: Whether to output attributes starting with "_" (e.g., __init__).
maxlength: The maximum output length of one object.
ignore_funcs: If set to True, methods or functions of the object will not be output.
file: A file-like object for printing output.
'''
    if file is None:file=sys.stdout
    if level==maxlevel:
        result=repr(obj)
        if result.startswith('[') or result.startswith('{'):pprint(result)
        else:print(result,file=file)
    elif level>maxlevel:
        raise ValueError("Argument level is larger than maxlevel")
    else:
        print(shortrepr(obj,maxlength)+': ',file=file)
        if type(obj) is type:
            print("Base classes of the object:",file=file)
            bases(obj,level+1,tab)
            print(file=file)
        for attr in dir(obj):
            if verbose or not attr.startswith("_"):
                print(' '*tab*(level+1),end='',file=file)
                try:
                    value = getattr(obj,attr)
                    if ignore_funcs and isfunc(value):
                        continue
                    print(f"{attr}: ",file=file)
                    if attr in _always_ignored_names:
                        describe(value,level+1,maxlevel,tab,verbose,file,maxlength)
                    else:
                        print(shortrepr(value,maxlength),file=file)
                except AttributeError:
                    print(f"{attr}: <AttributeError!>",file=file)
        if isinstance(obj, list):
            print("\nList items of the object:",file=file)
            for i,item in enumerate(obj):
                print(f"{' '*tab*(level+1)}{i}: ",end='',file=file)
                describe(item,level+1,maxlevel,tab,verbose,file,maxlength)
        if isinstance(obj, dict):
            print("\nDictionary items of the object:",file=file)
            for key in obj.keys():
                print(f"{' '*tab*(level+1)}{key!r}: ",end='',file=file)
                try:
                    describe(obj[key],level+1,maxlevel,tab,verbose,file,maxlength)
                except KeyError:
                    print("<KeyError!>",file=file)

desc = describe #别名

# 导入其他子模块中的函数和类
try:
    from pyobject.browser import browse
    __all__.append("browse")
except ImportError:warn("Failed to import module pyobject.browser.")
try:
    from pyobject.search import make_list,make_iter,search
    __all__.extend(["make_list","make_iter","search"])
except ImportError:warn("Failed to import pyobject.search.")

try:
    from pyobject.code import Code
    __all__.append("Code")
except ImportError:warn("Failed to import pyobject.code.")
try:
    from pyobject.pyobj_extension import *
    __all__.extend(["convptr","py_incref","py_decref","getrealrefcount",
                    "setrefcount","list_in","getrefcount_nogil","setrefcount_nogil",
                    "get_type_flag","set_type_flag","set_type_base","set_type_bases",
                    "set_type_mro","get_type_subclasses","set_type_subclasses",
                    "set_type_subclasses_by_cls"])
except ImportError:warn("Failed to import pyobject.pyobj_extension.")
try:
    from pyobject.objproxy import ObjChain,ProxiedObj,unproxy_obj
    __all__.extend(["ObjChain","ProxiedObj","unproxy_obj"])
except ImportError as err:
    warn("Failed to import pyobject.objproxy (%s): %s"%(type(err).__name__,err))

if __name__=="__main__":
    describe(type,verbose=True)
