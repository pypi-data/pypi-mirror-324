#! /usr/bin/env python

from solid2 import cube, text, translate, union, scad_render_to_file, scad_inline, \
                   CustomizerDropdownVariable, CustomizerSliderVariable, \
                   scad_for, scad_range

#register all the custom variables you want to use
objects = CustomizerDropdownVariable("objects", 4, [2, 4, 6])
side = CustomizerSliderVariable("side", 4)
cube_pos = CustomizerSliderVariable("cube_pos", [5, 5, 5])
cube_size = CustomizerSliderVariable("cube_size", 5)
customizedText = CustomizerDropdownVariable("text", "customize me!",
                                            ["customize me!", "Thank you!"])

#use scad_inline to use them
scene = scad_for(scad_range(1, objects), lambda i: cube(side).left(2*i*side))

scene += cube(cube_size * 2).translate(cube_pos)
scene += text(customizedText).back(20) #type: ignore

scad_render_to_file(scene)

