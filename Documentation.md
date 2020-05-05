# Documentation
## Flow of the pipeline (so far)
### Rasterizer
* Get vertices
* Calculate points of primitive
* Make fragments array
* Interpolation
* Send fragments to fragment shader
### Fragment Shader
* Sends fragments array to fragment processing stage (for now)
### Fragment Processing
* Alpha/ depth/ blending tests
* Passes fragments as pixels to buffer
