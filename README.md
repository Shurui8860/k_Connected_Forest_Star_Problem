# The $\kappa$-Connected Arborescence–Star Problem

**Formulation and Branch-and-Cut Implementation**

This repository provides a reference implementation for the **$\kappa$-connected Arborescence–Star Problem** on directed graphs. It includes: 

(i) data generation utilities, 

(ii) a mixed-integer programming (MIP) model constructed in DOCplex, 

(iii) CPLEX callback routines for branch-and-cut (lazy and user cuts), and 

(iv) a NetworkX/Matplotlib visualizer for solutions. 

Intuitively, given a directed graph with a designated set of roots $\mathcal{R}$ and customer vertices $\mathcal{V}$, the goal is to select an arborescence-like backbone (a union of rooted directed trees) and to either place customers on the backbone or assign them to backbone vertices, while enforcing **$\kappa$-connectivity**: each backbone vertex must admit at least $\kappa$ pairwise edge-disjoint directed paths from distinct roots. The model internalizes a cost trade-off between building backbone arcs and assigning customers.

![](example.png)

---

## Repository Layout

```
.
├─ main.py          # Entry point: data generation → model build → callbacks → solve → plot
├─ data.py          # Data utilities: random coordinates, arc sets, cost matrices
├─ model.py         # MIP model (DOCplex): variables, objective, constraints
├─ callback.py      # CPLEX callbacks: lazy cuts, user cuts, incumbent logging
├─ plot.py          # Visualization (NetworkX + Matplotlib)
├─ example.png      # Sample output figure
├─ The_kappa_connected_Arborescence_Star_Problem__Formulation_and_Branch_and_Cut_Algorithm.pdf
└─ README.md
```

---

## Requirements and Installation

### Prerequisites

* **Python** ≥ 3.8
* **IBM ILOG CPLEX Optimization Studio** (with a valid license)
* Python packages: `cplex` (the solver’s Python API), `docplex`, `numpy`, `networkx`, `matplotlib`

> **Note.** `docplex` is only the modeling layer. A local CPLEX installation is required to run the MIP with callbacks.

### Suggested Conda Environment

```bash
conda create -n kfsp python=3.10 -y
conda activate kfsp
pip install numpy networkx matplotlib docplex
```

---

## Quick Start

1. **Configure instance parameters** (optional)
   Open `main.py` and adjust the default parameters, for example:

   ```python
   num_of_roots, num_of_customers = 3, 24
   k, const, seed = 3, 2, 0        # κ (connectivity), assignment-cost factor, RNG seed
   p.create_data(const=const, seed=seed, width=100)
   ```

   * `const=None` makes assignment costs proportional to arc costs (e.g., $a = k\cdot c$);
     otherwise ($a = \texttt{const}\cdot c$).

2. **Solve and visualize**

   ```bash
   python main.py
   ```

   The script prints solver progress and objective values, then renders a solution plot.

---

## Input Model and Parameters

* **Graph construction.** `data.py` samples vertex coordinates and builds a directed graph (complete or sparsified, depending on the routine), together with:

  * arc cost matrix $c_{ij}$ (backbone construction cost),
  * assignment cost matrix $a_{ij}$ (assigning customer $j$ to backbone vertex $i$).

* **Key parameters.**

  * `num_of_roots = |R|` — number of root (supply) vertices.
  * `num_of_customers = |V|` — number of customer vertices.
  * `k` — κ-connectivity requirement (edge-disjoint root-to-vertex paths from **distinct** roots).
  * `const` — assignment-to-arc cost scaling (see above).
  * `seed`, `width` — randomness and geometric scaling for instance generation.

---

## Optimization Model 

### Decision variables

* $x_{ij}\in{0,1}$ for $(i,j)\in A$: arc $(i,j)$ is selected in the backbone.
* $y_{ij}\in{0,1}$ for $i\in V,\ j\in C$: customer $j$ is assigned to (served by) backbone vertex (i).
* $w_i\in{0,1}$ for $i\in V$: vertex $i$ lies on the backbone (is “opened/kept” in the arborescence union).

> Intuition: $x$ builds the directed forest, $w$ indicates which vertices actually belong to that forest, and $y$ lets customers that are not on the forest be attached to some backbone vertex.



### Objective

