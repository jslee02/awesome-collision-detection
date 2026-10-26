# Awesome Collision Detection

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of collision detection libraries, algorithms, papers, and related resources.

## Contents
* [Libraries](#libraries)
* [Mesh Processing](#mesh-processing)
* [Papers](#papers)
* [Books](#books)
* [Articles](#articles)
* [Other Awesome Lists](#other-awesome-lists)
* [Comparisons](COMPARISONS.md)
* [Contributing](#contributing)
* [Star History](#star-history)
* [License](#license)

> **Legend**: 🟢 commit within 1 yr · 🟡 commit within 3 yr · 💀 archived · ⭐ GitHub stars as of 2026-10-26. Software entries are ordered by stars; inactive entries (archived, or no commits for 3+ years) are folded at the end of each category.

## [Libraries](#contents)

_Collision detection, distance query, and proximity query libraries. See also [Comparisons](COMPARISONS.md)._

* 🟢 [MuJoCo](https://mujoco.org/) - Physics simulator with contact, collision, and distance queries for robotics and control. [⭐ 15.9k](https://github.com/google-deepmind/mujoco)
* 🟢 [Bullet](http://bulletphysics.org) - Real-time physics SDK with collision detection for games, robotics, and simulation. [⭐ 14.8k](https://github.com/bulletphysics/bullet3)
* 🟢 [Box2D](https://box2d.org) - 2D physics engine with collision, distance, ray cast, and shape cast queries. [⭐ 10.5k](https://github.com/erincatto/box2d)
* 🟢 tinyc2 - Single-header 2D collision detection library for primitive shapes. [⭐ 5.1k](https://github.com/RandyGaul/cute_headers)
* 🟢 [PhysX](https://nvidia-omniverse.github.io/PhysX/) - NVIDIA physics SDK with scene queries, contact generation, and collision detection. [⭐ 4.8k](https://github.com/NVIDIA-Omniverse/PhysX)
* 🟡 [ReactPhysics3d](https://www.reactphysics3d.com/) - C++ 3D physics engine with rigid body collision detection. [⭐ 1.8k](https://github.com/DanielChappuis/reactphysics3d)
* 🟢 [FCL](https://github.com/flexible-collision-library/fcl) - Flexible Collision Library for collision, distance, and continuous collision queries. [⭐ 1.8k](https://github.com/flexible-collision-library/fcl)
* 🟢 [Parry](https://github.com/dimforge/parry) - Rust collision detection and geometric query library from Dimforge. [⭐ 885](https://github.com/dimforge/parry)
* 🟢 [coal (HPP-FCL)](https://github.com/coal-library/coal) - Collision detection and distance query library derived from HPP-FCL. [⭐ 658](https://github.com/coal-library/coal)
* 🟢 [python-fcl](https://github.com/BerkeleyAutomation/python-fcl) - Python bindings for FCL collision, distance, and continuous collision queries. [⭐ 271](https://github.com/BerkeleyAutomation/python-fcl)
* 🟢 [pytorch_volumetric](https://github.com/UM-ARM-Lab/pytorch_volumetric) - PyTorch utilities for volumetric signed distance fields and differentiable collision queries. [⭐ 252](https://github.com/UM-ARM-Lab/pytorch_volumetric)
* 🟢 [OpenGJK](https://www.mattiamontanari.com/opengjk/) - GJK-based minimum distance library with bindings for multiple languages. [⭐ 209](https://github.com/MattiaMontanari/openGJK)
* 🟢 [Tight-Inclusion](https://continuous-collision-detection.github.io/tight_inclusion/) - Conservative continuous collision detection library with minimum separation support. [⭐ 160](https://github.com/Continuous-Collision-Detection/Tight-Inclusion)
* 🟢 [Kraft](https://github.com/BeRo1985/kraft) - Object Pascal physics engine with discrete and optional continuous collision detection. [⭐ 133](https://github.com/BeRo1985/kraft)
* [ODE](https://ode.org/) - Open Dynamics Engine with rigid body simulation and collision detection. [[bitbucket](https://bitbucket.org/odedevs/ode)]

> Some libraries, such as ODE and Bullet, are physics engines that can also be used as collision detection libraries.

<details>
<summary>Inactive (12): archived or no commits for 3+ years</summary>

* 💀 qu3e - Lightweight 3D rigid body physics engine with collision detection. [⭐ 993](https://github.com/RandyGaul/qu3e) · last commit 2021
* [ncollide](http://ncollide.org/) - Rust collision detection library for 2D and 3D geometric queries. [⭐ 926](https://github.com/dimforge/ncollide) · last commit 2022
* [libccd](https://github.com/danfis/libccd) - Small C library for collision detection between convex shapes using GJK and EPA. [⭐ 653](https://github.com/danfis/libccd) · last commit 2018
* [BEPUphysics 1](http://www.bepuphysics.com/) - Pure C# physics engine with broadphase and narrowphase collision detection. [⭐ 434](https://github.com/bepu/bepuphysics1) · last commit 2021
* collision-rs - Rust collision detection library with broadphase and narrowphase queries. [⭐ 129](https://github.com/rustgd/collision-rs) · last commit 2021
* [CCD-Wrapper](https://github.com/Continuous-Collision-Detection/CCD-Wrapper) - Wrapper and benchmark for continuous collision detection algorithms. [⭐ 61](https://github.com/Continuous-Collision-Detection/CCD-Wrapper) · last commit 2022
* [JitterPhysics](https://github.com/mattleibow/jitterphysics) - C# rigid body physics engine with collision detection support. [⭐ 47](https://github.com/mattleibow/jitterphysics) · last commit 2021
* OZCollide - Legacy collision detection library. [⭐ 4](https://github.com/jslee02/OZCollide) · last commit 2017
* [ColDet](https://sourceforge.net/projects/coldet/) - 3D Collision Detection.
* [GIMPACT](https://gimpact.sourceforge.net/) - Tools for geometry processing and collision detection.
* [OPCODE](http://www.codercorner.com/Opcode.htm) - Optimized Collision Detection.
* [SOLID](https://solid.sourceforge.net/) - Collision detection of 3D objects undergoing rigid motion and deformation.

</details>

## [Mesh Processing](#contents)

_Geometry processing libraries useful for collision-ready meshes and convex approximations._

* 🟢 [libigl](https://libigl.github.io/) - A simple C++ geometry processing library. [⭐ 5.1k](https://github.com/libigl/libigl)
* 🟢 [CoACD](https://colin97.github.io/CoACD/) - Approximate convex decomposition for collision-aware mesh approximation. [⭐ 1.2k](https://github.com/SarahWeiii/CoACD)
* 🟢 cinolib - A generic programming header only C++ library for processing polygonal and polyhedral meshes. [⭐ 1.1k](https://github.com/mlivesu/cinolib)

<details>
<summary>Inactive (1): archived or no commits for 3+ years</summary>

* [bounding-mesh](http://www.boundingmesh.com/) - Implementation of the bounding mesh and bounding convex decomposition algorithms for single-sided mesh approximation. [⭐ 351](https://github.com/gaschler/bounding-mesh) · last commit 2019

</details>

## [Papers](#contents)

_Research papers on collision detection, distance and proximity queries, and supporting algorithms._

#### Collision Detection and Distance Computation

* GJK++: Leveraging Acceleration Methods for Faster Collision Detection (2023), Montaut et al. [[pdf](https://hal.science/hal-04070039v1/document), [code](https://github.com/coal-library/coal), [benchmarks](https://github.com/lmontaut/colbench)]
* Collision Detection Accelerated: An Optimization Perspective (2022), Montaut et al. [[pdf](https://hal.archives-ouvertes.fr/hal-03662157/document), [code](https://github.com/coal-library/coal), [benchmarks](https://github.com/lmontaut/collision-detection-benchmark)]
* A fast procedure for computing the distance between complex objects in three-dimensional space (1988) Gilbert, Johnson and Keerthi [[pdf](https://graphics.stanford.edu/courses/cs448b-00-winter/papers/gilbert.pdf)]

#### Differentiable Collision Detection

* Differentiable Collision Detection: a Randomized Smoothing Approach (2022), Montaut et al. [[pdf](https://hal.archives-ouvertes.fr/hal-03780482v2/document), [code](https://github.com/coal-library/coal)]

#### Triangle-triangle Test

* A faster triangle-to-triangle intersection test algorithm (2013), L.-Y. Wei.
* Efficient triangle-triangle intersection test for OBB-based collision detection (2009), J.-W. Chang et al. [[pdf](http://ldc.usb.ve/~vtheok/cursos/ci6322/escogidos/Efficient%20triangle%E2%80%93triangleintersectiontestforOBB.pdf)]
* A fast triangle to triangle intersection test for collision detection (2006), O. Tropp et al. [[pdf](https://webee.technion.ac.il/~ayellet/Ps/TroppTalShimshoni.pdf)]
  * A failure case was reported in [Stack Overflow](http://stackoverflow.com/a/29563443/3122234).
* Faster Triangle-Triangle Intersection Tests (2006), O. Devillers et al. [[pdf](https://hal.inria.fr/inria-00072100/document), [code](https://github.com/CGAL/cgal/blob/076c982dbf37cc244206fd7962e73360fb17ea47/Intersections_3/include/CGAL/Triangle_3_Triangle_3_do_intersect.h)]
* A Fast Triangle-Triangle Intersecion Test (1997), T. Muller. [[pdf](http://web.stanford.edu/class/cs277/resources/papers/Moller1997b.pdf), [code](https://github.com/erich666/jgt-code/blob/master/Volume_02/Number_2/Moller1997b/tritri_isectline.c)]

#### Mesh Collision

* Robust contact generation for robot simulation with unstructured meshes (2013), K. Hauser. [[pdf](https://motion.cs.illinois.edu/papers/ISRR2013-RobustContact.pdf), [web](http://motion.cs.illinois.edu/simulation/index.html)]
* Approximate Convex Decomposition for 3D Meshes with Collision-Aware Concavity and Tree Search (2022), X. Wei et al. [[pdf](https://arxiv.org/pdf/2205.02961), [project](https://colin97.github.io/CoACD/), [code](https://github.com/SarahWeiii/CoACD), [video](https://www.youtube.com/watch?v=r12O0z0723s)]

#### Penetration Depth Computation

* PolyDepth: Real-time Penetration Depth Computation using Iterative Contact-Space Projection (2012), C. Je et al. [[pdf](https://arxiv.org/pdf/1508.06181v1.pdf)]

#### Proximity Query / Signed Distance Field

* Local Optimization for Robust Signed Distance Field Collision (2020), [M. Macklin](http://blog.mmacklin.com/) et al. [[pdf](https://mmacklin.com/sdfcontact.pdf), [slides](https://mmacklin.com/sdfcontact_slides.pdf), [video](https://youtu.be/icU6Bm-HZ-E)]
* Hierarchical hp-Adaptive Signed Distance Fields (2016), D. Koschier et al. [[pdf](https://pdfs.semanticscholar.org/0dac/60f8ebf218a5510799cab4c74c5bb1f276e9.pdf), [video](https://youtu.be/x_Iq2yM4FcA)]
* Voxblox: Building 3d signed distance fields for planning (2016), H Oleynikova et al. [[pdf](https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/128028/eth-50485-01.pdf), [code](https://github.com/ethz-asl/voxblox)]
* Signed distance fields for polygon soup meshes (2014), H. Xu and Jernej Barbic. [[pdf](https://pdfs.semanticscholar.org/6247/71efeaff92c9826b9fa176e8c76a2def1d9f.pdf)]
* Fast Proximity Queries with Swept Sphere Volumes (1999), E. Larsen et al. [[pdf](https://www.researchgate.net/profile/Dinesh_Manocha/publication/2318075_Fast_Proximity_Queries_with_Swept_Sphere_Volumes/links/54ecdc250cf2465f53305253/Fast-Proximity-Queries-with-Swept-Sphere-Volumes.pdf), [web](https://gamma.cs.unc.edu/SSV/)]

#### Continuous Collision Detection

* Hierarchical and Controlled Advancement for Continuous Collision Detection of Rigid and Articulated Models (2013), M. Tang et al. [[pdf](http://graphics.ewha.ac.kr/C2A/TVCG13.pdf), [web](http://graphics.ewha.ac.kr/C2A/)]
* Efficient Geometrically Exact Continuous Collision Detection (2012), T. Brochu et al. [[pdf](https://www.researchgate.net/profile/Essex_Edwards/publication/254200434_Efficient_Geometrically_Exact_Continuous_Collision_Detection/links/5540dd8a0cf2322227304cce/Efficient-Geometrically-Exact-Continuous-Collision-Detection.pdf)]
* C2A: Controlled Conservative Advancement for Continuous Collision Detection of Polygonal Models (2009), M. Tang et al. [[pdf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.500.7676&rep=rep1&type=pdf)]
* Continuous Collision Detection for Articulated Models using Taylor Models and Temporal Culling (2007), X. Zhang et al. [[pdf](https://hal.inria.fr/file/index/docid/390313/filename/SIGGRAPH2007.pdf), [web](http://graphics.ewha.ac.kr/CATCH/)]
* Interactive continuous collision detection for non-convex polyhedra (2006), X. Zhang et al. [[pdf](https://link.springer.com/content/pdf/10.1007/s00371-006-0060-0.pdf), [web](http://graphics.ewha.ac.kr/FAST/)]

#### Nearest Neighbor

* Faster cover tree (2015), M. Izbicki et al. [[pdf](http://proceedings.mlr.press/v37/izbicki15.pdf), [code](https://github.com/manzilzaheer/CoverTree)]
* Fast Approximate Nearest Neighbors with Automatic Algorithm Configuration (2009), M. Muja and D. Lowe. [[pdf](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.160.1721&rep=rep1&type=pdf), [code](https://github.com/flann-lib/flann)]
* Cover Tree for Nearest Neighbor (2006), A. Beygelzimer et al. [[pdf](https://homes.cs.washington.edu/~sham/papers/ml/cover_tree.pdf), [web](https://hunch.net/~jl/projects/cover_tree/cover_tree.html), [code](https://github.com/DNCrane/Cover-Tree)]

#### Comprehensive Collision Detection Library

* FCL: A General Purpose Library for Collision and Proximity Queries (2012), J. Pan et al. [[pdf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.259.2177&rep=rep1&type=pdf), [code](https://github.com/flexible-collision-library/fcl)]

#### Survey

* Collision Detection: A Survey (2007), S. Kockara et al. [[pdf](https://pdfs.semanticscholar.org/250e/296b4b4c1b7ac0229e57d6638fe81188121e.pdf)]
* 3D collision detection: a survey (2001), P. Jiménez et al. [[pdf](https://users.soe.ucsc.edu/~pang/161/w06/notes/jtt01.pdf)]

## [Books](#contents)

_Books on collision detection algorithms and their implementation._

* Real-Time Collision Detection, CRC Press 2004 ([amazon](https://www.amazon.com/Real-Time-Collision-Detection-Interactive-Technology/dp/1558607323/ref=sr_1_1?s=books&ie=UTF8&qid=1463804277&sr=1-1&keywords=real+time+collision+detection))
* Collision Detection in Interactive 3D Environments, CRC Press 2003 ([amazon](https://www.amazon.com/Collision-Detection-Interactive-Environments-Technology/dp/155860801X))

## [Articles](#contents)

_Articles, talks, tutorials, and blog posts about collision detection and related geometry algorithms._

#### Overview & Tutorial

* [Video Game Physics Tutorial - Part II: Collision Detection for Solid Objects](https://www.toptal.com/game/video-game-physics-part-ii-collision-detection-for-solid-objects) by [Nilson Souto](https://www.toptal.com/resume/nilson-souto)
* [GPU Rigid Body Simulation](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/bullet/GDC2013_ErwinCoumans_GPU_rigid_body_simulation.pdf) (GDC 2013), Erwin Coumans
* [OpenCL accelerated rigid body and collision detection](https://www.cse.lehigh.edu/~trink/RSS-2011/Presentations/coumans.pdf) (RSS 2011), Erwin Coumans
* [Contact Generation](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/bullet/GDC10_Coumans_Erwin_Contact.pdf) (GDC 2010), Erwin Coumans

#### Benchmark

* [spatial-collision-datastructures](https://github.com/ttvd/spatial-collision-datastructures) - Benchmark of various spatial data structures for collision detection.
* [Continuous Collision Detection](https://continuous-collision-detection.github.io/) ([code](https://github.com/continuous-collision-detection)) Project page for continuous collision detection papers, implementations, benchmarks, and datasets.

#### Narrow-phase

* [Algorithm table for narrowphase algorithms](http://www.realtimerendering.com/intersections.html)
* [3D Collision detection](https://www.miguelcasillas.com/?mcportfolio=collision-detection-c) by [Miguel Casillas](http://www.miguelcasillas.com/?page_id=451)
* [Collision Detection](http://www.jeffreythompson.org/collision-detection/) ([code](https://github.com/jeffThompson/CollisionDetection)) by Jeff Thompson - This book explains the algorithms behind those collisions using basic shapes like circles, rectangles, and lines so you can implement them into your own projects.
* [Note: The Gibert-Jonson-Keerthi algorithm](https://realtimecollisiondetection.net/pubs/SIGGRAPH04_Ericson_GJK_notes.pdf) by Christer Ericson

#### Space Partitioning

* [Benchmark of various spatial data structures for collision detection](https://github.com/ttvd/spatial-collision-datastructures)
* Bounding volume hierarchy
  * [Bounding Volume Hierarchy Optimization through Agglomerative Treelet Restructuring](https://www.highperformancegraphics.org/wp-content/uploads/2015/Papers-Session1/apresentacao.pdf) ([paper](http://dl.acm.org/citation.cfm?id=2790065), [code](https://github.com/leonardo-domingues/atrbvh)) by Leonardo R. Domingues and Helio Pedrini.
  * [Dynamic AABB Tree](http://www.randygaul.net/2013/08/06/dynamic-aabb-tree/) by [Randy Gaul](http://www.randygaul.net/about/)
  * [Efficient BVH Construction via Approximate Agglomerative Clustering](http://dl.acm.org/citation.cfm?id=2492054) ([pdf](http://repository.cmu.edu/cgi/viewcontent.cgi?article=3602&context=compsci)) by Yan Gu et al.
  * [Octree vs BVH](http://thomasdiewald.com/blog/?p=1488) by [Thomas Diewald](http://thomasdiewald.com/blog/?page_id=14)

## [Other Awesome Lists](#contents)

_Related curated lists and collections._

* 🟢 [Awesome Robotics Libraries](https://github.com/jslee02/awesome-robotics-libraries) - This is a list of various libraries and software for robotics. It's also attempting to provide some comparisons for selected libraries and software. [⭐ 3.1k](https://github.com/jslee02/awesome-robotics-libraries)

## [Contributing](#contents)

Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/main/CONTRIBUTING.md) first. Also, please feel free to report any error.

## [Star History](#contents)

<a href="https://www.star-history.com/?repos=jslee02%2Fawesome-collision-detection">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=jslee02/awesome-collision-detection&type=date&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=jslee02/awesome-collision-detection&type=date&legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=jslee02/awesome-collision-detection&type=date&legend=top-left" />
  </picture>
</a>

## [License](#contents)

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
