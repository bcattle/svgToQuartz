#!/usr/bin/env python

# Quote button background
# svg_str = 'c 1.97942,-0.6032 3.70962,-1.8525 4.601811,-3.32 0.97707,-1.6047 1.32383,-3.901 1.32383,-8.8184 0,-5.3405 0.14448,-4.9659 -1.94873,-4.9659 -3.579702,0.028 -6.316985,0.05 -10.0849708,0.073 l 0,4.3111 c 0,4.9483 -0.18783,4.7049 3.4820598,4.5855 1.18116,-0.044 2.25576,0.015 2.38399,0.1179 0.12642,0.1033 0.10836,0.9292 0,1.8318 -0.28897,1.8672 -1.35815,3.0058 -2.82647,3.0058 -0.87413,0 -0.90122,0.059 -0.90122,1.8761 l 0,1.8761 1.04932,0 c 0.57432,0 1.89815,-0.2596 2.93663,-0.5767 z'
# Quote box
# svg_str = 'c -4.20267,0 -7.58358,2.8936 -7.58358,6.4968 l 0.0361,15.3934 -3.46581,5.8848 6.48009,-1.3378 c 1.27146,0.8068 2.84092,1.2788 4.54221,1.2788 l 239.39316,0 c 4.20087,0 7.58359,-2.8923 7.58359,-6.4954 l 0,-14.7238 c 0,-3.6032 -3.38272,-6.4968 -7.58359,-6.4968 z'
# Paw
svg_str = 'M 49.082979,-4.53 C 39.947541,-4.980515 29.925991,4.0260961 19.976242,0.0368 10.026493,-3.9524961 7.9875976,-15.361247 15.431139,-20.8672 c 7.443541,-5.505953 16.105385,-5.739956 20.00904,-12.3051 3.903655,-6.565144 6.36614,-8.519 9.45891,-9.6008 3.63458,-1.1309 6.36614,-1.2047 10.00825,-0.3074 5.45562,1.3584 7.27666,3.227 10.27921,8.9493 4.481031,11.470663 19.533584,9.441864 23.19202,18.7897 2.73165,8.187 -4.476171,16.4764082 -13.6428,16.8658 C 65.56914,1.9136918 58.218417,-4.079485 49.082979,-4.53 z m 25.28408,-37.9297 c 0,-5.6424 2.73156,-10.3382 7.27666,-14.3211 3.64208,-3.2515 6.37364,-4.5545 9.82762,-4.5545 1.82104,0 2.72406,-0.3073 2.72406,-2.6922 0,-1.4813 0.91052,-4.4253 0.91052,-6.5275 l 0,-3.8231 1.82104,1.6227 c 2.73156,2.2311 3.642171,8.6911 2.73156,13.2394 0,1.8378 -0.91052,5.3966 -1.82095,7.892 -1.82113,11.162 -11.188033,20.9287 -16.874011,19.3583 -5.685979,-1.5705 -6.596499,-4.7543 -6.596499,-10.194 z M 2.149545,-51.624 c 0,-2.5016 -0.91061,-6.0542 -1.82103897,-7.892 -0.91052,-5.2121 0,-13.3746 3.63449297,-14.186 0.91061,-0.3073 0.91061,0.4303 0.91061,3.7371 0,2.2435 0,5.1015 0,6.3554 0,1.9853 0.910519,2.2742 2.731559,2.2742 3.642077,0 6.366141,1.2846 9.82012,4.5545 5.463116,4.9725 9.097701,13.0673 7.276661,19.2629 -0.903025,4.4378 -6.366143,6.1034 -11.321354,3.3806 -4.95521,-2.7229 -9.959321,-10.0495 -11.23105,-17.4867 z m 52.027874,-8.0026 c -2.185426,-6.461285 0.91052,-20.7442 5.45562,-23.7929 1.82104,-1.3583 2.73156,-2.3664 4.55269,-8.396 1.81354,-7.4986 1.81354,-7.6031 3.63449,1.9484 0,3.5711 0.91061,4.9479 2.73165,6.38 4.54511,3.8231 6.36614,8.3469 6.36614,16.2512 0,8.6726 -3.64207,15.3968 -9.09779,17.2039 -5.932546,2.264682 -11.457374,-3.133315 -13.6428,-9.5946 z m -22.19122,-24.8193 c 1.81345,-1.8316 2.72406,-2.8704 3.63458,-8.0088 0,-3.2515 0.91052,-5.9067 1.82104,-5.9067 0,0 0.91052,2.5138 0.91052,5.5932 0.91052,5.1876 0.91052,5.7162 3.63458,7.4925 3.64208,2.3541 4.5526,4.3886 6.36614,9.1889 4.944668,13.959822 -7.418399,33.233595 -18.3723,21.8568 -3.89889,-4.2273 -7.092355,-22.1088 2.00544,-30.2159 z'