$$
\min \sum_{(i,j)} c_{ij},x_{ij} ;+; \sum_{(i,j)} a_{ij},y_{ij}.
$$


### Structural constraints

**(C1) Root activation:** All roots must belong to the backbone; they are the supply/entry points for connectivity.

$$
w_r = 1 \qquad \forall r\in R.
$$

**(C2) In–degree of non-roots:** A non-root vertex is either *outside* the backbone ($w_v=0$, then it has no entering backbone arc) or *in* the backbone ($w_v=1$), in which case it must have **exactly one** entering arc—this is the arborescence rule that avoids branching into a node.

$$
\sum_{i \in V:\ (i,v)\in A} x_{iv} = w_v \qquad \forall v \in V \setminus R.
$$

**(C3) In–degree of roots**: Roots have no predecessors in an arborescence.

$$
\sum_{i\in V:\ (i,r)\in A} x_{ir} = 0 \qquad \forall r\in R.
$$

**(C4) Outgoing arcs only from backbone vertices:** If a vertex is not on the backbone $w_v=0$, it cannot send backbone arcs; if it is on the backbone, any subset up to its out-degree is allowed. (Any equivalent big-(M) linking is acceptable; this one uses $\deg^{+}(v))$ as a tight (M).)

$$
\sum_{j\in V:\ (v,j)\in A} x_{vj} ;\le; \deg^{+}(v), w_v \qquad \forall v\in V.
$$

**(C5) No 2-cycles:** Two opposite arcs between a pair would form a directed 2-cycle and violate the tree-like structure.

$$
x_{ij}+x_{ji}\le 1 \qquad \forall {i,j}\subseteq V,\ (i,j)\in A,\ (j,i)\in A.
$$


> Remarks. (C2)–(C5) together with the connectivity cuts below rule out all directed cycles not containing a root. If a cycle appears, it would create a subset (S) with no entering arc from outside, violating the cut in (K-Cuts).
* **Structural constraints** (implemented in `model.py`):

  * Root designation and arborescence-style in-degree controls for non-roots.
  * Compatibility: assignments allowed only to backbone vertices.
  * Prohibitions on trivial symmetric 2-cycles, and additional linking logic between (x), (y), (w).

* **κ-connectivity constraints** (separated as lazy cuts in `callback.py`):
  For any subset (S\subseteq V) and for each demand configuration, enforce that the number of arcs leaving (S) is sufficiently large to guarantee κ edge-disjoint root-to-(S) connectivity from distinct roots. In practice, violated cuts are identified via min-cut routines on appropriately constructed auxiliary networks and added on the fly as **lazy constraints** (and, when helpful, as **user cuts**).

This separation scheme follows the standard branch-and-cut paradigm: solve relaxations, detect violations, add cuts, and continue until convergence.

Great—here is a precise list of the **decision variables, objective, and explicit constraints**, each followed by an **intuitive explanation**. The notation matches a directed graph (G=(V,A)) with roots (R\subseteq V) and customers (C:=V\setminus R). Costs (c_{ij}\ge 0) (building a backbone arc) and (a_{ij}\ge 0) (assigning customer (j) to backbone vertex (i)) are given.






---

## Assignment constraints

**(A1) Each customer is either on the backbone or assigned exactly once**
[
w_j + \sum_{i\in V} y_{ij} = 1 \qquad \forall j\in C.
]
**Why:** A customer is served either by being a backbone vertex itself or by being attached to exactly one backbone vertex.

**(A2) Assignment only to backbone vertices**
[
y_{ij} \le w_i \qquad \forall i\in V,\ \forall j\in C.
]
**Why:** You can only assign a customer to a vertex that actually exists on the backbone.

*(Optional, if desired)* **(A3) Forbid self-assignment unless on backbone**
This is already enforced by (A1)–(A2): if (y_{jj}=1) then (w_j=1). If you prefer to rule out (y_{jj}) explicitly, add (y_{jj}\le w_j) (redundant) or fix (y_{jj}=0) for modeling taste.

---

## κ-connectivity cuts (branch-and-cut)

