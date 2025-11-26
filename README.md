
# Emergent Mind Observatory (EMO) v0.1

**Tagline**  
A missing layer above Earth dashboards: existing tools track planetary health,  
but not whether our *species-level cognition* is functioning.  
**EMO v0.1** is the first working instrument for that gap.

---

## What this repo is

EMO v0.1 is a **planetary cognition dashboard prototype**.  
It computes five UIA-aligned “vital signs” for humanity as an emergent mind:

1. **Organismality Index (OI)**  
   Are we behaving more like a coherent organism (cooperation)  
   or a fragmented swarm (conflict)?

2. **Synergy / O-information (SΦ)**  
   How integrative are our information streams (news, search, science)?

3. **Global Workspace Ignition (GWI)**  
   When does the global mind “light up” around a topic?

4. **Self-Model Fidelity (SMF)**  
   How tightly are climate self-models (budgets, pathways)  
   coupled to actual emissions and budgets?

5. **Information-time (τ_I)**  
   How fast is our predictive capacity clock ticking, relative to calendar time?

All of this is implemented in **pure Python**, using **open data** and simple metrics,
so funders, collaborators, and institutions can run and extend the prototype easily.

Concepts and metric definitions follow the **EMO** and **UIA** v2 drafts  
(*The Emergent Mind Observatory* and *The Universal Interface Action*).

---

## Repository layout

The target layout is:

```text
emo_v01/
  README.md
  STATE_OF_THE_EMERGENT_MIND_2025.md
  requirements.txt

  emo/
    __init__.py
    config.py
    data_sources.py
    organismality.py
    synergy.py
    gwi.py
    smf.py
    info_time.py
    utils.py

  data/
    ecmwf_headline_scores.csv    # optional stub for forecast-skill time series

  main.py

  notebooks/
    emo_v01_climate_demo.ipynb   # optional notebook for plots / demos
