# Awesome Collision Detection

A curated list of collision detection open resources

#### Table of Contents
* [Libraries](#libraries)
* [Papers](#papers)
* [Books](#books)
* [Articles](#articles)
* [Other Awesome Lists](#other-awesome-lists)
* [Contributing](#contributing)

## [Libraries](#awesome-collision-detection)

**Active**

> :warning: The following table is not complete. Please feel free to report if you find something incorrect or missing.

| Name | Shapes | Features | Languages | Licenses | Code | Popularity |
|:----:| ------ | -------- | --------- | -------- | ---- | ---------- |
| [BEPUphysics 1](http://www.bepuphysics.com/) | (todo) | (todo) | C#, .NET | Apache v2 | [github](https://github.com/bepu/bepuphysics1) | ![BEPUphysics 1](https://img.shields.io/github/stars/bepu/bepuphysics1.svg?style=social&label=Star&maxAge=2592000) |
| [Bullet](http://bulletphysics.org) | (todo) | (todo) | C++, Python | Zlib | [github](https://github.com/bulletphysics/bullet3) | ![bullet3](https://img.shields.io/github/stars/bulletphysics/bullet3.svg?style=social&label=Star&maxAge=2592000) |
| collision-rs | (todo) | (todo) | Rust | Apache-2.0 | [github](https://github.com/rustgd/collision-rs) | ![rustgd/collision-rs](https://img.shields.io/github/stars/rustgd/collision-rs.svg?style=social&label=Star&maxAge=2592000) |
| [FCL](https://github.com/flexible-collision-library/fcl) | (todo) | (todo) | C++ | BSD-3-Clause | [github](https://github.com/flexible-collision-library/fcl) | ![fcl](https://img.shields.io/github/stars/flexible-collision-library/fcl.svg?style=social&label=Star&maxAge=2592000) |
| [JitterPhysics](https://github.com/mattleibow/jitterphysics) | (todo) | (todo) | C#, .NET | MIT | [github](https://github.com/mattleibow/jitterphysics) | ![JitterPhysics](https://img.shields.io/github/stars/mattleibow/jitterphysics.svg?style=social&label=Star&maxAge=2592000) |
| [libccd](https://github.com/danfis/libccd) | (todo) | (todo) | C | BSD-3-Clause | [github](https://github.com/danfis/libccd) | ![libccd](https://img.shields.io/github/stars/danfis/libccd.svg?style=social&label=Star&maxAge=2592000) |
| [ncollide](http://ncollide.org/) | (todo) | (todo) | Rust | BSD-3-Clause | [github](https://github.com/sebcrozet/ncollide) | ![sebcrozet/ncollide](https://img.shields.io/github/stars/sebcrozet/ncollide.svg?style=social&label=Star&maxAge=2592000) |
| [ODE](http://www.ode.org/) | (todo) | (todo) | C++, [Python](http://pyode.sourceforge.net/) | LGPL-2.1 or BSD-3-Clause | [bitbucket](https://bitbucket.org/odedevs/ode) | |
| [ReactPhysics3d](http://www.reactphysics3d.com/) | (todo) | (todo) | C++ | Zlib | [github](https://github.com/DanielChappuis/reactphysics3d) | ![reactphysics3d](https://img.shields.io/github/stars/DanielChappuis/reactphysics3d.svg?style=social&label=Star&maxAge=2592000) |
| tinyc2 | (todo) | 2d | C/C++ | Zlib | [github](https://github.com/RandyGaul/tinyheaders) | ![RandyGaul/tinyheaders](https://img.shields.io/github/stars/RandyGaul/tinyheaders.svg?style=social&label=Star&maxAge=2592000) |
| qu3e | (todo) | (todo) | C++ | Zlib | [github](https://github.com/RandyGaul/qu3e) | ![qu3e](https://img.shields.io/github/stars/RandyGaul/qu3e.svg?style=social&label=Star&maxAge=2592000) |

> Some libraries (e.g., ODE and Bullet) are physics engines that contain collision detection features, but they can be used just as collision detection libraries.

**Inactive**

* [ColDet](https://sourceforge.net/projects/coldet/) - 3D Collision Detection.
* [GIMPACT](http://gimpact.sourceforge.net/) - Tools for geometry processing and collision detection.
* [OPCODE](http://www.codercorner.com/Opcode.htm) - Optimized Collision Detection.
* OZCollide [[github](https://github.com/jslee02/OZCollide)]
* [SOLID](http://solid.sourceforge.net/) - Collision detection of 3D objects undergoing rigid motion and deformation.

### Mesh Processing

* [bounding-mesh](http://www.boundingmesh.com/) ([github](https://github.com/gaschler/bounding-mesh) ![bounding-mesh](https://img.shields.io/github/stars/gaschler/bounding-mesh.svg?style=social&label=Star&maxAge=2592000)) - Implementation of the bounding mesh and bounding convex decomposition algorithms for single-sided mesh approximation.
* cinolib ([github](https://github.com/mlivesu/cinolib) ![mlivesu/cinolib](https://img.shields.io/github/stars/mlivesu/cinolib.svg?style=social&label=Star&maxAge=2592000)) - A generic programming header only C++ library for processing polygonal and polyhedral meshes.
* [libigl](https://libigl.github.io/) ([github](https://github.com/libigl/libigl) ![libigl/libigl](https://img.shields.io/github/stars/libigl/libigl.svg?style=social&label=Star&maxAge=2592000)) - A simple C++ geometry processing library.

## [Papers](#awesome-collision-detection)

#### Collision Detection and Distance Computation

  * A fast procedure for computing the distance between complex objects in three-dimensional space (1988) Gilbert, Johnson and Keerthi [[pdf](https://graphics.stanford.edu/courses/cs448b-00-winter/papers/gilbert.pdf)]

#### Triangle-triangle Test

  * A faster triangle-to-triangle intersection test algorithm (2013), L.-Y. Wei.
  * Efficient triangle-triangle intersection test for OBB-based collision detection (2009), J.-W. Chang et al. [[pdf](http://ldc.usb.ve/~vtheok/cursos/ci6322/escogidos/Efficient%20triangle%E2%80%93triangleintersectiontestforOBB.pdf)]
  * A fast triangle to triangle intersection test for collision detection (2006), O. Tropp et al. [[pdf](http://webee.technion.ac.il/~ayellet/Ps/TroppTalShimshoni.pdf), [code](http://webee.technion.ac.il/labs/cgm/Computer-Graphics-Multimedia/Software/TriangleIntersection/code.cpp)]
    * A failure case was reported in [Stack Overflow](http://stackoverflow.com/a/29563443/3122234).
  * Faster Triangle-Triangle Intersection Tests (2006), O. Devillers et al. [[pdf](https://hal.inria.fr/inria-00072100/document), [code](https://github.com/CGAL/cgal/blob/076c982dbf37cc244206fd7962e73360fb17ea47/Intersections_3/include/CGAL/Triangle_3_Triangle_3_do_intersect.h)]
  * A Fast Triangle-Triangle Intersecion Test (1997), T. Muller. [[pdf](http://web.stanford.edu/class/cs277/resources/papers/Moller1997b.pdf), [code](https://github.com/erich666/jgt-code/blob/master/Volume_02/Number_2/Moller1997b/tritri_isectline.c)]

#### Mesh Collision

* Robust contact generation for robot simulation with unstructured meshes (2013), K. Hauser. [[pdf](https://motion.cs.illinois.edu/papers/ISRR2013-RobustContact.pdf), [web](http://motion.cs.illinois.edu/simulation/index.html)]

#### Penetration Depth Computation

* PolyDepth: Real-time Penetration Depth Computation using Iterative Contact-Space Projection (2012), C. Je et al. [[pdf](https://arxiv.org/pdf/1508.06181v1.pdf)]

#### Proximity Query / Signed Distance Field

* Hierarchical hp-Adaptive Signed Distance Fields (2016), D. Koschier et al. [[pdf](https://pdfs.semanticscholar.org/0dac/60f8ebf218a5510799cab4c74c5bb1f276e9.pdf), [video](https://youtu.be/x_Iq2yM4FcA)]
* Voxblox: Building 3d signed distance fields for planning (2016), H Oleynikova et al. [[pdf](https://www.research-collection.ethz.ch/bitstream/handle/20.500.11850/128028/eth-50485-01.pdf), [code](https://github.com/ethz-asl/voxblox)]
* Signed distance fields for polygon soup meshes (2014), H. Xu and Jernej Barbic. [[pdf](https://pdfs.semanticscholar.org/6247/71efeaff92c9826b9fa176e8c76a2def1d9f.pdf)]
* Fast Proximity Queries with Swept Sphere Volumes (1999), E. Larsen et al. [[pdf](https://www.researchgate.net/profile/Dinesh_Manocha/publication/2318075_Fast_Proximity_Queries_with_Swept_Sphere_Volumes/links/54ecdc250cf2465f53305253/Fast-Proximity-Queries-with-Swept-Sphere-Volumes.pdf), [web](http://gamma.cs.unc.edu/SSV/)]

#### Continuous Collision Detection

* Hierarchical and Controlled Advancement for Continuous Collision Detection of Rigid and Articulated Models (2013), M. Tang et al. [[pdf](http://graphics.ewha.ac.kr/C2A/TVCG13.pdf), [web](http://graphics.ewha.ac.kr/C2A/)]
* Efficient Geometrically Exact Continuous Collision Detection (2012), T. Brochu et al. [[pdf](https://www.researchgate.net/profile/Essex_Edwards/publication/254200434_Efficient_Geometrically_Exact_Continuous_Collision_Detection/links/5540dd8a0cf2322227304cce/Efficient-Geometrically-Exact-Continuous-Collision-Detection.pdf), [video](https://youtu.be/5bGPoMbXIzs)]
* C2A: Controlled Conservative Advancement for Continuous Collision Detection of Polygonal Models (2009), M. Tang et al. [[pdf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.500.7676&rep=rep1&type=pdf)]
* Continuous Collision Detection for Articulated Models using Taylor Models and Temporal Culling (2007), X. Zhang et al. [[pdf](https://hal.inria.fr/file/index/docid/390313/filename/SIGGRAPH2007.pdf), [web](http://graphics.ewha.ac.kr/CATCH/)]
* Interactive continuous collision detection for non-convex polyhedra (2006), X. Zhang et al. [[pdf](https://link.springer.com/content/pdf/10.1007/s00371-006-0060-0.pdf), [web](http://graphics.ewha.ac.kr/FAST/)]

#### Nearest Neighbor

* Faster cover tree (2015), M. Izbicki et al. [[pdf](http://proceedings.mlr.press/v37/izbicki15.pdf), [code](https://github.com/manzilzaheer/CoverTree)]
* Fast Approximate Nearest Neighbors with Automatic Algorithm Configuration (2009), M. Muja and D. Lowe. [[pdf](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.160.1721&rep=rep1&type=pdf), [code](https://github.com/mariusmuja/flann)]
* Cover Tree for Nearest Neighbor (2006), A. Beygelzimer et al. [[pdf](https://homes.cs.washington.edu/~sham/papers/ml/cover_tree.pdf), [web](http://hunch.net/~jl/projects/cover_tree/cover_tree.html), [code](https://github.com/DNCrane/Cover-Tree)]

####  Comprehensive Collision Detection Library

* FCL: A General Purpose Library for Collision and Proximity Queries (2012), J. Pan et al. [[pdf](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.259.2177&rep=rep1&type=pdf), [code](https://github.com/flexible-collision-library/fcl)]

#### Survey

* Collision Detection: A Survey (2007), S. Kockara et al. [[pdf](https://pdfs.semanticscholar.org/250e/296b4b4c1b7ac0229e57d6638fe81188121e.pdf)]
* 3D collision detection: a survey (2001), P. Jiménez et al. [[pdf](https://users.soe.ucsc.edu/~pang/161/w06/notes/jtt01.pdf)]

## [Books](#awesome-collision-detection)

* Real-Time Collision Detection, CRC Press 2004 ([amazon](http://www.amazon.com/Real-Time-Collision-Detection-Interactive-Technology/dp/1558607323/ref=sr_1_1?s=books&ie=UTF8&qid=1463804277&sr=1-1&keywords=real+time+collision+detection))
* Collision Detection in Interactive 3D Environments, CRC Press 2003 ([amazon](http://www.amazon.com/Collision-Detection-Interactive-Environments-Technology/dp/155860801X))

## [Articles](#awesome-collision-detection)

#### Overview & Tutorial

* [Video Game Physics Tutorial - Part II: Collision Detection for Solid Objects](https://www.toptal.com/game/video-game-physics-part-ii-collision-detection-for-solid-objects) by [Nilson Souto](https://www.toptal.com/resume/nilson-souto)
* [GPU Rigid Body Simulation](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/bullet/GDC2013_ErwinCoumans_GPU_rigid_body_simulation.pdf) (GDC 2013), Erwin Coumans
* [OpenCL accelerated rigid body and collision detection](http://www.cs.rpi.edu/~trink/RSS-2011/Presentations/coumans.pdf) (RSS 2011), Erwin Coumans
* [Contact Generation](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/bullet/GDC10_Coumans_Erwin_Contact.pdf) (GDC 2010), Erwin Coumans

#### Benchmark

* [spatial-collision-datastructures](https://github.com/ttvd/spatial-collision-datastructures) - Benchmark of various spatial data structures for collision detection.

#### Narrow-phase

* [Algorithm table for narrowphase algorithms](http://www.realtimerendering.com/intersections.html)
* [3D Collision detection](http://www.miguelcasillas.com/?mcportfolio=collision-detection-c) by [Miguel Casillas](http://www.miguelcasillas.com/?page_id=451)
* [Collision Detection](http://www.jeffreythompson.org/collision-detection/) ([code](https://github.com/jeffThompson/CollisionDetection)) by Jeff Thompson - This book explains the algorithms behind those collisions using basic shapes like circles, rectangles, and lines so you can implement them into your own projects.
* [Note: The Gibert-Jonson-Keerthi algorithm](http://realtimecollisiondetection.net/pubs/SIGGRAPH04_Ericson_GJK_notes.pdf) by Christer Ericson

#### Space Partitioning

* [Benchmark of various spatial data structures for collision detection](https://github.com/ttvd/spatial-collision-datastructures)
* Bounding volume heirarchy
  * [Bounding Volume Hierarchy Optimization through Agglomerative Treelet Restructuring](http://www.highperformancegraphics.org/wp-content/uploads/2015/Papers-Session1/apresentacao.pdf) ([paper](http://dl.acm.org/citation.cfm?id=2790065), [code](https://github.com/leonardo-domingues/atrbvh)) by Leonardo R. Domingues and Helio Pedrini.
  * [Dynamic AABB Tree](http://www.randygaul.net/2013/08/06/dynamic-aabb-tree/) by [Randy Gaul](http://www.randygaul.net/about/)
  * [Efficient BVH Construction via Approximate Agglomerative Clustering](http://dl.acm.org/citation.cfm?id=2492054) by Yan Gu et al. ([pdf](http://repository.cmu.edu/cgi/viewcontent.cgi?article=3602&context=compsci))
  * [Octree vs BVH](http://thomasdiewald.com/blog/?p=1488) by [Thomas Diewald](http://thomasdiewald.com/blog/?page_id=14)
  
#### SDF and Mesh Interaction

* [Local Optimization for Robust Signed Distance Field Collision](https://mmacklin.com/sdfcontact.pdf) by [Miles Macklin](http://blog.mmacklin.com/), Kenny Erleben, Matthias Müller, Nuttapong Chentanez, Stefan Jeschke, Zach Corse - a new method for collision detection, that allows fast cloth simulation

## [Other Awesome Lists](#awesome-collision-detection)

* [Awesome Robotics Libraries](https://github.com/jslee02/awesome-robotics-libraries) - This is a list of various libraris and software for robotics. It's also attempting to provide some comparisons for selected libraries and software.

## [Contributing](#awesome-collision-detection)

Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/master/CONTRIBUTING.md) first. Also, please feel free to report any error.

## [License](#awesome-collision-detection)

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)
