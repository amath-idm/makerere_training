'''
Define parameters
'''

import sciris as sc

variants = sc.objdict(

    delta = dict(
        rel_beta        = 2.2, # Estimated to be 1.25-1.6-fold more transmissible than B117: https://www.researchsquare.com/article/rs-637724/v1
        rel_symp_prob   = 1.0,
        rel_severe_prob = 3.2, # 2x more transmissible than alpha from https://mobile.twitter.com/dgurdasani1/status/1403293582279294983
        rel_crit_prob   = 1.0,
        rel_death_prob  = 1.5, # CK: calibrated
    ),
    
    omicron = dict(
        rel_beta        = 9.0, # CK: calibrated
        rel_symp_prob   = 1.0,
        rel_severe_prob = 0.8,
        rel_crit_prob   = 0.5,
        rel_death_prob  = 1.0*0.2, # CK: calibrated
    ),
)


vaccines = sc.objdict(

    pfizer = dict(
        wild  = 1.0,
        alpha = 1/2.0, # https://www.nejm.org/doi/full/10.1056/nejmc2100362
        beta  = 1/10.3, # https://www.nejm.org/doi/full/10.1056/nejmc2100362
        gamma = 1/6.7, # https://www.nejm.org/doi/full/10.1056/nejmc2100362
        delta = 1/2.9, # https://www.researchsquare.com/article/rs-637724/v1
        omicron = 1/40 # https://www.medrxiv.org/content/10.1101/2021.12.28.21268481v1
    ),

)