# TGDK - Memorychain
### NEETs by TGDK - Kuberneets for Mobius Folded Memory

**LICENSE: BFE-TGDK-022ST | Holder: Sean Tichenor | (c) TGDK 2026**
**Repo: https://github.com/OliviaAI-TGDK/TGDK**

> Memory chain folding on top and through itself. 4 Duo-Corrugations on 3 Phi Lattices + 1 Pi Lattice.

---

## What is TGDK?

TGDK is a mobius-folded memory chain with concurrent policy ratio clipping (0.8 - 1.2). When the chain length hits 8, 16, 32... you don't just add a block, you fold the chain through itself and seal a knot.

**Core equation:**
```
MobiusHash = Keccak256(Head.Data + Tail.Data)
Inverted = true when count % 8 == 0
```

**Build:**
```bash
tcc tgdk-neets-final.c -o neets -lpthread -lm
./neets
```

---

## NEETs by TGDK

NEETs = Node Elastic Entity Transport System. Kubernetes for memory.

```
neets get nodes
NAME    LATTICE  FACTOR     STATUS
phi-0   phi      1.6180     Ready
phi-1   phi      1.6180     Ready
phi-2   phi      1.6180     Ready
pi-0    pi       3.1415     Ready

neets apply -f deployment.yaml
[NEETs pod: duo-phi-0 | node: phi-0] iter 00 ratio 1.043 clipped 1.043
>>> [TGDK KNOT SEALED] Block 8 | MobiusHash a3f2c1... | Inverted=1
```

**4 Duo-Corrugation Workers:**
- 3x phi workers - golden expansion `real_size *= PHI`
- 1x pi worker - circular sin/cos deformation + knot sealer
- Duo pass: forward + backward inverted (mobius dex)

---

## t# by TGDK - The Compiler

Replace gcc with t#.

```bash
# Install
chmod +x tcc-compiler.sh tsharp-compiler.sh
sudo cp tcc-compiler.sh /usr/local/bin/tcc
sudo cp tsharp-compiler.sh /usr/local/bin/tsharp

# Use
tcc tgdk-neets-final.c -o neets
tsharp dimfo.t

# Alias gcc
alias gcc="tcc"
```

`tcc` auto-detects TGDK builds and applies:
```
-lpthread -lm -O2 -DMARA_FACTOR=1.6180339887 -DPHI_LATTICE -DPI_LATTICE -DNEETS_ENABLED
```

---

## dimfo.t - Dimensional Foundation Engine v0.3

**Core lattice:**
```
1 × 244 × 48833 × 66440 = 791,649,342,880 foundation space
```

**Foundation equation:**
```
XYJR((π^144 × 9)/(7×4×3×1×(0.0102+0.98))) × 3^3.2
```

### Extensions

**1. Snellineated Offsets - 3 sets × 9 = 27 folds**
Snell law: `n1*sinθ1 = n2*sinθ2` with `n2 = PHI = 1.618`
- Set 0: phi-0 lattice offsets
- Set 1: phi-1 lattice offsets
- Set 2: phi-2 lattice offsets
- Pi-0 uses combined refraction for sealing

```python
theta1_deg = (i * 10) + (set_idx * 3.33)
sin_theta2 = (n1/n2) * sin(theta1)
offset = base * (theta1-theta2) * PHI^(set+1) * 0.0001
```

**2. Hookean Derivatives - 21 strain derivatives**
`F = -k*x` where `k = PHI`, `x = magnitude / 1e9`

- Order 0: displacement
- Order 1: stiffness
- Order 2: curvature
- Order 3-8: jerk, snap, crackle, pop, lock, drop
- Order 9-20: hookean_n
- Orders 18-20 seal on pi-0 lattice
- All clipped to 0.8-1.2 for NEETs stability

```bash
./dimfo.t
# or
tsharp dimfo.t
```

Output:
```json
{
  "foundation": {"axis_0": 1, "axis_1": 244, "axis_2": 48833, "axis_3": 66440},
  "space": 791649342880,
  "snellineated_offsets": {"total": 27, "sets": [...]},
  "hookean_derivatives": {"total": 21, "derivatives": [...]}
}
```

---

## Repo Structure

```
TGDK/
├── core/
│   ├── memory.c       # snell_memory_allocate with MARA factor
│   ├── lattice.c      # phi[3] + pi[1] lattices
│   └── duo.c          # duo-corrugation workers
├── tgdk-neets-final.c           # combined C build (v1)
├── tgdk-neets-final-v2-dimfo.c  # combined + dimfo.t integrated (v2)
├── dimfo.t                      # Dimensional Foundation Engine v0.3 (tsharp)
├── neets.t                      # NEETs orchestration
├── tgdk.t                       # TGDK chain
├── tsharp.t                     # tsharp compiler spec
├── tcc / tcc_compiler.sh        # t# compiler
├── tsharp / tsharp_compiler.sh  # tsharp wrapper
└── neets-deployment.yaml        # k8s-like deployment for NEETs
```

---

## Quick Start

```bash
git clone https://github.com/OliviaAI-TGDK/TGDK.git
cd TGDK

# Build NEETs
tcc tgdk-neets-final-v2-dimfo.c -o neets -lpthread -lm

# Run dimensional foundation
python3 dimfo.t

# Or run full cluster with dimfo integrated
./neets

# Expected:
# [dimfo.t] Initializing Dimensional Foundation 1 x 244 x 48833 x 66440 = 791649342880
# [dimfo.t] 27 snellineated offsets sealed (3x9) | 21 hookean derivatives sealed
# ========== NEETs CLUSTER SEALED ==========
# 3 Phi Lattices: 8, 8, 8 blocks [Sealed]
# 1 Pi Lattice: 8 blocks [Sealed]
```

---

## Policy Clipping

All policy ratios enforced 0.8 - 1.2 like PPO/GRPO:

```c
double ratio = pi_theta / pi_old;
double clipped = fmax(0.8, fmin(1.2, ratio));
```

Applies to:
- Duo-corrugation workers
- Hookean derivatives
- Snell refractive deviation

---

## Website

Live NEETs docs: [NEETs by TGDK Site](./site) (generated artifact)

Includes phi/pi visualization, terminal, downloads.

---

## License

**BFE-TGDK-022ST** - Proprietary. Holder: Sean Tichenor. © TGDK 2026. All rights reserved.

No redistribution without authorization. This repo is the memorychain reference implementation.

---

**Built with t# by TGDK - the compiler that folds memory through itself.**
