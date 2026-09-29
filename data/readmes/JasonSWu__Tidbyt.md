# Tidbyt
App(s) for Tidbyt clock

Run the parent folder of the main starlark file, not the file itself
For a folder "a", the main file must be "a.star"

Animate kirby moving up and down with the animation transformation. I think ease in is the best one or maybe in and out

A frame is 50 ms

animation.Transformation duration is in units of frames

When stacking an animation.Transformation with a render.Animation, the animation.Transformation doesn't start again until the render.Animation
is finished. The solution here is to make the animation.Transformation duration the same as the number of frames in the render.Animation,
then just generate a crap ton of intermediate key frames which make kirby oscillate.

# TODO
- make the sparkles stay at their current level after leaving the star. Can't do this in starlark.
    Need to make new kirby_star_sparkles frames using python. It's pretty different working with frames (strict 50ms each)
    themselves rather than the more flexible keyframes though. Especially the curves in animation.Transformation.
    
    + This is probably possible if I rewrite the logic for animation.Transformation and render.Stack

- make another daytime animation of kirby sitting on a truck driving down the road. Truck might not be able to have enough detail
    in a 64 x 32 png