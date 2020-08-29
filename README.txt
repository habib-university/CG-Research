Specification of different files


constants.py : Contains different constants which are used throughout the program.

fragment.py: This file implements the fragment class, which is assumed as equivalent to pixel right now.

fragment_processing.py : Contains code for fragment processing stage of the pipeline. 
Three operations can be performed which are blending, alpha test, depth test.

fragment_shader.py: Contains code for fragment shader stage of pipeline.
It sets colors according to the color specified in programmable fragment shader.

frame_buffer.py: Contains code for framebuffer where pixels that need to be rendered are stored.
Operations on framebuffer are also defined in this file (set pixels, depth etc.).
Double buffering is also implemented (which can be enabled by pressing 'D' key). 

helpers.py : Different helper functions which aid in calculations and conversions throughout the program.

main.py : Sets screen and refresh rates, updates the renders on screen and runs main program.

primitive.py : Primitives (line and point) are implemented in this file.
Their drawing calculations are also performed within their respective classes.

program.py : Links different stages of the pipeline and runs the program.
This can be thought of as the gl context which links everything in a typical WebGL program.

rasterizer.py : Contains code for rasterizer stage of pipeline. Lights up vertices for primitives which need to be colored.

tests.py : Contains unit tests for different possible cases (that I could think of!)

user_program.py : Contains the code that the user can write for the pipeline.
	All the colors defined by the user should be in the range of 0 to 1.
	Following are the required functions in user program. The MUST be defined else the program will not run and will throw errors.
	- init()
	Declare global variables which will be constant throughout the program
	(declaring global variables is necessary, you can only change screen resolution, block size or margin)
	- render()
	This function will have the draw_arrays function which renders primitives from vertices array data.
	draw_arrays function: draw_arrays(primitive, first, count)
    	primitive can be either "POINT" or "LINE", first is the starting index in vertices array,
    	count is the number of vertices to be rendered
	- main_program()
	This is the main program where user will specify what he wants in his render.
	The user is required to specify background color, add fragment shader, and specify vertices and colors that need to be rendered.  
	If the background color is not specified, all the pixels will be rendered as black (default color).
	The user can also enable fragment processing tests by using program.enable_test("test name"),
	and then calling the specified test function. 
	Valid test names are "blend" for blending, "depth" for depth test, and "alpha" for alpha test.
	program.blend_func(src, dst), program.depth_func(), program.alpha_func(const, ref) are the test functions respectively.
	Please look at the sample test before enabling blending because you need to render simple primitives first (base image)
	and then apply blending on top of it by rendering other primitives.
	Blending and depth tests should not be enabled at the same time as that is not possible (it will either throw an error or render incorrect image).
	- write_fragmentShader()
	Fragment shader consists of varying and uniform variables.
	For now, we are assuming that we don't have any uniforms variables and are providing varying variable (vColor)
	as well as color variable of fragment shader (fragColor) as an argument in the function. 
	Later, we may add other components in this function which helps specifying calculations regarding
	shading and texture etc. For now, we are only assigning color.
	If you want to specify color directly in fragment shader set fragColor = (your desired color).
	If you want to render colors based on the color array specified set fragColor = vColor.