absolute_origin_x = 0.0
absolute_origin_y = 0.0
currX = 0.0
currY = 0.0

# Are we outputting commands that draw to context
# or are we creating a CGPathRef?
DRAW_TO_PATH = True

contextref_name = 'context'
path_name = 'path'
# Path commands let you specify an affine transform:
pathref_transform_name = 'rectTransform'


class Point(object):
    def __init__(self, s):
        """
        :param s: Expects a string of the form  `1.97942,-0.6032`
        """
        x_str, y_str = s.split(',')
        self.x = float(x_str)
        # Coming form inkscape, we invert all y-values
        self.y = float(y_str)

    def __repr__(self):
        print '<Point x: %f, %f>' % (self.x, self.y)


class Command(object):
    def __init__(self, command_str, x_points, y_points):
        self.command_str = command_str
        self.x_points = x_points
        self.y_points = y_points

    def smallest_y(self):
        if self.y_points:
            return min(self.y_points)
        else:
            return 0.0

    def add_y_offset(self, offset):
        self.y_points = [y_val + offset for y_val in self.y_points]

    def __repr__(self):
        s = '%s(%s, ' % (self.command_str, contextref_name)
        for point in zip(self.x_points, self.y_points):
            s += '%.2ff, %.2ff, ' % (point[0], point[1])
        s =  s[:-2] + ');'
        return s


class PathCommand(Command):
    """
    Adds the path name and extra affine transform argument
    """
    def __init__(self, command_str, x_points, y_points, transform=True):
        self.command_str = command_str
        self.x_points = x_points
        self.y_points = y_points
        self.transform = transform

    def __repr__(self):
        if self.transform:
            s = '%s(%s, &%s, ' % (self.command_str, path_name, pathref_transform_name)
        else:
            s = '%s(%s, ' % (self.command_str, path_name)
        for point in zip(self.x_points, self.y_points):
            s += '%.2ff, %.2ff, ' % (point[0], point[1])
        s =  s[:-2] + ');'
        return s


def get_objc_for_C(iterator, prev_value=None):
    # curveto command, absolute coordinates
    global currX, currY
    prev_value = prev_value or iterator.next()

    # pull off three points
    ctrl1 = Point(prev_value)
    ctrl2 = Point(iterator.next())
    pt = Point(iterator.next())

    # end point becomes currX, currY?
    currX = pt.x
    currY = pt.y

    if DRAW_TO_PATH:
        return PathCommand('CGPathAddCurveToPoint',
                   x_points=[ctrl1.x, ctrl2.x, pt.x],
                   y_points=[ctrl1.y, ctrl2.y, pt.y])
    else:
        return Command('CGContextAddCurveToPoint',
                   x_points=[ctrl1.x, ctrl2.x, pt.x],
                   y_points=[ctrl1.y, ctrl2.y, pt.y])


def get_objc_for_c(iterator, prev_value=None):
    # curveto command
    # lowercase c means relative coordinates
    # syntax is: c <ctrl1 x> <ctrl1 y> <ctrl2 x> <ctrl2 y> <x> <y>
    global currX, currY

    prev_value = prev_value or iterator.next()

    # pull off three points
    ctrl1 = Point(prev_value)
    ctrl2 = Point(iterator.next())
    pt = Point(iterator.next())

    # convert relative to absolute
    # all points are relative to currX, currY
    ctrl1_x = ctrl1.x + currX
    ctrl2_x = ctrl2.x + currX
    pt_x = pt.x + currX

    ctrl1_y = ctrl1.y + currY
    ctrl2_y = ctrl2.y + currY
    pt_y = pt.y + currY

    currX = pt_x
    currY = pt_y

    if DRAW_TO_PATH:
        return PathCommand('CGPathAddCurveToPoint',
                   x_points=[ctrl1_x, ctrl2_x, pt_x],
                   y_points=[ctrl1_y, ctrl2_y, pt_y])
    else:
        return Command('CGContextAddCurveToPoint',
                   x_points=[ctrl1_x, ctrl2_x, pt_x],
                   y_points=[ctrl1_y, ctrl2_y, pt_y])


def get_objc_for_l(iterator, prev_value=None):
    # lineto command
    # lowercase means relative coordinates
    # syntax is: l <x> <y>
    global currX, currY

    prev_value = prev_value or iterator.next()

    # pull off one point
    pt = Point(prev_value)

    # convert relative to absolute
    pt_x = pt.x + currX
    pt_y = pt.y + currY
    currX = pt_x
    currY = pt_y

    if DRAW_TO_PATH:
        return PathCommand('CGPathAddLineToPoint', [pt_x], [pt_y])
    else:
        return Command('CGContextAddLineToPoint', [pt_x], [pt_y])


