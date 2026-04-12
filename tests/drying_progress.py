#%%
from laundromatic.core import drying_progress_for_hour

#%%
for T in [-5, 5, 10, 15, 20]:
    progress = drying_progress_for_hour(T, humidity_pct=60)
    print(T, progress)

#%%
for RH in [40, 60, 80, 95, 100]:
    progress = drying_progress_for_hour(20, RH)
    print(RH, progress)

#%%
progress = drying_progress_for_hour(20, 70)
print(progress)
# %%
