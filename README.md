# README
生物信息数据分析实验 of gf LJ (1804)。

由于MainByLJ.py和MainByTeacher.py运行时间可达6小时，因此重写MainByRayiooo.py以解决该程序的运行效率，实现2分钟内运行完成。

|Author|爱吃大板|
|---|---|
|Email|rayiooo@foxmail.com|

## 要求
取出 1.tab 中的编号和GO，根据 go-basic.obo 中的 is_a 关系和 part_of 关系（仅这两个关系是父子关系）找到每个编号所有GO及GO的父、爷……GO。

例如在 go-basic.obo 中这个Term：
```
[Term]
id: GO:0006869
name: lipid transport
namespace: biological_process
def: "The directed movement of lipids into, out of or within a cell, or between cells, by means of some agent such as a transporter or pore. Lipids are compounds soluble in an organic solvent but not, or sparingly, in an aqueous solvent." [ISBN:0198506732]
subset: goslim_pir
subset: goslim_yeast
subset: gosubset_prok
is_a: GO:0071702 ! organic substance transport
relationship: part_of GO:0010876 ! lipid localization
```
表示 GO:0006869 的父GO有 GO:0071702 和 GO:0010876。

## MainByRayiooo.py

Wrote by LJ's bf rayiooo, use tree and Breadth First Search to handle the problem.

Only run less than 2 minutes.