def get_objc_for_M(iterator, prev_value=None):
    # moveto command, absolute coordinates
    global currX, currY
    prev_value = prev_value or iterator.next()

    # pull off one point
    pt = Point(prev_value)
    # currX, currY becomes this point
    currX = pt.x
    currY = pt.y

    if DRAW_TO_PATH:
        return PathCommand('CGPathMoveToPoint', [pt.x], [pt.y])
    else:
        return Command('CGContextMoveToPoint', [pt.x], [pt.y])


def get_objc_for_m(iterator, prev_value=None):
    # moveto command
    # lowercase means relative coordinates
    # syntax is: m <x> <y>
    global currX, currY

    prev_value = prev_value or iterator.next()

    # pull off one point
    pt = Point(prev_value)

    # convert relative to absolute
    pt_x = pt.x + currX
    pt_y = pt.y + currY
    currX = pt_x
    currY = pt_y

    if DRAW_TO_PATH:
        return PathCommand('CGPathMoveToPoint', [pt_x], [pt_y])
    else:
        return Command('CGContextMoveToPoint', [pt_x], [pt_y])


def get_objc_for_z():
    if DRAW_TO_PATH:
        return PathCommand('CGPathCloseSubpath', [], [], transform=False)
    else:
        return Command('CGContextClosePath', [], [])


# import ipdb
# ipdb.set_trace()

objc_commands = []
last_command = ''
substrs = iter(svg_str.split(' '))
substr = ''
first_iteration = True
while True:
    # print 'loop. x: %.2f y: %.2f' % (currX, currY)
    try:
        #index, substr = substrs.next()
        substr = substrs.next()
        if substr == 'c':
            # curveto command
            # lowercase c means relative coordinates
            # syntax is: c <ctrl1 x> <ctrl1 y> <ctrl2 x> <ctrl2 y> <x> <y>
            last_command = substr
            objc_commands.append(get_objc_for_c(substrs))
        elif substr == 'C':
            # curveto command
            # lowercase c means relative coordinates
            # syntax is: c <ctrl1 x> <ctrl1 y> <ctrl2 x> <ctrl2 y> <x> <y>
            last_command = substr
            objc_commands.append(get_objc_for_C(substrs))
        elif substr == 'l':
            # lineto command
            # lowercase means relative coordinates
            # syntax is: l <x> <y>
            last_command = substr
            # objc_commands.append(get_objc_for_l(substrs, currX, currY))
            objc_commands.append(get_objc_for_l(substrs))
        elif substr == 'm':
            last_command = substr
            # If this is the first iteration, set the absolute origin
            # moveto_str = None
            # if first_iteration:
            #     moveto_str = substrs.next()
            #     abs_origin_pt = Point(moveto_str)
            #     absolute_origin_x = abs_origin_pt.x
            #     absolute_origin_y = abs_origin_pt.y
            # objc_commands.append(get_objc_for_m(substrs, prev_value=moveto_str))
            objc_commands.append(get_objc_for_m(substrs))
        elif substr == 'M':
            last_command = substr
            # # Set currX and currY to the difference between this point
            # # and the absolute origin
            # abs_moveto_pt = Point(substrs.next())
            # currX = abs_moveto_pt.x
            # currY = abs_moveto_pt.y
            objc_commands.append(get_objc_for_M(substrs))
        elif substr == 'z':
            # closepath command
            last_command = substr
            objc_commands.append(get_objc_for_z())
        else:
            # No command specified, we need to continue the previous command
            # BUT we already consumed one value from the iterator, so need to pass it
            if last_command == 'c':
                objc_commands.append(get_objc_for_c(substrs, prev_value=substr))
            elif last_command == 'C':
                objc_commands.append(get_objc_for_C(substrs, prev_value=substr))
            elif last_command == 'l':
                objc_commands.append(get_objc_for_l(substrs, prev_value=substr))
            elif last_command == 'm':
                objc_commands.append(get_objc_for_m(substrs, prev_value=substr))
            elif last_command == 'M':
                objc_commands.append(get_objc_for_M(substrs, prev_value=substr))
            else:
                print 'ERROR unknown command %s at position %d' % (substr, svg_str.find(substr))
        first_iteration = False
    except StopIteration:
        break
    except:
        print 'ERROR current substr: %s' % substr
        raise

# Go through the commands and find the smallest y-value
# add that as an offset to all points
# smallest_y = 0
# for command in objc_commands:
#     curr_smallest = command.smallest_y()
#     if curr_smallest < smallest_y:
#         smallest_y = curr_smallest
#
# for command in objc_commands:
#     command.add_y_offset(-smallest_y)

print ''
for command in objc_commands:
    print command

