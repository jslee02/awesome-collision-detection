# Awesome Collision Detection

A curated list of collision detection open resources

#### Table of Contents
* [Libraries](#libraries)
* [Articles](#articles)
* [Books](#books)
* [Other Awesome Lists](#other-awesome-lists)
* [Contributing](#contributing)

## [Libraries](#awesome-collision-detection)

**Active**

> :warning: The following table is not complete. Please feel free to report if you find something incorrect or missing.

| Name | Shapes | Features | Languages | Licenses | Code | Popularity |
|:----:| ------ | -------- | --------- | -------- | ---- | ---------- |
| [Bullet](http://bulletphysics.org) | (todo) | (todo) | C++, Python | Zlib | [github](https://github.com/bulletphysics/bullet3) | ![bullet3](https://img.shields.io/github/stars/bulletphysics/bullet3.svg?style=social&label=Star&maxAge=2592000) |
| [ColDet](https://sourceforge.net/projects/coldet/) | (todo) | (todo) | (todo) | (todo) | (todo) | (todo) |
| [FCL](https://github.com/flexible-collision-library/fcl) | (todo) | (todo) | (todo) | (todo) | [github](https://github.com/flexible-collision-library/fcl) | ![fcl](https://img.shields.io/github/stars/flexible-collision-library/fcl.svg?style=social&label=Star&maxAge=2592000) |
| [libccd](https://github.com/danfis/libccd) | (todo) | (todo) | (todo) | (todo) | [github](https://github.com/danfis/libccd) | ![libccd](https://img.shields.io/github/stars/danfis/libccd.svg?style=social&label=Star&maxAge=2592000) |
| [ODE](http://www.ode.org/) | (todo) | (todo) | (todo) | C++, [Python](http://pyode.sourceforge.net/) | LGPL-2.1 or BSD-3-Clause | [bitbucket](https://bitbucket.org/odedevs/ode) | |
| [OZCollide](http://www.tsarevitch.org/ozcollide/) | (todo) | (todo) | (todo) | (todo) | (todo) | (todo) |
| [ReactPhysics3d](http://www.reactphysics3d.com/) | (todo) | (todo) | C++ | Zlib | [github](https://github.com/DanielChappuis/reactphysics3d) | ![reactphysics3d](https://img.shields.io/github/stars/DanielChappuis/reactphysics3d.svg?style=social&label=Star&maxAge=2592000) |
| qu3e | (todo) | (todo) | (todo) | Zlib | [github](https://github.com/RandyGaul/qu3e) | ![qu3e](https://img.shields.io/github/stars/RandyGaul/qu3e.svg?style=social&label=Star&maxAge=2592000) |

> Some libraries (e.g., ODE and Bullet) are physics engines that contain collision detection features, but they can be used just as collision detection libraries.

**Inactive**
* [OPCODE](http://www.codercorner.com/Opcode.htm) - Optimized Collision Detection.
* [GIMPACT](http://gimpact.sourceforge.net/) - A software library with tools for geometry processing and collision detection, focused on solving most common problems on Virtual Reality development.
* [SOLID](http://solid.sourceforge.net/) -  A library for collision detection of 3D objects undergoing rigid motion and deformation designed for interactive 3D graphics applications.

## [Books](#awesome-collision-detection)

* Real-Time Collision Detection, CRC Press 2004 ([amazon](http://www.amazon.com/Real-Time-Collision-Detection-Interactive-Technology/dp/1558607323/ref=sr_1_1?s=books&ie=UTF8&qid=1463804277&sr=1-1&keywords=real+time+collision+detection))
* Collision Detection in Interactive 3D Environments, CRC Press 2003 ([amazon](http://www.amazon.com/Collision-Detection-Interactive-Environments-Technology/dp/155860801X))

## [Articles](#awesome-collision-detection)

* Overview & Tutorial

  * [Video Game Physics Tutorial - Part II: Collision Detection for Solid Objects](https://www.toptal.com/game/video-game-physics-part-ii-collision-detection-for-solid-objects) by [Nilson Souto](https://www.toptal.com/resume/nilson-souto)
  * [GPU Rigid Body Simulation](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/bullet/GDC2013_ErwinCoumans_GPU_rigid_body_simulation.pdf) (GDC 2013), Erwin Coumans
  * [OpenCL accelerated rigid body and collision detection](http://www.cs.rpi.edu/~trink/RSS-2011/Presentations/coumans.pdf) (RSS 2011), Erwin Coumans
  * [Contact Generation](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/bullet/GDC10_Coumans_Erwin_Contact.pdf) (GDC 2010), Erwin Coumans

* Benchmark
  * [spatial-collision-datastructures](https://github.com/ttvd/spatial-collision-datastructures) - Benchmark of various spatial data structures for collision detection.

* Narrow-phase

  * [Algorithm table for narrowphase algorithms](http://www.realtimerendering.com/intersections.html)
  * [3D Collision detection](http://www.miguelcasillas.com/?mcportfolio=collision-detection-c) by [Miguel Casillas](http://www.miguelcasillas.com/?page_id=451)
  * [Collision Detection](http://www.jeffreythompson.org/collision-detection/) ([code]()) by Jeff Thompson - This book explains the algorithms behind those collisions using basic shapes like circles, rectangles, and lines so you can implement them into your own projects.
  * [Note: The Gibert-Jonson-Keerthi algorithm](http://realtimecollisiondetection.net/pubs/SIGGRAPH04_Ericson_GJK_notes.pdf) by Christer Ericson

* Triangle-triangle test

  * A faster triangle-to-triangle intersection test algorithm (2013), L.-Y. Wei.
  * Efficient triangle-triangle intersection test for OBB-based collision detection (2009), J.-W. Chang et al. ([pdf](http://ldc.usb.ve/~vtheok/cursos/ci6322/escogidos/Efficient%20triangle%E2%80%93triangleintersectiontestforOBB.pdf))
  * A fast triangle to triangle intersection test for collision detection (2006), O. Tropp et al. ([pdf](http://webee.technion.ac.il/~ayellet/Ps/TroppTalShimshoni.pdf) | [code](http://webee.technion.ac.il/labs/cgm/Computer-Graphics-Multimedia/Software/TriangleIntersection/code.cpp))
    * [A failure case was reported in SO](http://stackoverflow.com/a/29563443/3122234).
  * Faster Triangle-Triangle Intersection Tests (2006), O. Devillers et al. ([pdf](https://hal.inria.fr/inria-00072100/document) | [code](https://github.com/CGAL/cgal/blob/076c982dbf37cc244206fd7962e73360fb17ea47/Intersections_3/include/CGAL/Triangle_3_Triangle_3_do_intersect.h))
  * A Fast Triangle-Triangle Intersecion Test (1997), T. Muller. ([pdf](http://web.stanford.edu/class/cs277/resources/papers/Moller1997b.pdf) | [code](https://github.com/erich666/jgt-code/blob/master/Volume_02/Number_2/Moller1997b/tritri_isectline.c))

* Space partitioning

  * [Benchmark of various spatial data structures for collision detection](https://github.com/ttvd/spatial-collision-datastructures)
  * Bounding volume heirarchy
    * [Bounding Volume Hierarchy Optimization through Agglomerative Treelet Restructuring](http://www.highperformancegraphics.org/wp-content/uploads/2015/Papers-Session1/apresentacao.pdf) ([paper](http://dl.acm.org/citation.cfm?id=2790065), [code](https://github.com/leonardo-domingues/atrbvh)) by Leonardo R. Domingues and Helio Pedrini.
    * [Dynamic AABB Tree](http://www.randygaul.net/2013/08/06/dynamic-aabb-tree/) by [Randy Gaul](http://www.randygaul.net/about/)
    * [Efficient BVH Construction via Approximate Agglomerative Clustering](http://dl.acm.org/citation.cfm?id=2492054) by Yan Gu et al. ([pdf](http://repository.cmu.edu/cgi/viewcontent.cgi?article=3602&context=compsci))
    * [Octree vs BVH](http://thomasdiewald.com/blog/?p=1488) by [Thomas Diewald](http://thomasdiewald.com/blog/?page_id=14)

* Mesh collision

  * K. Hauser, [Robust contact generation for robot simulation with unstructured meshes](http://motion.pratt.duke.edu/simulation/index.html), ISRR 2013  ([pdf](http://motion.pratt.duke.edu/papers/ISRR2013-RobustContact.pdf))

* Penetration depth computation

  * C. Je, M. Tang, Y. Lee, M. Lee, and Y Kim, PolyDepth: Real-time Penetration Depth Computation using Iterative Contact-Space Projection, TOG 2012 ([pdf](https://arxiv.org/pdf/1508.06181v1.pdf))

* Nearest neighbor
  
  * Cover tree
    * [Wikipedia](https://en.wikipedia.org/wiki/Cover_tree)
    * [Cover Tree for Nearest Neighbor caclulations](http://hunch.net/~jl/projects/cover_tree/cover_tree.html) by Alina Beygelzimer et al, ICML 2006.
    * https://github.com/DNCrane/Cover-Tree
  * Faster cover tree
    * [Faster cover tree](http://machinelearning.wustl.edu/mlpapers/paper_files/icml2015_izbicki15.pdf) by Mike Izbicki et al., ICML 2015.
    * https://github.com/manzilzaheer/CoverTree
  * [FLANN - Fast Library for Approximate Nearest Neighbors](http://www.cs.ubc.ca/research/flann/) ([github](https://github.com/mariusmuja/flann)) 

## [Other Awesome Lists](#awesome-collision-detection)

* [Awesome Robotics Libraries](https://github.com/jslee02/awesome-robotics-libraries) - This is a list of various libraris and software for robotics. It's also attempting to provide some comparisons for selected libraries and software.

## [Contributing](#awesome-collision-detection)

Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/master/CONTRIBUTING.md) first. Also, please feel free to report any error.

## [License](#awesome-collision-detection)

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)
