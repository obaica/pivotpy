# AUTOGENERATED! DO NOT EDIT! File to edit: XmlElementTree.ipynb (unless otherwise specified).

__all__ = ['Dic2Dot', 'read_asxml', 'exclude_kpts', 'get_ispin', 'get_summary', 'get_kpts', 'get_tdos', 'get_evals',
           'get_bands_pro_set', 'get_dos_pro_set', 'get_structure', 'export_vasprun']

# Cell
class Dic2Dot(dict):
    """
    Returns dot notation accessible if a dictionary is input.
    """
    def __getattr__(self, name):
        return self[name]

# Cell
def read_asxml(path=None):
    if(path==None):
        path='./vasprun.xml'
    import xml.etree.ElementTree as ET
    if(not path):
        print('vasprun.xml not found.')
    else:
        tree = ET.parse(path)
        xml_data = tree.getroot()
        return xml_data

# Cell
def exclude_kpts(xml_data=None):
    if(xml_data==None):
        xml_data=read_asxml()
    for kpts in xml_data.iter('varray'):
        if(kpts.attrib=={'name': 'weights'}):
            weights=[float(arr.text.strip()) for arr in kpts.iter('v')]
    exclude=[]
    [exclude.append(item) for item in weights if item!=weights[-1]];
    skipk=len(exclude) #that much to skip
    return Dic2Dot({'skipk':skipk})

# Cell
def get_ispin(xml_data=None):
    if(xml_data==None):
        xml_data=read_asxml()
    for item in xml_data.iter('i'):
        if(item.attrib=={'type': 'int', 'name': 'ISPIN'}):
            return Dic2Dot({'ISPIN':int(item.text)})

# Cell
def get_summary(xml_data=None):
    if(xml_data==None):
        xml_data=read_asxml()
    for i_car in xml_data.iter('incar'):
        incar={car.attrib['name']:car.text.strip() for car in i_car}
    n_ions=[int(atom.text) for atom in xml_data.iter('atoms')][0]
    type_ions=[int(atom_types.text) for atom_types in xml_data.iter('types')][0]
    elem=[info[0].text.strip() for info in xml_data.iter('rc')]
    elem_name=[]; #collect IONS names
    [elem_name.append(item) for item in elem[:-type_ions] if item not in elem_name]
    elem_index=[0]; #start index
    [elem_index.append((int(entry)+elem_index[-1])) for entry in elem[-type_ions:]];
    ISPIN=get_ispin(xml_data=xml_data).ISPIN
    #Writing information to a dictionary
    info_dic={'SYSTEM':incar['SYSTEM'],'NION':n_ions,'TypeION':type_ions,'ElemName':elem_name,\
             'ElemIndex':elem_index,'ISPIN':ISPIN}
    return Dic2Dot(info_dic)

# Cell
def get_kpts(xml_data=None,skipk=0):
    if(xml_data==None):
        xml_data=read_asxml()
    import numpy as np
    for kpts in xml_data.iter('varray'):
        if(kpts.attrib=={'name': 'kpointlist'}):
            kpoints=[[float(item) for item in arr.text.split()] for arr in kpts.iter('v')]
    kpoints=np.array(kpoints[skipk:])
    #KPath solved.
    kpath=[0];pts=kpoints
    [kpath.append(np.round(np.sqrt(np.sum((pt1-pt2)**2))+kpath[-1],6)) for pt1,pt2 in zip(pts[:-1],pts[1:])];
    return Dic2Dot({'NKPTS':len(kpoints),'kpoints':kpoints,'kpath':kpath})

