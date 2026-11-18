# Robot simulation & legged locomotion: claims, sources, evidence

A table of **what upstream projects actually claim** about simulation throughput, training time and sim-to-real —
with the hardware, the version and the link, and an honest column saying whether anyone has reproduced it.

This is a curation repo. **None of the numbers in the tables below are mine.** They are quoted from papers and
repositories, and every row carries the label `UPSTREAM` until a third party repeats the measurement.
My own measurements live in [sim-throughput-benchmark](https://github.com/cccjj55/sim-throughput-benchmark)
and are labelled `MEASURED`.

Why bother: the field is full of "10× faster" with no baseline, no hardware and no version. A claim you can't
trace is a claim you can't use in a design review. This repo keeps the traceable ones in one place and marks
the rest as unverified.

---

## How to read a row

| label | meaning |
| --- | --- |
| `UPSTREAM` | quoted from the project's paper or README; nobody independent has repeated it |
| `3P` | reproduced by a third party, with their hardware and version recorded |
| `MEASURED` | measured by a maintainer of this repo, with the artifact committed |

A row without a hardware field is not a row. A "faster" without a baseline is not a claim.

---

## 1. Parallel simulation: what the sources say

| engine | task | claim (as published) | hardware in the source | source | label |
| --- | --- | --- | --- | --- | --- |
| Isaac Gym | ANYmal locomotion (PPO) | flat terrain trained **under 4 min**, uneven terrain **~20 min** | single workstation GPU (source does not pin the model) | Rudin et al., CoRL 2021, [arXiv:2109.11978](https://arxiv.org/abs/2109.11978) | `UPSTREAM` |
| Isaac Gym | general RL training | **2–3 orders of magnitude** faster than CPU-sim + GPU-network setups | single GPU | Makoviychuk et al., [arXiv:2108.10470](https://arxiv.org/abs/2108.10470) | `UPSTREAM` |
| MuJoCo Playground (MJX) | quadrupeds, humanoids, hands, arms | "train policies **in minutes** on a single GPU", zero-shot sim-to-real | single GPU (model not pinned in the abstract) | Zakka et al., [arXiv:2502.08844](https://arxiv.org/abs/2502.08844) | `UPSTREAM` |
| MuJoCo / MJX (cart-pole) | throughput microbenchmark | MuJoCo CPU **212k** env-steps/s; MJX on CPU **522k** at 64 envs; MJX scales with env count, the Python loop does not | RTX 5070 Ti Laptop 12 GB, WSL2, 24 cores | [sim-throughput-benchmark](https://github.com/cccjj55/sim-throughput-benchmark) | `MEASURED` |

Two things this table already shows, without running anything:

1. **"Minutes" claims are about a specific task on a specific GPU.** None of the abstracts pin the GPU model,
   which is exactly why the numbers are hard to reuse.
2. **The bottleneck is not always the physics.** In my own cart-pole run, the CPU baseline was flat from 8 to 64
   environments (209k → 212k env-steps/s) while MJX grew 1.5×–2.5× — the Python loop, not the integrator,
   was the limit. A GPU claim measured against a Python loop says little about the GPU.

---

## 2. Engines, and what each is actually good at

| engine | model | best at | watch out |
| --- | --- | --- | --- |
| [MuJoCo](https://github.com/google-deepmind/mujoco) / [MJX](https://github.com/google-deepmind/mujoco/tree/main/mjx) | CPU / JAX-on-GPU | contact-rich manipulation, fast single-env iteration, MJX for batched training | MJX recompiles per shape change; not a drop-in for large scenes |
| [Isaac Sim](https://github.com/isaac-sim/IsaacSim) / [Isaac Lab](https://github.com/isaac-sim/IsaacLab) | PhysX 5 on GPU | photoreal sensors, thousands of envs, legged RL at scale | install weight, GPU memory, version churn |
| [Gazebo](https://github.com/gazebosim/gz-sim) (Harmonic/Ionic) | ODE/DART/Bullet | ROS integration, sensor plugins, reproducible CI worlds | throughput per env is low; not built for 10k envs |
| [Brax](https://github.com/google/brax) | JAX | differentiable / batched RL research | model authoring is MJCF/URDF-adjacent, ecosystem smaller |
| [Genesis](https://github.com/Genesis-Embodied-AI/Genesis) | custom | very fast claims, broad feature list | young project; treat performance claims as unverified until versioned |
| [PyBullet](https://github.com/bulletphysics/bullet3) | CPU | quick scripts, education, legacy benchmark suites | no long-term roadmap |
| [Drake](https://github.com/RobotLocomotion/drake) | CPU | contact mechanics, optimization-based control, verification | not a throughput play |

---

## 3. Quadruped locomotion and navigation simulation

Starting points that are actually runnable, in the order I would read them.

**Training a gait**

| resource | what it gives you | note |
| --- | --- | --- |
| [legged_gym](https://github.com/leggedrobotics/legged_gym) | Isaac Gym training code for ANYmal, terrain curriculum | the paper behind the "4 minutes" claim; code matches |
| [IsaacLab](https://github.com/isaac-sim/IsaacLab) | successor stack, many legged tasks, manager-based configs | heavier, actively maintained |
| [MuJoCo Playground](https://github.com/google-deepmind/mujoco_playground) | MJX training for quadrupeds (Go1/Go2-class), `pip install playground` | smallest path from zero to a walking policy |
| [unitree_rl_gym](https://github.com/unitreerobotics/unitree_rl_gym) | Unitree Go2/A1/H1 environments, sim2sim scripts | pairs with `unitree_mujoco` for policy transfer checks |
| [walk-these-ways](https://github.com/Improbable-AI/walk-these-ways) | rapid locomotion adaptation, teacher-student | good reading for privileged training |

**Navigating terrain**

| resource | what it gives you |
| --- | --- |
| [elevation_mapping_cupy](https://github.com/leggedrobotics/elevation_mapping_cupy) | GPU elevation maps from depth, used in legged navigation stacks |
| [Nav2](https://github.com/ros-navigation/navigation2) | costmaps, planners, recovery behaviours — works for quadrupeds once a proper footprint and terrain layer exist |
| [grid_map](https://github.com/ANYbotics/grid_map) | 2.5D terrain representation, the usual glue between perception and planning |

**Reading, not running**

- Rudin et al. 2021 ([arXiv:2109.11978](https://arxiv.org/abs/2109.11978)) — the massively-parallel recipe and its curriculum.
- Lee et al., "Learning quadrupedal locomotion over challenging terrain" (Science Robotics 2020) — teacher-student, terrain perception.
- Hwangbo et al. 2019 (Science Robotics) — the sim-to-real pipeline that made legged RL credible: actuator model, latency, domain randomisation.
- Kumar et al., "RMA: Rapid Motor Adaptation" (RSS 2021) — adaptation without online system identification.

---

## 4. How to read a speedup (six questions)

Before you put a number in a slide, answer these. If any answer is "don't know", the number is decoration.

1. **Baseline what?** A speedup exists only against a named alternative. "10× faster" without a baseline is a mood.
2. **On which hardware?** The same code moves 3× between a laptop 4070 and an A100. GPU model, count, memory.
3. **Which version?** Physics engines change contact solvers between minor releases. Commit hash or version tag.
4. **What task and scene size?** 4k envs of cart-pole and 4k envs of a 20-DoF quadruped on rough terrain are not the same measurement.
5. **Which metric?** env-steps/s, wall-clock-to-reward, samples-to-threshold, and real-time factor are four different numbers. A paper that reports one and you quote another is a mismatch, not a result.
6. **How noisy?** One run is an anecdote. Best-of-three without spread is still an anecdote.

A useful habit: whenever you read "X is N× faster", write down what question 1 through 5 would need to be true.
Most of the time you cannot fill them in, and that tells you how much weight the claim can carry.

## 5. Quadruped simulation suites at a glance

Descriptive, not ranked. "Sim2real" means the suite ships an actuator model, latency model or domain randomisation
that the authors used on hardware.

| suite | engine | tasks | sim2real support | notes |
| --- | --- | --- | --- | --- |
| [legged_gym](https://github.com/leggedrobotics/legged_gym) | Isaac Gym | ANYmal / Cassie / A1 locomotion, terrain curriculum | actuator network + terrain curriculum from the paper | smallest readable codebase for the 4-minute result |
| [IsaacLab](https://github.com/isaac-sim/IsaacLab) | Isaac Sim (PhysX 5) | legged, manipulators, sensors, many envs | yes, plus sensor simulation | heavier install, actively maintained |
| [MuJoCo Playground](https://github.com/google-deepmind/mujoco_playground) | MJX | quadruped, humanoid, hands, arms | actuator + latency modelling in the task configs | `pip install playground`, lowest setup cost |
| [unitree_rl_gym](https://github.com/unitreerobotics/unitree_rl_gym) | Isaac Gym | Go2 / A1 / H1 | ships sim2sim scripts (Isaac to MuJoCo) | the sim2sim path is the useful part |
| [walk-these-ways](https://github.com/Improbable-AI/walk-these-ways) | Isaac Gym | rapid locomotion adaptation, teacher-student | privileged training + adaptation module | good reading for privileged learning |

Pick by what you need to prove, not by stars: to prove *throughput*, MuJoCo Playground gets you to a running
number in one evening; to prove *sim2real discipline*, legged_gym or walk-these-ways show the whole pipeline.

## 6. Motion control: where the milliseconds actually go

Real-time loops are the part of this field where claims age fastest and matter most.

- A 1 kHz loop has a 1 ms budget. A single missed deadline is a torque spike, not a slow frame.
- Typical end-to-end budget, in the order it is usually spent: sensor read → fieldbus transfer → controller compute →
  command write. On EtherCAT the frame itself is tens of microseconds; on a 115200 serial link a 20-byte frame is
  already ~1.7 ms, which blows the budget before any control code runs.
- `SCHED_FIFO` removes CFS scheduling noise but not interrupt or SMI jitter; `PREEMPT_RT` removes most of the rest.
  Measure `P99` and `max`, not the mean — the mean is always fine.

Measured jitter numbers from this account live in [rt-joint-control](https://github.com/cccjj55/rt-joint-control)
and are labelled there as synthetic until a board is attached.

---

## 7. What this repo refuses to do

- Quote a speedup without the baseline it was measured against.
- Quote a throughput without the hardware.
- Present an upstream claim as a reproduction.
- Rank engines by one number. A simulator that trains a policy in four minutes and cannot reproduce a contact
  sequence is not "faster" in any useful sense.

---

## Contributing

If you have a number with a source, a hardware line and a version, open an issue using the *submit a number*
template. The bar is in [docs/evidence-rules.md](docs/evidence-rules.md). Contradicting rows are welcome —
a `3P` row that disagrees with an `UPSTREAM` row is the most valuable thing this repo can hold.

## License

MIT for the text and tables. Quoted numbers remain the property of their sources; each row links to one.
