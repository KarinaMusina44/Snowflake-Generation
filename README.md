# Snowflake Modeling & Generation

Numerical simulation to generate synthetic snowflakes and study how model parameters shape their morphology.



https://github.com/user-attachments/assets/f40a41bf-9ccb-44b5-879d-89a01f9cdb39




## Goals

- Generate snowflakes with a physically motivated model.
- Analyze how parameters affect the resulting shapes (plates, dendrites, facets).
- Discuss stability, complexity, and model limitations.

## Project Scope

- **Level:** 1st MEng year  
- **Period:** **January 2023**  
- **Course:** Modeling  
- **Team:** Noé Bertramo, Théophile Donato, Karina Musina


## Method & Models

### Continuous-state model (used)

- 2D **hexagonal** lattice; each cell stores three quantities:  
  **b** (quasi-liquid water), **c** (ice), **d** (vapor).
- Each iteration applies four stages:
  1) **Diffusion** of vapor (**d**)
  2) **Freezing** (part of **d** converts into **b** and **c** at the boundary)
  3) **Attachment** (cells join the crystal based on neighbor count and thresholds)
  4) **Melting** (a fraction of **b**/**c** returns to **d** at the boundary)
- Implemented in **Python** with **Pygame** for real-time visualization.

### Algorithm (high-level)

1. **Diffusion:** local averaging of **d** for non-flake cells.  

2. **Freezing** (on the boundary):  
   $$
   b \leftarrow b + (1-\kappa)\,d,\quad
   c \leftarrow c + \kappa\,d,\quad
   d \leftarrow 0
   $$

3. **Attachment** (based on number of flake neighbors \(n\)):
   - $n \in \{1,2\}$: attach if $b \ge \beta$
   - \( n = 3 \): attach if \( b \ge \alpha \) and an additional condition on \( d \) (threshold \( \theta \))
   - \( n \ge 4 \): attach automatically

4. **Melting** (new boundary cells):  
   $$
   b \leftarrow (1-\mu)\,b,\quad
   c \leftarrow (1-\gamma)\,c,\quad
   d \leftarrow d + \mu\,b + \gamma\,c
   $$

### Key assumptions

- **2D** growth on a **hexagonal** lattice.  
- **Locally homogeneous** environment (flake \( \ll \) cloud).  
- No global refreezing of the entire crystal (only partial boundary melting).  
- **Discrete time**; local linear stability considered.


## Parameters & qualitative effects

- **\( \rho \)** — vapor density / supersaturation:  
  higher \( \rho \) ⇒ faster growth and more **dendritic** patterns.
- **\( \beta \)** — attachment threshold at **tips** (1–2 neighbors):  
  lower \( \beta \) ⇒ faster tip elongation.
- **\( \mu \)** — **melting** intensity of quasi-liquid water:
  
## References
- Gravner, J., & Griffeath, D. — Modeling Snow Crystal Growth II: A Mesoscopic Lattice Map with Plausible Dynamics.
- Li, J. — On the Geometry and Mathematical Modelling of Snowflakes and Viruses.
