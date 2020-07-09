# LowPolyfy
Low-poly object representations have become very popular art style in recent years. This artistic technique decomposes an image into a mesh of connected polygons. Delaunay triangulation is a well known algorithm which can perform this abstraction. Typical algorithms for creating low-poly image representations involve feature detection followed by Delaunay triangulation.

![Parakeet](https://i.imgur.com/uTHlhGl.jpg) ![Parakeet Low Poly](https://i.imgur.com/8mc7zi2.png)

This methodology has also been applied for videos, which performs feature detection and Delaunay triangulation on a frame-by-frame basis. This technique poses an issue of frame coherence in the resulting video approximations. Between each frame, the same features in a scene may not always be detected. As a result, the computed triangulations can vary, results in unintended flickering effects. A proposed solution for this problem is to perform Delaunay tetrahedralization across the input video footage in temporal space.

LowPolyfy is an application which creates low-poly approximations of video footage using Delaunay tetrahedralization.

For this research project, I will do two things:
1) Design a framework which can create low-poly approximations based on a specified point-placement algorithm
2) Investigate and design several point placement modules.

## Installation:
1. Clone the repository
2. Use a virtual environment
```
python -m venv venv
```
```
. /venv/bin/activate (linux)
.\venv\Scripts\activate (win)
```
3. Install the project dependencies in editable state
```
pip install -r requirements.txt -e .
```

## Running:
python lowpolyfy -s [SOURCE] -a [ALGORITHMNAME] -n [NUMPOINTS]

## Running Tests
python -m unittest discover -v
