# Documentation
## General Notes - Flow of pipeline (so far)
### 4th May 2020
#### Rasterizer
* Get vertices
* Calculate points of primitive
* Make fragments array
* Interpolation
* Send fragments to fragment shader
#### Fragment Shader
* Sends fragments array to fragment processing stage (for now)
#### Fragment Processing
* Alpha/ depth/ blending tests
* Passes fragments as pixels to buffer


## Meeting Minutes
### 5th May 2020
* Blending was working fine, we didnt call the functions properly Seperate function for drawing and a seperate file for Test cases is made
* Do not spend too much time optimizing things which do not yield so much value. 
* We have to take the compiler into account. does not need to be full on compiler but some part or restrict our shaders by always using atleast one varying attribute. 
* The fragment shader has to use atleast one of the varying attributes. 
* If fragment shader does not use varying attribute, all the work in rasterizer goes to waste.
* Cleaned up code and all the blending, alpha and depth tests working
* SHould research: about how the z values will be taken into account 
* Testing using top down approach
* Testing in python: using module pytest
* write test functions and then call eventual implementation
