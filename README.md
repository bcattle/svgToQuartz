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

Right now there is no good, robust tool to convert the SVG output from a program like [Inkscape](http://inkscape.org/) or Adobe Illustrator 
into Apple Quartz2D vector commands. 

Such a tool should exist, because SVG is an extremely simple format and its commands map almost 1:1 to Quartz. 
Even the order of parameters is nearly identical, as in mapping from `c` to `CGContextAddCurveToPoint`.

The goal is that it becomes much easier to generate crisp, resizable vector graphics rather than mainaining a forest of 
PNG files of various sizes. 


SVG commands that are supported
--------------
This script specifically parses the contents of the `<path d="">` attribute. Other features (colors, simple shapes) will be needed on an as-needed basis. Feel free to propose any improvements. 

Commands that work so far:
* `m`: move to point, relative coordinates
* `c`: add cubic bezier curve, relative coordinates
* `l`: add line, relative coordinates
* `z`: close path

These commands appear to cover most common output from Inkscape.


References 
--------------

The SVG format
* [Mozilla description](https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d) of the `path` `d`-attribute
* W3's [formal discription](http://www.w3.org/TR/SVG/paths.html#DAttribute) of the `path` `d`-attribute 
* A more readable [tutorial](http://tutorials.jenkov.com/svg/path-element.html)


There are a couple links online that attempt to offer this functionality, but I wasn't able to get them to work well or at all
* "[Convert SVG Path Data to IOS graphics](http://yepher.com/svg2ios.html)". Doesn't work.  
* The [Quarkee Lite](http://wavecoders.ca/productsDefault.cfm?prod=2) app, $4.99 in the [Mac App Store](https://itunes.apple.com/app/qwarkee/id498340809). Didn't work for me. 
* [Paintcode](https://itunes.apple.com/us/app/paintcode/id507897570?mt=12), a graphics editor that outputs Quartz commands. $99. I haven't used it. 
* A [blog post](http://rdsquared.wordpress.com/2012/01/10/svg-to-coregraphics-conversion/) from Ryan Dillon on the issue
* Another [blog post](http://blog.mikeswanson.com/post/19874621055/smaller-apps-with-vector-images) discussing this. The author appears to have gotten great results but unfortunately didn't release any code. 

The [SVGKit](https://github.com/SVGKit/SVGKit) library renders an SVG natively. Looks nice, and appears to suport 90% of the SVG standard, but was overkill for my use case. I also disagree with interpreting the file at run time, there's no reason no to *compile* the SVG into native drawing commands, rather than deal with XML parsing and validation in the draw cycle.  Here's another article on [using](http://t-machine.org/index.php/2012/12/31/svgkit-2013-usage/) SVGKit. 


Where to go from here
-----------------------

Add support for more commands, multiple paths, colors.
Make this an Inkscape plugin: "export directly to Quartz"?

