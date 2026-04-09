#%%
from laundromatic.models import drying_progress_for_hour

for T in [5, 10, 15, 20]:
    progress = drying_progress_for_hour(T, humidity_pct=60)
    print(T, progress)
# %%
