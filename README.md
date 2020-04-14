# pivotpy
> Python Processing Tool for Vasp Input/Output.


This file will become your README and also the index of your documentation.

## Install

`pip install pivotpy`

## How to use

```
from pivotpy import vr_parser as vp
xml_data=vp.read_asxml(path='./data/vasprun.xml')
vr=vp.export_vasprun(xml_data=xml_data,elim=[-5,5])
vr.keys()
```




    dict_keys(['sys_info', 'dim_info', 'kpoints', 'kpath', 'bands', 'tdos', 'pro_bands', 'pro_dos', 'poscar', 'xml'])



```
print(vp.exclude_kpts(xml_data=xml_data).skipk)
vp.get_summary(xml_data=xml_data)
```

    10
    




    {'SYSTEM': 'GaAs',
     'NION': 2,
     'TypeION': 2,
     'ElemName': ['Ga', 'As'],
     'ElemIndex': [0, 1, 2],
     'ISPIN': 1}



```
import matplotlib.pyplot as plt
import numpy as np
en=vr.tdos.dos[:,0]
dos=vr.tdos.dos[:,1]
dplot=plt.plot(en,dos)
```


![png](docs/images/output_6_0.png)


```
k=vr.kpath
ef=vr.bands.E_Fermi
evals=vr.bands.evals-ef
plot=plt.plot(k,evals,'r')
```


![png](docs/images/output_7_0.png)

