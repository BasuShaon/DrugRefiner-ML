# %% filepath and dependencies
###################################################################################
###################################################################################
###################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import sys
import importlib
import re
import importlib
sys.path.append(os.path.join(os.path.dirname(__file__)))
import device_summarystatistics

# %%

path = os.path.dirname(__file__) d

data_path = os.path.join(path, '..', 'data')

fig_path = os.path.join(path, '..', 'figures')

# %%
# %% Glu_gal data for 381 (Figure 3)

galactose = pd.read_excel(os.path.join(data_path, 'Figure3_Compound1_Galactose_250204a.xlsx'))

galactose.index = [10, 5, 1, 0.5, 0.25, 0]

galactose.drop(galactose.columns[0], axis = 1, inplace = True) # drop not category column 

norm = galactose / galactose.iloc[-1]

# Calculate mean and standard deviation for error bars
normsum = norm.assign(
    glu_mean=norm.iloc[:, 0:3].mean(axis=1),
    glu_std=norm.iloc[:, 0:3].std(axis=1),
    gal_mean=norm.iloc[:, 3:6].mean(axis=1),
    gal_std=norm.iloc[:, 3:6].std(axis=1)
)

# Plot
plt.figure(figsize=(6, 4))

# Plot mean trend lines with error bars
plt.errorbar(normsum.index, normsum["glu_mean"], yerr=normsum["glu_std"], fmt="o-", label="Glucose Mean", capsize=3, linestyle = '--')
plt.errorbar(normsum.index, normsum["gal_mean"], yerr=normsum["gal_std"], fmt="s-", label="Galactose Mean", capsize=3, linestyle = '--')
plt.plot(norm.index, normsum.iloc[:,3:6], color = 'orange', alpha = 0.5)
plt.plot(norm.index, normsum.iloc[:,0:3], color = 'lightblue', alpha = 0.5)

# Formatting
plt.savefig(os.path.join(fig_path,'Compound1_glugal_250204a.pdf'))
plt.show()

# Reload
importlib.reload(device_summarystatistics)

# used data normalized to 0 micromolar
real = norm.copy()

#remove normalizing measurement
real = norm.drop([0.00])

#log transform drug concentration
real.index = np.log10(real.index)

# extract column wise IC50s using linear model 
ic50_values = device_summarystatistics.linear_IC50(real)

# clean up data for t-test
ic50_df = pd.DataFrame({'Glucose': ic50_values[0:3].values,
                            'Galactose': ic50_values[3:6].values}, 
                            index = ['rep1', 'rep2', 'rep3'])

# perform t-test (welch, independent)
device_summarystatistics.t_test(ic50_df['Glucose'], ic50_df['Galactose'])

# unlog IC50
print(10**(ic50_df.mean()))

# %% Seahorse at max resp (Figure 3)
seahorse = pd.read_excel(os.path.join(data_path, 'Figure3_Compound1_Seahorse_250204a.xlsx'))

device_summarystatistics.t_test(pd.concat([seahorse['Enza '],seahorse['Control']]), seahorse['Compound 1'])

plt.figure(figsize=(1.5,3))
sns.boxplot(seahorse, order = ['Control','Enza ', 'Compound 1'])
sns.swarmplot(seahorse, color = 'black')
plt.savefig(os.path.join(fig_path, 'Fig3_seahosemax.pdf'))

# %% Complex II data for all (Figure 3 and Figure 4)

complex2 = pd.read_excel(os.path.join(data_path, 'Figure3_all_Complex2_250204a.xlsx'), index_col = 0)

# Reload
importlib.reload(device_summarystatistics)

device_summarystatistics.one_test(complex2.loc['AZ14183816'], 100)

device_summarystatistics.one_test(pd.Series(complex2.loc[['AZ14197166', 'AZ14183816']].values.flatten()), 100)

plot_list = ['AZ14183816', 'AZ14196658','AZ14197166','DMSO']

complex2.loc[plot_list].T.mean().plot(kind = 'bar', 
    yerr = complex2.loc[plot_list].T.std())
plt.savefig(os.path.join(fig_path, 'complexII_all_fig4.pdf'))

# %% Complex I data (Figure 4)
importlib.reload(device_summarystatistics)

# import data
complex1 = pd.read_excel(os.path.join(data_path, 'Figure3_Complex1_250219a.xlsx'), index_col = 0)
# numerize to log10index
complex1.index = np.log10([0,20,5,1,0.1,0.05,0.01,0.005])
# bring down to decimal percent
complex1 = complex1/100
# drop DMSO
complex1 = complex1.iloc[1:]
# calculate log10IC50 down reps
ic50_values = device_summarystatistics.linear_IC50(complex1)
# t-test on the log10IC50s
device_summarystatistics.t_test(ic50_values.iloc[0:3], ic50_values.iloc[6:9])
# exponentiate to IC50
print((10**ic50_values.iloc[0:3]).mean())

