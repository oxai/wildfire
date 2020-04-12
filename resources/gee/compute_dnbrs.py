from .config import EE_CREDENTIALS
from .methods import get_ee_product
from .vis_handler import vis_dnbr
import ee
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tifffile


ee.Initialize(EE_CREDENTIALS)

NUM_DAYS_OF_MONTHS = [0,31,59,90,120,151,181,212,243,273,304,334]

ee_product = get_ee_product(platform="sentinel", sensor="2", product="l1c")

def fname_to_fire_id(fname):
    return fname.split('__')[0]

def fname_to_date(fname):
    try:
        return fname.split('__')[2].split('.')[0]
    except: import pdb; pdb.set_trace()

def date_to_days(date):
    year,month,day = date.split('-')
    year_days = 365*int(year)
    month_days = NUM_DAYS_OF_MONTHS[int(month)-1]
    day_days = int(day)
    return year_days + month_days + day_days

def fname_to_days(fname):
    date = fname_to_date(fname)
    days = date_to_days(date)
    return days


def days_between(date1,date2): 
    return date_to_days(date1) - date_to_days(date2)

def days_between_fnames(fname1, fname2):
    date1 = fname_to_date(fname1)
    date2 = fname_to_date(fname2)
    return days_between(date1, date2)

def fpaths_to_dnbr(fpath1, fpath2, out_fpath):
    img1 = tifffile.imread(fpath1)
    img2 = tifffile.imread(fpath2)
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    dnbr_img = vis_dnbr(ee_product, arr1, vis_params=None,comp_image=arr2)
    dnbr_img.save(out_fpath)
    

def compute_dnbrs_for_dir(fire_dir):
    fname_list = [fname for fname in os.listdir(fire_dir) if not
    os.path.isdir(os.path.join(fire_dir,fname))]
    fire_ids = set([fname_to_fire_id(fname) for fname in fname_list])
    fnames_by_fire_id = {fire_id: [fname for fname in fname_list if
    fname_to_fire_id(fname) == fire_id] for fire_id in fire_ids}
    print("Fire ids:", fire_ids)

    for fire_id, id_fname_list in fnames_by_fire_id.items():
        sorted_fnames = sorted(id_fname_list,key=lambda x: fname_to_days(x))
        for i in range(1,len(sorted_fnames)):
            fname_prev, fname = sorted_fnames[i-1:i+1]
            print(fname)
            print(fname_to_date(fname))
            days_since = days_between_fnames(fname, fname_prev)
            if days_since > 10:
                continue
            date = fname_to_date(fname)
            fpath1 = os.path.join(fire_dir,fname)
            fpath2 = os.path.join(fire_dir,fname_prev)
            out_fpath = os.path.join(fire_dir,'dnbrs',f'{fire_id}-{date}-dnbr.png')
            try:
                fpaths_to_dnbr(fpath1, fpath2, out_fpath)
            except KeyboardInterrupt: sys.exit(0)
            except: print("Can't load", fname)

FIRE_DIR = '/home/oxai/GlobFire/images/sentinel-2_l1c_globfire_2015-01-01_2019-12-31_13_w_fire'
compute_dnbrs_for_dir(FIRE_DIR)
