# Comparisons

A companion to the main [Awesome Collision Detection](README.md) list, providing side-by-side comparisons for commonly used collision detection and proximity query libraries.

> **Last updated**: May 2026. Feature data is summarized from project documentation and repository metadata.

## Contents

* [Library Feature Matrix](#library-feature-matrix)
* [Shape Support](#shape-support)
* [Decision Guide](#decision-guide)
* [Benchmark Resources](#benchmark-resources)

## Library Feature Matrix

| Name | Collision | Distance | CCD | Ray/Shape Cast | Language | License |
|------|:---------:|:--------:|:---:|:--------------:|----------|---------|
| [Box2D](https://box2d.org) | Yes | Yes | Yes | Yes | C | MIT |
| [Bullet](https://pybullet.org/) | Yes | Yes | Yes | Yes | C++, Python | Zlib |
| [CCD-Wrapper](https://github.com/Continuous-Collision-Detection/CCD-Wrapper) | No | No | Yes | No | C++ | MIT |
| [FCL](https://github.com/flexible-collision-library/fcl) | Yes | Yes | Yes | No | C++ | BSD-3-Clause |
| [coal](https://github.com/coal-library/coal) | Yes | Yes | Partial | No | C++, Python | BSD-3-Clause |
| [libccd](https://github.com/danfis/libccd) | Yes | No | No | No | C | BSD-3-Clause |
| [MuJoCo](https://mujoco.org/) | Yes | Yes | No | No | C++, Python | Apache-2.0 |
| [ODE](https://ode.org/) | Yes | Partial | No | Yes | C++, Python | LGPL-2.1 or BSD-3-Clause |
| [OpenGJK](https://www.mattiamontanari.com/opengjk/) | No | Yes | No | No | C++, C#, Go, MATLAB, Python | GPL-3.0 |
| [Parry](https://github.com/dimforge/parry) | Yes | Yes | Yes | Yes | Rust | Apache-2.0 |
| [PhysX](https://nvidia-omniverse.github.io/PhysX/) | Yes | Yes | Partial | Yes | C++ | BSD-3-Clause |
| [python-fcl](https://github.com/BerkeleyAutomation/python-fcl) | Yes | Yes | Yes | No | Python, Cython | BSD-3-Clause |
| [pytorch_volumetric](https://github.com/UM-ARM-Lab/pytorch_volumetric) | Partial | Yes | No | No | Python | MIT |
| [ReactPhysics3d](https://www.reactphysics3d.com/) | Yes | Partial | No | Yes | C++ | Zlib |
| [Tight-Inclusion](https://continuous-collision-detection.github.io/tight_inclusion/) | No | No | Yes | No | C++ | MIT |

**Legend**: Yes = directly supported by the library API; Partial = supported for selected shapes, backends, or workflows; No = not a primary feature.

## Shape Support

| Name | Primitives | Convex | Mesh | Height Field | SDF / Volumetric |
|------|:----------:|:------:|:----:|:------------:|:----------------:|
| Box2D | Yes | 2D | No | No | No |
| Bullet | Yes | Yes | Yes | Yes | No |
| FCL / coal / python-fcl | Yes | Yes | Yes | Yes | No |
| libccd | No | Yes | No | No | No |
| MuJoCo | Yes | Yes | Yes | Yes | No |
| ODE | Yes | Yes | Yes | No | No |
| OpenGJK | No | Yes | No | No | No |
| Parry | Yes | Yes | Yes | Yes | No |
| PhysX | Yes | Yes | Yes | Yes | No |
| pytorch_volumetric | No | Partial | Yes | No | Yes |
| ReactPhysics3d | Yes | Yes | Yes | Yes | No |

## Decision Guide

**Which library should I use?**

* **General C++ collision and proximity queries:** [FCL](https://github.com/flexible-collision-library/fcl), [coal](https://github.com/coal-library/coal), or [Bullet](https://github.com/bulletphysics/bullet3).
* **Robotics with Python bindings:** [python-fcl](https://github.com/BerkeleyAutomation/python-fcl), [coal](https://github.com/coal-library/coal), or [MuJoCo](https://github.com/google-deepmind/mujoco).
* **2D games and simulations:** [Box2D](https://github.com/erincatto/box2d).
* **Rust projects:** [Parry](https://github.com/dimforge/parry).
* **Exact or conservative continuous collision detection research:** [Tight-Inclusion](https://github.com/Continuous-Collision-Detection/Tight-Inclusion) or [CCD-Wrapper](https://github.com/Continuous-Collision-Detection/CCD-Wrapper).
* **Convex-only distance queries:** [OpenGJK](https://github.com/MattiaMontanari/openGJK) or [libccd](https://github.com/danfis/libccd).
* **GPU or production physics engine integration:** [PhysX](https://github.com/NVIDIA-Omniverse/PhysX), [Bullet](https://github.com/bulletphysics/bullet3), or [MuJoCo](https://github.com/google-deepmind/mujoco).
* **Signed distance fields and differentiable geometric queries:** [pytorch_volumetric](https://github.com/UM-ARM-Lab/pytorch_volumetric).

## Benchmark Resources

* [Continuous Collision Detection](https://continuous-collision-detection.github.io/) - Project page for CCD papers, implementations, benchmarks, and datasets.
* [CCD-Wrapper](https://github.com/Continuous-Collision-Detection/CCD-Wrapper) - Wrapper and benchmark for multiple CCD algorithms.
* [spatial-collision-datastructures](https://github.com/ttvd/spatial-collision-datastructures) - Benchmark of spatial data structures for collision detection.
* [Collision Detection Accelerated](https://github.com/lmontaut/collision-detection-benchmark) - Benchmark code for optimization-oriented collision detection.
* [GJK++ / colbench](https://github.com/lmontaut/colbench) - Benchmark suite for accelerated GJK variants.

## [Contributing](#comparisons)

Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/master/CONTRIBUTING.md) first. Also, please feel free to report any error.

## [License](#comparisons)

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)
