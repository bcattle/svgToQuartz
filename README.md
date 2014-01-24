svgToQuartz
===========

A first attempt at a script that converts svg paths to Apple Quartz2D commands.

Converts 

```
m 8.36779,-42.4597 c 0,-5.6424 2.73156,-10.3382 7.27666,-14.3211 z
```

to 

``` objective-c
CGContextMoveToPoint(context, 8.36f, -42.45);
CGContextAddCurveToPoint(context, 0.00f, -5.64f, 2.73f, -10.33f, 7.28f, -14.32);
CGContextClosePath(context);
```

Right now there is no good, robust tool to convert the SVG output from a program like Inkscape or Adobe Illustrator 
into Apple Quartz2D vector commands. 

Such a tool should exist, because SVG is an extremely simple format and its commands map almost 1:1 to Quartz. 
Even the order of parameters is nearly identical, as in mapping from `c` to `CGContextAddCurveToPoint`.

The goal is that it becomes much easier to generate crisp, resizable vector graphics rather than mainaining a forest of 
PNG files of various sizes. 


SVG commands that are supported
--------------
This script specifically parses the contents of the `<path d="">` attribute. Other features (colors, simple shapes) will be needed on an as-needed basis. Feel free to propose any improvements. 

References 
--------------

The SVG format
* [Mozilla description](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d) of the `path` `d`-attribute
* W3's [formal discription](http://www.w3.org/TR/SVG/paths.html#DAttribute) of the `path` `d`-attribute 
* A more readable [tutorial](http://tutorials.jenkov.com/svg/path-element.html)


There are a couple links online that attempt to offer this functionality, but I wasn't able to get any of them to work well or at all
* 
* 

The following library 
