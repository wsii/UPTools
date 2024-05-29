import os
import unreal
# NOTE 生成一个 Unreal Class 对象
@unreal.uclass()
class PyBPFunctionLibrary(unreal.BlueprintFunctionLibrary):
    # NOTE 蓝图库分类设置为 Python Blueprint
    @unreal.ufunction(static=True,meta=dict(Category="Python Blueprint"))
    def TestFunction():
        unreal.SystemLibrary.print_string(None,'Python Test Function Run',text_color=[255,255,255,255])

    @unreal.ufunction(params=[str],ret=str,static=True,meta=dict(Category="Python Blueprint"))
    def TestReadFile(filepath):
        if not os.path.exists(filepath):
            return ''
        with open(filepath,'r') as f:
            data = f.read()
        return data