# Cell
def get_tdos(xml_data=None,spin_set=1,elim=[]):
    if(xml_data==None):
        xml_data=read_asxml()
    import numpy as np #Mandatory to avoid errors.
    tdos=[]; #assign for safely exit if wrong spin set entered.
    ISPIN=get_ispin(xml_data=xml_data).ISPIN
    for neighbor in xml_data.iter('dos'):
        for item in neighbor[1].iter('set'):
            if(ISPIN==1 and spin_set==1):
                if(item.attrib=={'comment': 'spin 1'}):
                    tdos=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
            if(ISPIN==2 and spin_set==1):
                if(item.attrib=={'comment': 'spin 1'}):
                    tdos_1=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
                if(item.attrib=={'comment': 'spin 2'}):
                    tdos_2=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
                    tdos=Dic2Dot({'SpinUp':tdos_1,'SpinDown':tdos_2})
            if(spin_set!=1): #can get any
                if(item.attrib=={'comment': 'spin {}'.format(spin_set)}):
                    tdos=np.array([[float(entry) for entry in arr.text.split()] for arr in item])
    for i in xml_data.iter('i'):
        if(i.attrib=={'name': 'efermi'}):
            efermi=float(i.text)
    dos_dic=Dic2Dot({'E_Fermi':efermi,'ISPIN':ISPIN,'tdos':tdos})
    #Filtering in energy range.
    if elim: #check if elim not empty
        if(ISPIN==1 and spin_set==1):
            up_ind=np.max(np.where(tdos[:,0]-efermi<=np.max(elim)))+1
            lo_ind=np.min(np.where(tdos[:,0]-efermi>=np.min(elim)))
            tdos=tdos[lo_ind:up_ind,:]
        if(ISPIN==2 and spin_set==1):
            up_ind=np.max(np.where(tdos.SpinUp[:,0]-efermi<=np.max(elim)))+1
            lo_ind=np.min(np.where(tdos.SpinUp[:,0]-efermi>=np.min(elim)))
            tdos=Dic2Dot({'SpinUp':tdos_1[lo_ind:up_ind,:],'SpinDown':tdos_2[lo_ind:up_ind,:]})
        if(spin_set!=1):
            up_ind=np.max(np.where(tdos[:,0]-efermi<=np.max(elim)))+1
            lo_ind=np.min(np.where(tdos[:,0]-efermi>=np.min(elim)))
            tdos=tdos[lo_ind:up_ind,:]
        dos_dic=Dic2Dot({'E_Fermi':efermi,'ISPIN':ISPIN,'grid_range':range(lo_ind,up_ind),'dos':tdos})
    return dos_dic

# Cell
def get_evals(xml_data=None,skipk=None,elim=[]):
    if(xml_data==None):
        xml_data=read_asxml()
    import numpy as np #Mandatory to avoid errors.
    evals=[]; #assign for safely exit if wrong spin set entered.
    ISPIN=get_ispin(xml_data=xml_data).ISPIN
    if skipk!=None:
        skipk=skipk
    else:
        skipk=exclude_kpts(xml_data=xml_data).skipk #that much to skip by default
    for neighbor in xml_data.iter('eigenvalues'):
            for item in neighbor[0].iter('set'):
                if(ISPIN==1):
                    if(item.attrib=={'comment': 'spin 1'}):
                        evals=np.array([[float(th.text.split()[0]) for th in thing] for thing in item])[skipk:]
                        NBANDS=len(evals[0])
                if(ISPIN==2):
                    if(item.attrib=={'comment': 'spin 1'}):
                        eval_1=np.array([[float(th.text.split()[0]) for th in thing] for thing in item])[skipk:]
                    if(item.attrib=={'comment': 'spin 2'}):
                        eval_2=np.array([[float(th.text.split()[0]) for th in thing] for thing in item])[skipk:]
                        evals=Dic2Dot({'SpinUp':eval_1,'SpinDown':eval_2})
                        NBANDS=len(eval_1[0])

    for i in xml_data.iter('i'): #efermi for condition required.
        if(i.attrib=={'name': 'efermi'}):
            efermi=float(i.text)
    evals_dic=Dic2Dot({'E_Fermi':efermi,'ISPIN':ISPIN,'NBANDS':NBANDS,'evals':evals})
    if elim: #check if elim not empty
        if(ISPIN==1):
            up_ind=np.max(np.where(evals[:,:]-efermi<=np.max(elim))[1])+1
            lo_ind=np.min(np.where(evals[:,:]-efermi>=np.min(elim))[1])
            evals=evals[:,lo_ind:up_ind]
        if(ISPIN==2):
            up_ind=np.max(np.where(eval_1[:,:]-efermi<=np.max(elim))[1])+1
            lo_ind=np.min(np.where(eval_1[:,:]-efermi>=np.min(elim))[1])
            evals=Dic2Dot({'SpinUp':eval_1[:,lo_ind:up_ind],'SpinDown':eval_2[:,lo_ind:up_ind]})
        NBANDS=up_ind-lo_ind #update Bands
        evals_dic=Dic2Dot({'E_Fermi':efermi,'ISPIN':ISPIN,'NBANDS': NBANDS,'bands_range':range(lo_ind,up_ind),'evals':evals})
    return evals_dic

