from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import numpy as np
# import matplotlib.pyplot as plt
import sys
sys.path.append('/home/grzegorz/Desktop/risk_calc/storm-risk/riskpy/')
from vulnerability import vulnerability as vul
# import vulnerability as vul

lenght = 18.29
width = 11.58
exp_cat = 'B'
gust_speed = np.arange(0, 120)
cap_walls = 2614
cap_rc = 2442
cap_rs = 2614
cap_window = 2500
cap_door = 2400
cap_gd = 1500
cap_r2w = 1900
wall_height = 3
roof_height = 4
n_windows = 10
cov = 0.2

# ----------- Damage ratio functions --------------
dam_ratio_r2w = vul.dam_rat_r2w(exp_cat=exp_cat, gust_speed=gust_speed,
                                mean_cap=cap_r2w, lenght=lenght, width=width, cov=0.2)

damage_ratio_wall = vul.cul_dam_rat_wall(exp_cat=exp_cat, gust_speed=gust_speed, mean_cap=cap_walls,
                                         lenght=lenght, width=width, cov=cov,
                                         wall_height=wall_height, roof_height=roof_height)

damage_ratio_roof_cover = vul.cul_dam_rat_roof_cover(exp_cat=exp_cat, gust_speed=gust_speed,
                                                     mean_cap=cap_rc, lenght=lenght,
                                                     width=width, cov=cov,
                                                     wall_height=wall_height, roof_height=roof_height)

damage_ratio_roof_sh = vul.cul_dam_rat_roof_sh(exp_cat=exp_cat, gust_speed=gust_speed, mean_cap=cap_rs,
                                               lenght=lenght, width=width, cov=cov,
                                               wall_height=wall_height, roof_height=roof_height)

damage_ratio_windows = vul.cul_dam_rat_window(exp_cat=exp_cat, gust_speed=gust_speed,
                                              mean_cap=cap_window, cov=cov)

damage_ratio_door = vul.cul_dam_rat_door(exp_cat=exp_cat, gust_speed=gust_speed,
                                         mean_cap=cap_door, cov=cov)

damage_ratio_garage_door = vul.cul_dam_rat_gar_door(exp_cat=exp_cat, gust_speed=gust_speed,
                                                    mean_cap=cap_gd, cov=cov)

int_loss = vul.internal_loss(damage_ratio_roof_cover)

ng = 4  # garage door is like 4 windows
nd = 3  # front door is like 3 windows
n_open = ng + nd + n_windows
damage_ratio_openings = (ng*damage_ratio_garage_door + nd*damage_ratio_door
                         + n_windows*damage_ratio_windows)/n_open

damage_ration = vul.vulnerability(exp_cat=exp_cat, gust_speed=gust_speed, cap_walls=cap_walls,
                                  cap_rc=cap_rc, cap_rs=cap_rs, cap_window=cap_window, cap_door=cap_door,
                                  cap_gd=cap_gd, lenght=lenght, width=width, cov=0.2, wall_height=3,
                                  roof_height=4, n_windows=10)