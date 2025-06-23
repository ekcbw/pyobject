pyobject - 一个多功能合一的提供操作Python对象底层工具的Python包, 支持几乎所有Python 3版本。

[[English](README.md) | 中文]

## 子模块

pyobject.\_\_init\_\_ - 显示和输出Python对象的各个属性值

pyobject.browser - 调用tkinter，浏览Python对象的图形界面

pyobject.code - Python 底层字节码(bytecode)的操作工具

pyobject.search - 以一个对象为起点，查找和搜索能到达的所有python对象

pyobject.objproxy - 实现一个通用的对象代理，能够代理任意Python对象，包括模块，函数和类

pyobject.pyobj_extension - C扩展模块, 提供操作Python对象底层的函数

## 包含的函数

**describe(obj, level=0, maxlevel=1, tab=4, verbose=False, file=sys.stdout)**:

以`属性名: 值`格式，打印出对象的各个属性，便于实时调试对象。（别名为`desc()`）  

- maxlevel: 打印对象属性的层数。
- tab: 缩进的空格数，默认为4。
- verbose: 一个布尔值，是否打印出对象的特殊方法（如`__init__`）。
- file: 一个类似文件的对象，用于打印输出。

**browse(object, verbose=False, name='obj')**:

用图形界面浏览任意的Python对象，需要tkinter库。

- verbose: 与describe相同，是否打印出对象的特殊方法（如`__init__`）。

