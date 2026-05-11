# Awesome Collision Detection

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of collision detection libraries, algorithms, papers, and related resources.

## Contents
* [Libraries](#libraries)
  * [Active](#active)
  * [Inactive](#inactive)
  * [Mesh Processing](#mesh-processing)
* [Comparisons](COMPARISONS.md)
* [Papers](#papers)
* [Books](#books)
* [Articles](#articles)
* [Other Awesome Lists](#other-awesome-lists)
* [Contributing](#contributing)
* [Star History](#star-history)
* [License](#license)

> **Legend**: 🟢 Active (<1yr) · 🟡 Slow (1-2yr) · 🔴 Stale (>2yr) · 💀 Archived

## [Libraries](#contents)

### [Active](#contents)

_Collision detection, distance query, and proximity query libraries. See also [Comparisons](COMPARISONS.md)._

* 🔴 [BEPUphysics 1](http://www.bepuphysics.com/) - Pure C# physics engine with broadphase and narrowphase collision detection. [⭐ 425](https://github.com/bepu/bepuphysics1)
* 🟢 [Box2D](https://box2d.org) - 2D physics engine with collision, distance, ray cast, and shape cast queries. [⭐ 9.7k](https://github.com/erincatto/box2d)
* 🟢 [Bullet](http://bulletphysics.org) - Real-time physics SDK with collision detection for games, robotics, and simulation. [⭐ 14.5k](https://github.com/bulletphysics/bullet3)
* 🔴 [CCD-Wrapper](https://github.com/Continuous-Collision-Detection/CCD-Wrapper) - Wrapper and benchmark for continuous collision detection algorithms. [⭐ 60](https://github.com/Continuous-Collision-Detection/CCD-Wrapper)
* 🟢 [coal (HPP-FCL)](https://github.com/coal-library/coal) - Collision detection and distance query library derived from HPP-FCL. [⭐ 586](https://github.com/coal-library/coal)
* 🔴 collision-rs - Rust collision detection library with broadphase and narrowphase queries. [⭐ 130](https://github.com/rustgd/collision-rs)
* 🟢 [FCL](https://github.com/flexible-collision-library/fcl) - Flexible Collision Library for collision, distance, and continuous collision queries. [⭐ 1.7k](https://github.com/flexible-collision-library/fcl)
* 🔴 [JitterPhysics](https://github.com/mattleibow/jitterphysics) - C# rigid body physics engine with collision detection support. [⭐ 47](https://github.com/mattleibow/jitterphysics)
* 🟢 [Kraft](https://github.com/BeRo1985/kraft) - Object Pascal physics engine with discrete and optional continuous collision detection. [⭐ 126](https://github.com/BeRo1985/kraft)
* 🔴 [libccd](https://github.com/danfis/libccd) - Small C library for collision detection between convex shapes using GJK and EPA. [⭐ 639](https://github.com/danfis/libccd)
* 🟢 [MuJoCo](https://mujoco.org/) - Physics simulator with contact, collision, and distance queries for robotics and control. [⭐ 13.4k](https://github.com/google-deepmind/mujoco)
* 🔴 [ncollide](http://ncollide.org/) - Rust collision detection library for 2D and 3D geometric queries. [⭐ 934](https://github.com/sebcrozet/ncollide)
* [ODE](http://www.ode.org/) - Open Dynamics Engine with rigid body simulation and collision detection. [[bitbucket](https://bitbucket.org/odedevs/ode)]
* 🟢 [OpenGJK](https://www.mattiamontanari.com/opengjk/) - GJK-based minimum distance library with bindings for multiple languages. [⭐ 197](https://github.com/MattiaMontanari/openGJK)
* 🟢 [Parry](https://github.com/dimforge/parry) - Rust collision detection and geometric query library from Dimforge. [⭐ 819](https://github.com/dimforge/parry)
* 🟢 [PhysX](https://nvidia-omniverse.github.io/PhysX/) - NVIDIA physics SDK with scene queries, contact generation, and collision detection. [⭐ 4.5k](https://github.com/NVIDIA-Omniverse/PhysX)
* 🟢 [python-fcl](https://github.com/BerkeleyAutomation/python-fcl) - Python bindings for FCL collision, distance, and continuous collision queries. [⭐ 269](https://github.com/BerkeleyAutomation/python-fcl)
* 🟢 [pytorch_volumetric](https://github.com/UM-ARM-Lab/pytorch_volumetric) - PyTorch utilities for volumetric signed distance fields and differentiable collision queries. [⭐ 246](https://github.com/UM-ARM-Lab/pytorch_volumetric)
* 💀 qu3e - Lightweight 3D rigid body physics engine with collision detection. [⭐ 991](https://github.com/RandyGaul/qu3e)
* 🟡 [ReactPhysics3d](http://www.reactphysics3d.com/) - C++ 3D physics engine with rigid body collision detection. [⭐ 1.7k](https://github.com/DanielChappuis/reactphysics3d)
* 🟢 [Tight-Inclusion](https://continuous-collision-detection.github.io/tight_inclusion/) - Conservative continuous collision detection library with minimum separation support. [⭐ 157](https://github.com/Continuous-Collision-Detection/Tight-Inclusion)
* 🟢 tinyc2 - Single-header 2D collision detection library for primitive shapes. [⭐ 5k](https://github.com/RandyGaul/tinyheaders)

> Some libraries, such as ODE and Bullet, are physics engines that can also be used as collision detection libraries.

### [Inactive](#contents)

* [ColDet](https://sourceforge.net/projects/coldet/) - 3D Collision Detection.
* [GIMPACT](http://gimpact.sourceforge.net/) - Tools for geometry processing and collision detection.
* [OPCODE](http://www.codercorner.com/Opcode.htm) - Optimized Collision Detection.
* 🔴 OZCollide - Legacy collision detection library. [⭐ 4](https://github.com/jslee02/OZCollide)
* [SOLID](http://solid.sourceforge.net/) - Collision detection of 3D objects undergoing rigid motion and deformation.

### [Mesh Processing](#contents)

_Geometry processing libraries useful for collision-ready meshes and convex approximations._

* 🔴 [bounding-mesh](http://www.boundingmesh.com/) - Implementation of the bounding mesh and bounding convex decomposition algorithms for single-sided mesh approximation. [⭐ 349](https://github.com/gaschler/bounding-mesh)
* 🟢 cinolib - A generic programming header only C++ library for processing polygonal and polyhedral meshes. [⭐ 1.1k](https://github.com/mlivesu/cinolib)
* 🟢 [CoACD](https://colin97.github.io/CoACD/) - Approximate convex decomposition for collision-aware mesh approximation. [⭐ 1k](https://github.com/SarahWeiii/CoACD)
* 🟢 [libigl](https://libigl.github.io/) - A simple C++ geometry processing library. [⭐ 5k](https://github.com/libigl/libigl)

## [Papers](#contents)

#### Collision Detection and Distance Computation

* GJK++: Leveraging Acceleration Methods for Faster Collision Detection (2023), Montaut et al. [[pdf](https://hal.science/hal-04070039v1/document), [code](https://github.com/humanoid-path-planner/hpp-fcl), [benchmarks](https://github.com/lmontaut/colbench)]
* Collision Detection Accelerated: An Optimization Perspective (2022), Montaut et al. [[pdf](https://hal.archives-ouvertes.fr/hal-03662157/document), [code](https://github.com/humanoid-path-planner/hpp-fcl), [benchmarks](https://github.com/lmontaut/collision-detection-benchmark)]
* A fast procedure for computing the distance between complex objects in three-dimensional space (1988) Gilbert, Johnson and Keerthi [[pdf](https://graphics.stanford.edu/courses/cs448b-00-winter/papers/gilbert.pdf)]

#### Differentiable Collision Detection

* Differentiable Collision Detection: a Randomized Smoothing Approach (2022), Montaut et al. [[pdf](https://hal.archives-ouvertes.fr/hal-03780482v2/document), [code](https://github.com/humanoid-path-planner/hpp-fcl)]

#### Triangle-triangle Test

* A faster triangle-to-triangle intersection test algorithm (2013), L.-Y. Wei.
* Efficient triangle-triangle intersection test for OBB-based collision detection (2009), J.-W. Chang et al. [[pdf](http://ldc.usb.ve/~vtheok/cursos/ci6322/escogidos/Efficient%20triangle%E2%80%93triangleintersectiontestforOBB.pdf)]
* A fast triangle to triangle intersection test for collision detection (2006), O. Tropp et al. [[pdf](http://webee.technion.ac.il/~ayellet/Ps/TroppTalShimshoni.pdf)]
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
* Fast Proximity Queries with Swept Sphere Volumes (1999), E. Larsen et al. [[pdf](https://www.researchgate.net/profile/Dinesh_Manocha/publication/2318075_Fast_Proximity_Queries_with_Swept_Sphere_Volumes/links/54ecdc250cf2465f53305253/Fast-Proximity-Queries-with-Swept-Sphere-Volumes.pdf), [web](http://gamma.cs.unc.edu/SSV/)]

#### Continuous Collision Detection

* Hierarchical and Controlled Advancement for Continuous Collision Detection of Rigid and Articulated Models (2013), M. Tang et al. [[pdf](http://graphics.ewha.ac.kr/C2A/TVCG13.pdf), [web](http://graphics.ewha.ac.kr/C2A/)]
* Efficient Geometrically Exact Continuous Collision Detection (2012), T. Brochu et al. [[pdf](https://www.researchgate.net/profile/Essex_Edwards/publication/254200434_Efficient_Geometrically_Exact_Continuous_Collision_Detection/links/5540dd8a0cf2322227304cce/Efficient-Geometrically-Exact-Continuous-Collision-Detection.pdf)]
* C2A: Controlled Conservative Advancement for Continuous Collision Detection of Polygonal Models (2009), M. Tang et al. [[pdf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.500.7676&rep=rep1&type=pdf)]
* Continuous Collision Detection for Articulated Models using Taylor Models and Temporal Culling (2007), X. Zhang et al. [[pdf](https://hal.inria.fr/file/index/docid/390313/filename/SIGGRAPH2007.pdf), [web](http://graphics.ewha.ac.kr/CATCH/)]
* Interactive continuous collision detection for non-convex polyhedra (2006), X. Zhang et al. [[pdf](https://link.springer.com/content/pdf/10.1007/s00371-006-0060-0.pdf), [web](http://graphics.ewha.ac.kr/FAST/)]

#### Nearest Neighbor

* Faster cover tree (2015), M. Izbicki et al. [[pdf](http://proceedings.mlr.press/v37/izbicki15.pdf), [code](https://github.com/manzilzaheer/CoverTree)]
* Fast Approximate Nearest Neighbors with Automatic Algorithm Configuration (2009), M. Muja and D. Lowe. [[pdf](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.160.1721&rep=rep1&type=pdf), [code](https://github.com/mariusmuja/flann)]
* Cover Tree for Nearest Neighbor (2006), A. Beygelzimer et al. [[pdf](https://homes.cs.washington.edu/~sham/papers/ml/cover_tree.pdf), [web](http://hunch.net/~jl/projects/cover_tree/cover_tree.html), [code](https://github.com/DNCrane/Cover-Tree)]

#### Comprehensive Collision Detection Library

* FCL: A General Purpose Library for Collision and Proximity Queries (2012), J. Pan et al. [[pdf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.259.2177&rep=rep1&type=pdf), [code](https://github.com/flexible-collision-library/fcl)]

#### Survey

* Collision Detection: A Survey (2007), S. Kockara et al. [[pdf](https://pdfs.semanticscholar.org/250e/296b4b4c1b7ac0229e57d6638fe81188121e.pdf)]
* 3D collision detection: a survey (2001), P. Jiménez et al. [[pdf](https://users.soe.ucsc.edu/~pang/161/w06/notes/jtt01.pdf)]

## [Books](#contents)

* Real-Time Collision Detection, CRC Press 2004 ([amazon](http://www.amazon.com/Real-Time-Collision-Detection-Interactive-Technology/dp/1558607323/ref=sr_1_1?s=books&ie=UTF8&qid=1463804277&sr=1-1&keywords=real+time+collision+detection))
* Collision Detection in Interactive 3D Environments, CRC Press 2003 ([amazon](http://www.amazon.com/Collision-Detection-Interactive-Environments-Technology/dp/155860801X))

## [Articles](#contents)

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
* [3D Collision detection](http://www.miguelcasillas.com/?mcportfolio=collision-detection-c) by [Miguel Casillas](http://www.miguelcasillas.com/?page_id=451)
* [Collision Detection](http://www.jeffreythompson.org/collision-detection/) ([code](https://github.com/jeffThompson/CollisionDetection)) by Jeff Thompson - This book explains the algorithms behind those collisions using basic shapes like circles, rectangles, and lines so you can implement them into your own projects.
* [Note: The Gibert-Jonson-Keerthi algorithm](http://realtimecollisiondetection.net/pubs/SIGGRAPH04_Ericson_GJK_notes.pdf) by Christer Ericson

#### Space Partitioning

* [Benchmark of various spatial data structures for collision detection](https://github.com/ttvd/spatial-collision-datastructures)
* Bounding volume hierarchy
  * [Bounding Volume Hierarchy Optimization through Agglomerative Treelet Restructuring](http://www.highperformancegraphics.org/wp-content/uploads/2015/Papers-Session1/apresentacao.pdf) ([paper](http://dl.acm.org/citation.cfm?id=2790065), [code](https://github.com/leonardo-domingues/atrbvh)) by Leonardo R. Domingues and Helio Pedrini.
  * [Dynamic AABB Tree](http://www.randygaul.net/2013/08/06/dynamic-aabb-tree/) by [Randy Gaul](http://www.randygaul.net/about/)
  * [Efficient BVH Construction via Approximate Agglomerative Clustering](http://dl.acm.org/citation.cfm?id=2492054) ([pdf](http://repository.cmu.edu/cgi/viewcontent.cgi?article=3602&context=compsci)) by Yan Gu et al.
  * [Octree vs BVH](http://thomasdiewald.com/blog/?p=1488) by [Thomas Diewald](http://thomasdiewald.com/blog/?page_id=14)

## [Other Awesome Lists](#contents)

* [Awesome Robotics Libraries](https://github.com/jslee02/awesome-robotics-libraries) [⭐ 2.9k](https://github.com/jslee02/awesome-robotics-libraries) - This is a list of various libraries and software for robotics. It's also attempting to provide some comparisons for selected libraries and software.

## [Contributing](#contents)

Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/main/CONTRIBUTING.md) first. Also, please feel free to report any error.

## [Star History](#contents)

[![Star History Chart](https://api.star-history.com/svg?repos=jslee02/awesome-collision-detection&type=Date)](https://star-history.com/#jslee02/awesome-collision-detection)

## [License](#contents)

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)