# Cell
def get_bands_pro_set(xml_data=None,spin_set=1,skipk=0,bands_range=None):
    if(xml_data==None):
        xml_data=read_asxml()
    import numpy as np
    #Collect Projection fields
    fields=[];
    for pro in xml_data.iter('projected'):
        for arr in pro.iter('field'):
            if('eig' not in arr.text and 'occ' not in arr.text):
                fields.append(arr.text.strip())
    #Get NIONS for reshaping data
    n_ions=[int(atom.text) for atom in xml_data.iter('atoms')][0]
    #check if bands_range provided. if not get all bands in projection.
    if bands_range==None:
        NBANDS=get_evals(xml_data=xml_data,skipk=skipk).NBANDS
        bands_range=range(0,NBANDS)
    else:
        bands_range=bands_range

    bands=[];bands_range=[ind+1 for ind in bands_range];
    for i in bands_range: #Bands loop.index written from 1.
        pro=[];
        for spin in xml_data.iter('set'):
            if(spin.attrib=={'comment': 'spin{}'.format(spin_set)}):
                for band in spin.iter('set'):
                    if(band.attrib=={'comment': 'band {}'.format(i)}):
                        for r in band.iter('r'):
                            pro.append(r.text)
        bands.append(pro)
    flist=[[[float(item) for item in entry.split()] for entry in pro] for pro in bands]
    #data shape is (NION,NKPTS,NBANDS,nProjections)
    data=np.reshape(flist,(len(flist),-1,n_ions,len(fields))).transpose([2,1,0,3])
    final_data=data[:,skipk:,:,:] #skip useless kpoints
    return Dic2Dot({'labels':fields,'pros':final_data})

# Cell
def get_dos_pro_set(xml_data=None,spin_set=1,dos_range=None):
    if(xml_data==None):
        xml_data=read_asxml()
    import numpy as np
    type_ion=get_summary(xml_data=xml_data).TypeION
    for pro in xml_data.iter('partial'):
        dos_fields=[field.text.strip()for field in pro.iter('field')]
        #Collecting projections.
        dos_pro=[]; set_pro=[]; #set_pro=[] in case spin set does not exists
        for ion in range(type_ion):
            for node in pro.iter('set'):
                if(node.attrib=={'comment': 'ion {}'.format(ion+1)}):
                    for spin in node.iter('set'):
                        if(spin.attrib=={'comment': 'spin {}'.format(spin_set)}):
                            set_pro=[[float(entry) for entry in r.text.split()] for r in spin.iter('r')]
            dos_pro.append(set_pro)
    if dos_range==None: #full grid computed.
        dos_pro=np.array(dos_pro) #shape(NION,e_grid,pro_fields)
    else:
        dos_range=list(dos_range)
        min_ind=dos_range[0]
        max_ind=dos_range[-1]+1
        dos_pro=np.array(dos_pro)[:,min_ind:max_ind,:]
    final_data=np.array(dos_pro) #shape(NION,e_grid,pro_fields)
    return Dic2Dot({'labels':dos_fields,'pros':final_data})