函数browse()的图形界面如下（中文的版本可在包目录内的[other/browser_chs_locale.py](https://github.com/ekcbw/pyobject/blob/main/pyobject/other/browser_chs_locale.py)中找到）：

![browse函数界面图片](https://i-blog.csdnimg.cn/blog_migrate/3d67b32633815a54c8c9d0c370248318.png)

**bases(obj, level=0, tab=4)**:

bases(obj) - 打印出对象的基类，以及继承顺序。

- tab: 缩进的空格数，默认为4。

## 用于对象搜索的函数

**make_list(start_obj, recursions=2, all=False)**:

创建一个对象的列表，列表中无重复的对象。

- start: 开始搜索的对象
- recursion: 递归次数
- all: 是否将对象的特殊属性（如`__init__`）加入列表

**make_iter(start_obj, recursions=2, all=False)**:

功能、参数与make_list相同，但创建迭代器，且迭代器中可能有重复的对象。


**search(obj, start, recursions=3, search_str=False)**:

从一个起点开始搜索对象，如`search(os, sys, 3)`返回`["sys.modules['site'].os", "sys.modules['os']", ...]`的结果。

- obj: 待搜索的对象
- start: 起点对象
- recursion: 递归次数
- search_str: 是否是查找字符串子串

## 类: `pyobject.Code`

类Code提供了Python字节码(bytecode)对象的封装，便于操作Python字节码。

Python内部的字节码对象`CodeType`，如`func.__code__`，是不可变的，这里的Code类提供了一个**可变**的字节码对象，以及一系列方法，使得操作底层字节码变得更容易。

此外和Java字节码不同，Python字节码是**不跨版本**的，不同版本Python解释器的字节码互不兼容，

而Code类提供了字节码的**通用接口**，支持**3.4至3.14**之间的所有Python版本（甚至PyPy的.pyc格式），简化了复杂的版本兼容性问题。

#### 构造函数（`Code(code=None)`）
`code`参数可以是现有的 `CodeType` 对象，或者另一个 `Code` 实例。如果未提供`code，则会创建一个默认的 `CodeType` 对象。

#### 属性

- `_code`: 当前Code对象的内部字节码，如应使用`exec(c._code)`或`exec(c.to_code())`，而不是直接使用`exec(c)`。

以下是Python内置字节码的属性（也是`Code`对象的属性）。Python内部的字节码`CodeType`是不可变的，这些属性只读，但`Code`对象可变，也就是这些属性都**可修改**:

- `co_argcount`: 位置参数的数量（包括有默认值的参数）。
- `co_cellvars`: 一个包含被嵌套函数所引用的局部变量名称的元组。
- `co_code`: 一个表示字节码指令序列的`bytes`类型，存放真正的二进制字节码。
- `co_consts`: 一个包含字节码所使用的字面值的元组。
- `co_filename`: 被编码代码所在的文件名。
- `co_firstlineno`: 字节码对应到源文件首行的行号，在解释器内部和`co_lnotab`结合使用，用来在Traceback中输出精确的行号。
- `co_flags`: 一个以整数编码表示的多个解释器所用的旗标。
- `co_freevars`: 一个包含自由变量名称的元组。
- `co_kwonlyargcount`: 仅关键字参数的数量。
- `co_lnotab`: 一个以编码表示的从字节码偏移量到行号的映射的字符串（Python 3.10开始，被`co_linetable`替代）。
- `co_name`: 字节码对应的函数/类名称。
- `co_names`: 一个包含字节码所使用的名称的元组。
- `co_nlocals`: 函数使用的局部变量数量（包括参数）。
- `co_stacksize`: 执行字节码需要的栈大小。
- `co_varnames`: 一个包括局部变量名称的元组（以参数名打头）。

3.8及以上版本新增的属性:

- `co_posonlyargcount`:  仅位置参数的数量，在Python 3.8引入。
- `co_linetable`: 行号映射数据，从3.10开始作为`co_lnotab`属性的替代。
- `co_exceptiontable`: 异常表数据，Python 3.11引入。
- `co_qualname`: 字节码的全名，Python 3.11引入。

#### 方法

**主要方法**

- `exec(globals_=None, locals_=None)`：在全局和局部作用域字典中执行代码对象。
- `eval(globals_=None, locals_=None)`：在全局和局部作用域字典中执行代码对象，并获取返回值。
- `copy()`：复制一份`Code`对象，返回复制的副本。
- `to_code()`：将 `Code` 实例转换回内置的 `CodeType` 对象，和`c._code`相同。
- `to_func(globals_=None, name=None, argdefs=None, closure=None, kwdefaults=None)`：将代码对象转换为 Python 函数，参数用法和Python内置`FunctionTypes`实例化的参数相同。
- `get_flags()`：返回 `co_flags` 属性的标志名称列表，如`["NOFREE"]`。
- `get_sub_code(name)`：搜索代码的`co_consts`中的子代码，如函数、类定义等，不会递归搜索。返回搜索到的`Code`对象，未找到时抛出`ValueError`。

**序列化**

- `to_pycfile(filename)`：使用 `marshal` 模块将代码对象转储到 `.pyc` 文件中。
- `from_pycfile(filename)`：从 `.pyc` 文件创建 `Code` 实例。
- `from_file(filename)`：从 `.py` 或 `.pyc` 文件创建 `Code` 实例。
- `pickle(filename)`：将 `Code` 对象序列化为 pickle 文件。

**调试和检查**

- `show(*args, **kw)`：在内部调用`pyobject.desc`，显示代码对象的属性，参数用法和`desc()`的用法相同。
- `info()`：在内部调用`dis.show_code`，显示字节码的基本信息。
- `dis(*args, **kw)`：调用 `dis` 模块输出字节码的反汇编，和`dis.dis(c.to_code())`相同。
- `decompile(version=None, *args, **kw)`：调用 `uncompyle6` 库将代码对象反编译为源代码。（安装`pyobject`库时， `uncompyle6` 库是可选的。）

**工厂函数**

- `fromfunc(function)`：从 Python 函数对象创建 `Code` 实例，和`Code(func.__code__)`相同。
- `fromstring(string, mode='exec', filename='')`：从源代码字符串创建 `Code` 实例，参数用法和`compile`内置函数相同，在内部调用`compile()`。

#### 兼容性细节

- 属性`co_lnotab`：在3.10以上的版本中，如果尝试设置`co_lnotab`属性，会自动转换成设置`co_linetable`。


示例用法: (从doctest中摘取):

```python
>>> def f():print("Hello")
>>> c=Code.fromfunc(f) # 或 c=Code(f.__code__)
>>> c.co_consts
(None, 'Hello')
>>> c.co_consts=(None, 'Hello World!')
>>> c.exec()
Hello World!
>>>
>>> # 保存到 pickle 文件
>>> import os,pickle
>>> temp=os.getenv('temp')
>>> with open(os.path.join(temp,"temp.pkl"),'wb') as f:
...     pickle.dump(c,f)
...
>>> # 读取pickle文件，并重新执行读取到的字节码
>>> f=open(os.path.join(temp,"temp.pkl"),'rb')
>>> pickle.load(f).to_func()()
Hello World!
>>> # 转换为pyc文件，并导入pyc模块
>>> c.to_pycfile(os.path.join(temp,"temppyc.pyc"))
>>> sys.path.append(temp)
>>> import temppyc
Hello World!
>>> Code.from_pycfile(os.path.join(temp,"temppyc.pyc")).exec()
Hello World!
```

## 对象代理类`ObjChain`和`ProxiedObj`

`pyobject.objproxy`是一个强大的代理任何其他对象，生成调用对象的代码的工具，能够记录对象的详细访问和调用历史记录。
`ObjChain`是用于管理多个`ProxiedObj`对象的类封装，`ProxiedObj`是代理其他对象的类。  

示例用法：
```python
from pyobject import ObjChain

chain = ObjChain(export_attrs=["__array_struct__"])
np = chain.new_object("import numpy as np","np")
plt = chain.new_object("import matplotlib.pyplot as plt","plt",
                        export_funcs = ["show"])

# 测试调用代理后的numpy, matplotlib模块
arr = np.array(range(1,11))
arr_squared = arr ** 2
print(np.mean(arr)) # 输出平均值

plt.plot(arr, arr_squared) # 绘制y=x**2的图像
plt.show()

# 显示自动生成的调用numpy, matplotlib库的代码
print(f"Code:\n{chain.get_code()}\n")
print(f"Optimized:\n{chain.get_optimized_code()}")
```
输出效果：
```python
Code: # 未优化的代码，包含了对象的所有详细访问记录
import numpy as np
import matplotlib.pyplot as plt
var0 = np.array
var1 = var0(range(1, 11))
var2 = var1 ** 2
var3 = np.mean
var4 = var3(var1)
var5 = var1.mean
var6 = var5(axis=None, dtype=None, out=None)
ex_var7 = str(var4)
var8 = plt.plot
var9 = var8(var1, var2)
var10 = var1.to_numpy
var11 = var1.values
var12 = var1.shape
var13 = var1.ndim
...
var81 = var67.__array_struct__
ex_var82 = iter(var70)
ex_var83 = iter(var70)
var84 = var70.mask
var85 = var70.__array_struct__
var86 = plt.show
var87 = var86()

Optimized: # 优化后的代码
import numpy as np
import matplotlib.pyplot as plt
var1 = np.array(range(1, 11))
plt.plot(var1, var1 ** 2)
plt.show()
```

#### 详细用法

**`ObjChain`**  
- `ObjChain(export_funcs = None, export_attrs = None)`: 创建一个`ObjChain`对象，`export_funcs`为全局范围需要导出的函数列表，`export_attrs`为全局范围需要导出的属性列表。由于是全局范围，对所有变量有效。
- `new_object(code_line,name, export_funcs=None, export_attrs=None, use_target_obj=True, use_exported_obj=True)`: 新增一个对象，返回一个生成的`ProxiedObj`类型的代理对象，返回值可以直接当作普通对象使用。  
`code_line`: 为了得到这个对象而需要执行的代码（如`"import numpy as np"`），`name`是执行之后对象放在的变量值（如`"np"`）。  
`export_funcs`和`export_attrs`: 针对这个对象，需要导出的方法和属性列表。  
`use_target_obj`: 是否实时创建一个代理的模板对象，并操作（详见“实现原理”一节）。  
`use_exported_obj`: 是否不将`ProxiedObj`对象在调用参数中传递给`__target_obj`。  
- `add_existing_obj(obj, name)`: 添加现有的对象，返回一个`ProxiedObj`类型的代理对象。  
`obj`为对象，`name`为任意的变量名，用来在`ObjChain`生成的代码中，指代这个对象。  
- `get_code(start_lineno=None, end_lineno=None)`: 获取`ObjChain`生成的原始代码，`start_lineno`和`end_lineno`为从0开始的行号，如果未指定，则默认为开头和末尾。
- `get_optimized_code(no_optimize_vars=None, remove_internal=True, remove_export_type=True)`: 获取优化后的代码，内部使用了有向无环图(DAG)进行优化（详见“实现原理”一节）。  
`no_optimize_vars`: 不能移除的变量名的列表，如`["temp_var"]`。  
`remove_internal`: 是否移除执行代码本身时产生的内部代码。例如`plt.plot`和`arr`, `arr2`都是`ProxiedObj`对象，
如果`remove_internal`为`False`，调用`plt.plot(arr,arr2)`本身时生成的访问`arr`, `arr2`的内部代码，如`var13 = arr.ndim`不会被移除。  
`remove_export_type`: 是否移除无用的类型导出，如`str(var)`。  

**`ProxiedObj`**  

`ProxiedObj`为`ObjChain`的`new_object()`、`add_existing_obj()`返回的代理对象的类型，可以替代任何普通对象使用，但通常不建议直接使用`ProxiedObj`类本身的方法和属性。  

#### 实现原理

`ObjChain`类**追踪**所有加入`ObjChain`的对象，以及派生出的对象，并且维护一个包含被追踪的对象的命名空间字典，用于调用`exec`执行自身生成的代码。  
每个`ProxiedObj`对象属于一个`ObjChain`。`ProxiedObj`类的所有魔法方法（如`__call__`, `__getattr__`）都是被**重写**的，重写的方法一边将调用记录加入`ProxiedObj`属于的`ObjChain`，
一边调用自身代理的对象`__target_obj`（如果有）的相同魔法方法。  
当对`ProxiedObj`的操作返回了新的对象（如`obj.attr`返回新的属性）时，新的对象也会被`ObjChain`追踪，直到`ObjChain`内部形成一个从第一个对象开始，派生出的所有对象的**长链**。  
如果`ProxiedObj`存在`__target_obj`属性，则调用`ProxiedObj`的魔法方法时，会**同步**地调用`__target_obj`的魔法方法，并将返回的结果传递给下一个`ProxiedObj`的`__target_obj`属性。  
如果`__target_obj`属性不存在，`ProxiedObj`不会同步地调用魔法方法，而是生成一份调用记录的代码，**临时保存**在`ProxiedObj`中，直到出现了需要导出（`export`）的方法或属性，
才会一次性执行全部之前加入的代码，并返回结果。  

**代码优化的原理**

在代码中，变量的依赖关系可以表示为一个**图**，如语句`y = func(x)`可以表示为节点`x`有一条指向`y`的边。  
但由于`ProxiedObj`生成的代码中一个对象只能对应一个变量，变量不能被重新赋值（类似js的`const`），会形成一个有向无环图(DAG)。  
优化时首先找出只影响0个或1个其他变量（只指向0~1个其他节点）的变量，如果只影响一个变量，则将自身的值代入被影响的语句进行内联，否则直接去除自身。  
如：
```python
temp_var = [1,2,3]
unused_var = func(temp_var)
```
代码中`temp_var`只有一条指向`unused_var`的边，而`unused_var`没有任何指出的边。  
将`temp_var`的值代入`func(temp_var)`进行内联，得到`unused_var = func([1,2,3])`，再去掉`unused_var`，优化后的代码会变成`func([1,2,3])`。  

## 模块`pyobject.pyobj_extension`

本模块使用了C语言编写。可使用`import pyobject.pyobj_extension as pyobj_extension`, 导入该独立模块。其中包含的函数如下:

**convptr(pointer)**:

将整数指针转换为Python对象，与id()相反。

**py_decref(object, n)**:

将对象的引用计数减小1。

**py_incref(object, n)**:

将对象的引用计数增加1。

**getrealrefcount(obj)**:

获取调用本函数前对象的实际引用计数。和sys.getrefcount()不同，不考虑调用时新增的引用计数。(差值为`_REFCNT_DELTA`这个常量)  
如：getrealrefcount([])会返回0，因为退出getrealrefcount后列表[]不再被任何对象引用，而sys.getrefcount([])会返回1。  
另外，a=[];getrealrefcount(a)会返回1而不是2。

**setrefcount(obj, n)**:

设置对象的实际引用计数(调用函数前)为n，和getrealrefcount()相反，同样不考虑调用时新增的引用计数。

**getrefcount_nogil(obj)**和**setrefcount_nogil(obj,ref_data)**:

在Python 3.14+的无GIL版本中获取和设置引用计数，`ref_data`为`(ob_ref_local, ob_ref_shared)`，不考虑调用时新增的引用计数。(实验性)

*警告: 不恰当地调用这些函数可能导致Python崩溃。*

**list_in(obj, lst)**:

判断obj是否在列表或元组lst中。与Python内置的obj in lst调用多次==运算符(`__eq__`)相比，
本函数直接比较对象的指针，提高了效率。


**`pyobject`当前版本**: 1.3.2

## 更新日志:

2025-6-23(v1.3.2):为pyobject.objproxy模块新增了`use_exported_obj`参数，并进一步优化性能。  
2025-6-6(v1.3.0):性能优化，提升了pyobject.objproxy模块的性能。  
2025-4-30(v1.2.9):改进和增强了子模块pyobject.objproxy，重命名子模块pyobject.code_为pyobject.code。  
2025-3-31(v1.2.8):将pyobject.super_proxy重命名为pyobject.objproxy，并正式发布；修改了pyobject.pyobj_extension模块。  
2025-3-6(v1.2.7):为pyobject.browser新增了`dir()`中不存在的类属性（如`__flags__`, `__mro__`），修改了pyobj_extension模块。  
2025-2-15(v1.2.6):修复了pyobject.browser浏览过大对象的卡顿问题，改进了pyobject.code_模块，新增了正在开发中的反射库pyobject.super_proxy，
在pyobj_extension新增了`getrefcount_nogil`和`setrefcount_nogil`。  
2024-10-24(v1.2.5):修复了pyobject.browser在Windows下的高DPI支持，修改了pyobj_extension模块，以及其他改进。  
2024-8-12(v1.2.4):针对pyobject.code_增加了对3.10及以上版本的支持；进一步优化了search模块的搜索性能，以及一些其他修复和改进。  
2024-6-20(v1.2.3):更新了包内test目录下的.pyc文件加壳工具，并更新了pyobject.browser中的对象浏览器，添加了显示列表和字典项，后退、前进、刷新页面，以及新增、编辑和删除项等新特性。  
2022-7-25(v1.2.2):增加了操作Python底层对象引用, 以及对象指针的C语言模块pyobj_extension。  
2022-2-2(v1.2.0):修复了一些bug,优化了search模块的性能; code_中增加了Code类, browser中增加编辑属性功能, 增加了Code类的doctest。  
