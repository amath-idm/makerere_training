'''
Process the raw data file into a format that Covasim can read
'''

import numpy as np
import pandas as pd
import sciris as sc
import pylab as pl

do_save = 1
do_plot = 0
outfile = 'vietnam_data.csv'
popout = 'vietnam_pop.json'
datafile = 'vietnam_vaccine_impact_data_2022sep03_renamed.xlsx'
popfile = 'Vietnam_Province_Region_Population.xlsx'
datadir = sc.path(sc.thisdir()) / '../data'

start_day = '2021-05-01'
end_day = '2022-05-01'

if __name__ == '__main__':

    T = sc.timer()
    
    sc.heading('Reading in the data...')
    datafn = datadir / datafile
    popfn = datadir / popfile
    
    dfs = sc.objdict(pd.read_excel(datafn, sheet_name=None))
    pop = pd.read_excel(popfn, header=2)
    
    sc.heading('Combining into daily totals...')
    totals = sc.objdict()
    for k,df in dfs.items():
        totals[k] = df.groupby('Date').sum()
        
    sc.heading('Merging into single dataframe...')
    dates = []
    for k,df in totals.items():
        dates += sc.date(df.index.to_list())
    dates = np.unique(dates)
    
    merged = sc.dataframe(dict(date=dates))
    merged = merged.set_index('date')
    for k,df in totals.items():
        df.index = sc.date(df.index.to_list())
        merged = pd.concat([merged, df], axis=1)
    
    m = merged.reset_index()
    inds = sc.findinds((merged.index >= sc.date('2021-05-01')) * (merged.index <= sc.date('2022-05-01')))
    final = sc.dataframe(dict(
        date                 = m['index'],
        new_diagnoses        = m.Cases,
        new_known_deaths     = m.Deaths,
        new_hospitalizations = m.Hospitalizations,
        dose1                = m.Dose1,
        dose2                = m.Dose2,
        booster1             = m.First_booster,
        booster2             = m.Second_booster,
    ))
    final = final.iloc[inds,:]
    final = final.reset_index(drop=True)
    
    sc.heading('Calculate population sizes...')
    popsizes = sc.odict()
    provs = dfs.cases.Province.unique()
    for prov in provs:
        mapping = {
            'TP Ho Chi Minh': 'Ho Chi Minh City',
            'Ba Ria Vung Tau': 'Ba Ria-Vung Tau',
            }
        if prov in mapping:
            prov = mapping[prov]
        thispop = pop.Population[sc.findinds(pop.Province == prov)].values[0]
        popsizes[prov] = thispop
    popsizes['total'] = popsizes[:].sum()
    
    if do_save:
        final.to_csv(outfile)
        sc.savejson(popout, popsizes)
        
    if do_plot:
        sc.options(dpi=150)
        fig = pl.figure(figsize=(10,8))
        nrows,ncols = sc.getrowscols(len(final.columns))
        for c,col in enumerate(final.columns):
            if col != 'date':
                pl.subplot(nrows, ncols, c)
                pl.plot(final.date, final[col])
                pl.title(col)
                sc.dateformatter()
        sc.figlayout()
        pl.show()
    
    T.toc('Done')