# Cell
def get_structure(xml_data=None):
    if(xml_data==None):
        xml_data=read_asxml()
    import numpy as np
    for final in xml_data.iter('structure'):
        if(final.attrib=={'name': 'finalpos'}):
            for i in final.iter('i'):
                volume=float(i.text)
            for arr in final.iter('varray'):
                if(arr.attrib=={'name': 'basis'}):
                    basis=[[float(a) for a in v.text.split()] for v in arr.iter('v')]
                if(arr.attrib=={'name': 'rec_basis'}):
                    rec_basis=[[float(a) for a in v.text.split()] for v in arr.iter('v')]
                if(arr.attrib=={'name': 'positions'}):
                    positions=[[float(a) for a in v.text.split()] for v in arr.iter('v')]
    st_dic={'volume': volume,'basis': np.array(basis),'rec_basis': np.array(rec_basis),'positions': np.array(positions)}
    return Dic2Dot(st_dic)

# Cell
def export_vasprun(xml_data=None,skipk=None,elim=[]):
    """
    Iput: read_asxml().xml object.
    Output: A dictionary accessible via dot notation containing objects:
        sys_info: System Information
        kpoints: numpy array of kpoints with excluded IBZKPT points
        kpath: 1D numpy array directly accessible for plot.
        evals: Dictionary.
        tdos: Dictionary.
        incar: INCAR file as dictionary accessible via dot notation.
        xml: xml root object which is iterable over nodes using xml.iter('node').
    """
    if(xml_data==None):
        xml_data=read_asxml()
    import numpy as np
    #First exclude unnecessary kpoints. Includes only same weight points
    if skipk!=None:
        skipk=skipk
    else:
        skipk=exclude_kpts(xml_data=xml_data).skipk #that much to skip by default
    info_dic=get_summary(xml_data=xml_data) #Reads important information of system.
    #KPOINTS
    kpts=get_kpts(xml_data=xml_data,skipk=skipk)
    #EIGENVALS
    eigenvals=get_evals(xml_data=xml_data,skipk=skipk,elim=elim)
    #TDOS
    tot_dos=get_tdos(xml_data=xml_data,spin_set=1,elim=elim)
    #Bands and DOS Projection
    if elim:
        bands_range=eigenvals.bands_range
        grid_range=tot_dos.grid_range
    else:
        bands_range=None #projection function will read itself.
        grid_range=None
    if(info_dic.ISPIN==1):
        pro_bands=get_bands_pro_set(xml_data=xml_data,spin_set=1,skipk=skipk,bands_range=bands_range)
        pro_dos=get_dos_pro_set(xml_data=xml_data,spin_set=1,dos_range=grid_range)
    if(info_dic.ISPIN==2):
        pro_1=get_bands_pro_set(xml_data=xml_data,spin_set=1,skipk=skipk,bands_range=bands_range)
        pro_2=get_bands_pro_set(xml_data=xml_data,spin_set=2,skipk=skipk,bands_range=bands_range)
        pros=Dic2Dot({'SpinUp': pro_1.pros,'SpinDown': pro_2.pros}) #accessing spins in dictionary after .pro.
        pro_bands=Dic2Dot({'labels':pro_1.labels,'pros': pros})
        pdos_1=get_dos_pro_set(xml_data=xml_data,spin_set=1,dos_range=grid_range)
        pdos_2=get_dos_pro_set(xml_data=xml_data,spin_set=1,dos_range=grid_range)
        pdos=Dic2Dot({'SpinUp': pdos_1.pros,'SpinDown': pdos_2.pros}) #accessing spins in dictionary after .pro.
        pro_dos=Dic2Dot({'labels':pdos_1.labels,'pros': pdos})

    #Structure
    poscar=get_structure(xml_data=xml_data)
    #Dimensions dictionary.
    dim_dic=Dic2Dot({'kpoints':'(NKPTS,3)','kpath':'(NKPTS,1)','bands':'(NKPTS,NBANDS)',\
                     'dos':'(grid_size,3)','pro_dos':'(NION,grid_size,en+pro_fields)',\
                     'pro_bands':'(NION,NKPTS,NBANDS,pro_fields)'})
    #Writing everything to be accessible via dot notation
    full_dic={'sys_info':Dic2Dot(info_dic),'dim_info':dim_dic,'kpoints':kpts.kpoints,'kpath':kpts.kpath,'bands':eigenvals,
             'tdos':tot_dos,'pro_bands':pro_bands,'pro_dos':pro_dos,'poscar': poscar,'xml':xml_data}
    return Dic2Dot(full_dic)