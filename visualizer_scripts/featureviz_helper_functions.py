#functions for using lucent to get visualizations
from lucent.optvis import render
from lucent.modelzoo import inceptionv1
from lucent.modelzoo.util import get_model_layers
from lucent.optvis import render, param, transform, objectives

import inspect
import time
import pandas as pd

from visualizer_helper_functions

def gen_visualization(model,image_name,objective,parametrizer,optimizer,tranforms,params):
    full_image_path = params['prepped_model_path']+'/visualizations/images/'+image_name
    _ = render.render_vis(model, objective, parametrizer, optimizer, transforms=transforms,save_image=True,image_name=full_image_path)

def gen_objective_str(targetid,model,params):
    if '-' in targetid:
        within_id = edgename_2_singlenum(model,targetid,params):
        layer_name = nodeid_2_perlayerid(targetid.split('-')[1],params)[2]
        return layer_name+'_preadd_conv:'+str(within_id)
    else:
        layer, within_id, layer_name = nodeid_2_perlayerid(targetid,params)
        return layer_name+':'+str(within_id)

def fetch_deepviz_img(model,targetid,params):
    objective = gen_objective_str(targetid,model,params)
    file_path = params['prepped_model_path']+'/visualizations/images.csv'
    parametrizer = params['deepviz_param']
    optimizer = params['deepviz_optim']
    transforms = params['deepviz_transforms']

    param_str = object_2_str(parametrizer,"params['deepviz_param']=")
    optimizer_str = object_2_str(optimizer,"params['deepviz_optim']=")
    transform_str = object_2_str(transforms,"params['deepviz_transforms']=")
    df = pd.read_csv(file_path)
    df_sel = df.loc[(df['objective'] == objective) & (df['parametrizer'] == param_str) & df['optimizer'] == optimizer_str) & (df['transforms'] == transforms_str)]
    if len(df_sel) == 0:
        print('deepviz image not found, generating . . .')
        image_name = 'deepviz_'+str(targetid)+'_'+objective+'_'+str(time.time())+'.jpg'
        gen_visualization(model,image_name,objective,parametrizer,optimizer,tranforms,params) 
        with open(file_path, 'a') as csv:
            csv.write(','.join([image_name,objective,param_str,optimizer_str,transforms_str]))
    else:
        print('found pre-generated image')
        image_name = df_sel.iloc[0]['image_name']    
    return image_name

def object_2_str(obj,prefix):
    if isinstance(obj,str):
        return obj
    if isinstance(obj,list):
        return obj
    if obj is None:
        return('none')
    else:
        s= inspect.getsource(obj).replace(' ','').replace(prefix,'').strip()
        return inspect.getsource(obj)
    