Let (\kappa\in\mathbb{Z}_{\ge 1}) be the required **edge-disjoint** connectivity from **distinct roots** to every backbone vertex. Using max-flow/min-cut arguments, for each *terminal* vertex (v\in V\setminus R) and each subset (S\subseteq V) with (v\in S), we must have enough backbone arcs entering (S) from outside to support (\kappa) disjoint root-to-(v) paths, after accounting for the number of roots already inside (S).

Define (\delta^{-}(S):={(i,j)\in A:\ i\notin S,\ j\in S}). Then:

**(K-Cuts) Node-based κ-root connectivity**
[
\sum_{(i,j)\in \delta^{-}(S)} x_{ij} ;;\ge;; \max{0,\ \kappa - |S\cap R|},, w_v
\qquad \forall v\in V\setminus R,\ \forall S\subseteq V \text{ with } v\in S.
]

**Why (intuition):**

* If **no root** lies in (S) ((|S\cap R|=0)), then at least (\kappa) backbone arcs must cross **into** (S). Otherwise, you cannot route (\kappa) edge-disjoint paths from distinct roots outside (S) to reach (v\in S).
* If (t:=|S\cap R|>0), then at most (t) of the required (\kappa) paths can start **inside** (S). The remainder (\kappa-t) must enter from outside; thus the right-hand side becomes (\kappa-t).
* The factor (w_v) deactivates the constraint when (v) is not on the backbone ((w_v=0)): non-backbone customers do not need κ-connectivity because they are served via assignment.
* Enforcing (K-Cuts) for **all** (S) is exponential; therefore, they are separated on-the-fly using min-cut routines in a **lazy-constraint** (and optionally **user-cut**) callback.

> Practical separation: For each candidate backbone vertex (v) with (w_v>0) in the current relaxation/solution, build an auxiliary network with unit capacities on selected backbone arcs, add root super-sources with capacities reflecting “distinct roots,” and compute a min-cut that either certifies feasibility (value (\ge \kappa)) or yields a violated set (S) to cut.

---

## Optional strengthening (if present in your codebase)

* **Root–outflow lower bounds.** One may enforce that each root has at least one outgoing backbone arc when a demand requires it (this is usually implied by (K-Cuts), but explicit lower bounds can tighten the root node relaxations).
* **Assignment-aware cuts.** If your variant requires that assigned customers inherit κ-robust reachability to their *host* (i), you can enforce (K-Cuts) only for vertices with positive inbound assignment or add:
  [
  \sum_{(p,q)\in \delta^{-}(S)} x_{pq} ;\ge; \max{0,\ \kappa - |S\cap R|}, \sum_{i\in S} y_{i j}
  \quad \forall j\in C,\ \forall S\subseteq V,
  ]
  which demands κ-robust access into any subset (S) that contains the hosting vertex of customer (j). (Use with care; it is stronger and costlier to separate.)

---

## What these constraints collectively guarantee

* **Tree-like backbone:** (C2)–(C5) enforce a union of rooted arborescences without directed cycles and with exactly one entering arc per non-root backbone node.
* **Service completeness:** (A1)–(A2) ensure every customer is served exactly once—either on the backbone or by attachment to a backbone vertex.
* **Robust reachability:** (K-Cuts) guarantee, for each backbone vertex, the existence of (\kappa) edge-disjoint directed paths from **distinct roots**, thus providing survivability to up to (\kappa-1) arc failures (under standard edge-disjoint path interpretations).

If you’d like, I can also provide the exact separation pseudocode for (K-Cuts) (single-commodity min-cut per terminal (v)) and a compact **LP relaxation** annotated with which constraints are added as lazy cuts versus static rows.

---

## Visualization

`plot.py` renders the optimized backbone and assignments:

* **Roots** are displayed in red.
* **Backbone vertices** and **assigned customers** are distinguished by color/shape.
* **Black arcs** show selected backbone/assignment arcs, following the optimized (x) and (y).

You may also call the routine directly from Python:

```python
from plot import plot_graph
plot_graph(data_obj, model_obj)
```

---

## Reproducibility and Scaling Tips

* Fix `seed` to reproduce a specific instance.
* Increase `const` to bias the solution toward assignments (smaller backbone).
* Reduce `num_of_customers` or `k` for faster runs; κ-connectivity substantially tightens the problem.
* Solver performance is sensitive to the sparsity of the candidate arc set; consider pruning long arcs when experimenting with larger instances.

---

