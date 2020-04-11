# VainPy
> VainPy refers to Vasp analysis in numerical Python as it is based on numpy, alogwith xml ElementTree package in python.


This file will become your README and also the index of your documentation.

## Install

`pip install VainPy`

## How to use

```python
from VainPy import vr_parser as vp
vr=vp.export_vasprun()
```

```python
vr.keys()
```




    dict_keys(['sys_info', 'dim_info', 'kpoints', 'kpath', 'bands', 'tdos', 'pro_bands', 'pro_dos', 'poscar', 'xml'])



```python
xml_data=vp.read_asxml(path='./vasprun.xml').xml
```

```python
vp.exclude_kpts(xml_data=xml_data)
```




    {'skipk': 10}



```python
vp.get_summary(xml_data=xml_data)
```




    {'SYSTEM': 'AlAs',
     'NION': 2,
     'TypeION': 2,
     'ElemName': ['Al', 'As'],
     'ElemIndex': [0, 1, 2],
     'ISPIN': 1}



```python
import matplotlib.pyplot as plt
import numpy as np
en=vr.tdos.tdos[:,0]
dos=vr.tdos.tdos[:,1]
plt.plot(en,dos)
```




    [<matplotlib.lines.Line2D at 0x1f467864108>]



```python
k=vr.kpath
ef=vr.bands.E_Fermi
evals=vr.bands.evals-ef
plot=plt.plot(k,evals,'b')
```


![png](docs/images/output_10_0.png)