print((10**ic50_values.iloc[6:9]).mean())

10**8.0281
# %% Complex I data (Figure 4)
importlib.reload(device_summarystatistics)
# import data
complex1 = pd.read_excel(os.path.join(data_path, 'Figure4_Complex1_250207a.xlsx'), index_col = 0)
# numerize to log10index
complex1.index = np.log10(complex1.index)
# bring down to decimal percenet
complex1 = complex1/100
# calculate log10IC50 down reps
ic50_values = device_summarystatistics.linear_IC50(complex1)
# t-test on the log10IC50s
device_summarystatistics.t_test(ic50_values.iloc[0:3], ic50_values.iloc[3:6])

device_summarystatistics.t_test(ic50_values.iloc[0:3], ic50_values.iloc[6:9])

device_summarystatistics.t_test(ic50_values.iloc[0:3], ic50_values.iloc[3:9])
# exponentiate to IC50
print((10**ic50_values.iloc[0:3]).mean())

print((10**ic50_values.iloc[3:9]).mean())

# %%

# %% primary HCC data (Figure 4)

HCC = pd.read_excel(os.path.join(data_path, 'Figure4_HCC_250208a.xlsx'), index_col = 0)

HCC = HCC.loc[~HCC.index.isna()]

HCC2 = HCC.assign(conc = np.log10(HCC.index))

#HCC2.conc.replace(-np.inf, -10, inplace = True)

HCC2 = HCC2.iloc[1:HCC2.shape[0]]

HCC2.set_index('conc', inplace = True)

# extract column wise IC50s using linear model 
HCC_values = device_summarystatistics.linear_IC50(HCC2)

# clean up data for t-test
ic50_df = pd.DataFrame({'Compound 1': ic50_values[0:3].values,
                            'Compound 2': ic50_values[3:6].values, 
                            'Compound 3': ic50_values[6:9].values}, 
                            index = ['rep1', 'rep2', 'rep3'])

# get IC50 values unlogged
ic50s = (10**ic50_df).mean()

# %% cell panel (Figure 4)

panel = pd.read_excel(
                os.path.join(data_path, 'Figure4_CellPanel_250207a.xlsx'),
                index_col = 0).T

panel['Compound'] = ['1', '1', '1', '1',
                    '2', '2', '2', '2',
                    '3', '3', '3', '3',
                    'Enz', 'Enz', 'Enz', 'Enz']

panel = panel.loc[panel['Compound']!='Enz']

panel_long=panel.melt(id_vars=['Compound'], var_name =  'Cell', value_name='Value')


# Plot the nested boxplot
plt.figure(figsize=(4,3.5))
sns.boxplot(x='Cell', y='Value', hue='Compound', data=panel_long, palette='Set2')
# Customization
plt.axhline(-4.5, linestyle = '--', color = 'black')
plt.xlabel('Cell Line')
plt.ylabel('Measurement Value')
plt.legend(title='Condition')
plt.savefig(os.path.join(fig_path, 'HCC_lines.pdf'))
plt.show()

# %%

panel = panel.assign(
                factor = pd.Index(panel.index).str.replace(
                r'[.\d]', '', regex=True))

panel = panel.loc[panel['factor']!='Enzalutamide']

ARpos = panel[panel.columns[0:2]]

ARneg = panel[panel.columns[2:panel.shape[1]-2]]

device_summarystatistics.t_test(pd.Series(ARpos.values.flatten()),
                pd.Series(ARneg.values.flatten()))


ARneg_stat = ARneg.assign(
    factor = ['Comppound 1', 'Compound 1', 'Compound 1', 'Compound 1','Analogue', 'Analogue', 'Analogue', 'Analogue', 'Analogue', 'Analogue','Analogue','Analogue'])


device_summarystatistics.t_test(pd.Series(ARneg_stat.loc[ARneg_stat['factor']!= 'Analogue'].iloc[:,0:3].values.flatten()),
                pd.Series(ARneg_stat.loc[ARneg_stat['factor']== 'Analogue'].iloc[:,0:3].values.flatten()))

# %% xenograft AR degradation (Figure 4)

importlib.reload(device_summarystatistics)

degron = pd.read_excel(
                os.path.join(data_path, 'Figure4_XenoGraftARdeg_250207a.xlsx'))

device_summarystatistics.t_test(degron['Vehicle'], degron['Compound 3'])

plt.figure(figsize = [1,3])
sns.boxplot(degron)
sns.swarmplot(degron, color = 'black')
plt.axhline(device_summarystatistics.geometric_mean(degron['Vehicle']), 
    color = 'red', linestyle = '--')
plt.axhline(device_summarystatistics.geometric_mean(degron['Compound 3']), 
    color = 'red', linestyle = '--')
plt.savefig(os.path.join(fig_path, 'Figure4_xenograft_ARdeg.pdf'))

