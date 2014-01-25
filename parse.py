#!/usr/bin/env python

CONTEXTREF_NAME = 'context'
PATH_NAME = 'path'
PATH_TRANSFORM_NAME = 'rectTransform'


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
        print '<Point x: %.2f, y: %.2f>' % (self.x, self.y)

class Rect(object):
    def __init__(self, x0, y0, dx, dy):
        self.x0 = x0
        self.y0 = y0
        self.width = dx
        self.height = dy

    def __repr__(self):
        return 'CGRectMake(%.2f, %.2f, %.2f, %.2f)' % (self.x0, self.y0, self.width, self.height)


class Command(object):
    def __init__(self, command_str, x_points, y_points):
        self.command_str = command_str
        self.x_points = x_points
        self.y_points = y_points

    def get_geometry_point(self):
        """ This is sort of a hack, returns the point that *isn't*
        a control point. Is either the only point in the command, or the third point.
        """
        if self.x_points:
            if len(self.x_points) == 3:
                return self.x_points[2], self.y_points[2]
            else:
                return self.x_points[0], self.y_points[0]
        return None, None


    def add_xy_offset(self, offsetX, offsetY):
        self.y_points = [y_val + offsetY for y_val in self.y_points]
        self.x_points = [x_val + offsetX for x_val in self.x_points]

    def __repr__(self):
        s = '%s(%s, ' % (self.command_str, CONTEXTREF_NAME)
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
            s = '%s(%s, &%s, ' % (self.command_str, PATH_NAME, PATH_TRANSFORM_NAME)
        else:
            s = '%s(%s, ' % (self.command_str, PATH_NAME)
        for point in zip(self.x_points, self.y_points):
            s += '%.2ff, %.2ff, ' % (point[0], point[1])
        s =  s[:-2] + ');'
        return s


class SvgFormatter(object):
    """
    Generates the Obj-C syntax commands and keeps
    track of the path state - i.e. the current X and Y
    to convert relative coordinates
    """
    def __init__(self, draw_to_path=True):
        self.currX = 0.0
        self.currY = 0.0
        self.draw_to_path = draw_to_path


    def get_objc_for_C(self, iterator, prev_value=None):
        # curveto command, absolute coordinates
        prev_value = prev_value or iterator.next()

        # pull off three points
        ctrl1 = Point(prev_value)
        ctrl2 = Point(iterator.next())
        pt = Point(iterator.next())

        # end point becomes currX, currY?
        self.currX = pt.x
        self.currY = pt.y

        if self.draw_to_path:
            return PathCommand('CGPathAddCurveToPoint',
                       x_points=[ctrl1.x, ctrl2.x, pt.x],
                       y_points=[ctrl1.y, ctrl2.y, pt.y])
        else:
            return Command('CGContextAddCurveToPoint',
                       x_points=[ctrl1.x, ctrl2.x, pt.x],
                       y_points=[ctrl1.y, ctrl2.y, pt.y])


    def get_objc_for_c(self, iterator, prev_value=None):
        # curveto command
        # lowercase c means relative coordinates
        # syntax is: c <ctrl1 x> <ctrl1 y> <ctrl2 x> <ctrl2 y> <x> <y>
        prev_value = prev_value or iterator.next()

        # pull off three points
        ctrl1 = Point(prev_value)
        ctrl2 = Point(iterator.next())
        pt = Point(iterator.next())

        # convert relative to absolute
        # all points are relative to currX, currY
        ctrl1_x = ctrl1.x + self.currX
        ctrl2_x = ctrl2.x + self.currX
        pt_x = pt.x + self.currX

        ctrl1_y = ctrl1.y + self.currY
        ctrl2_y = ctrl2.y + self.currY
        pt_y = pt.y + self.currY

        self.currX = pt_x
        self.currY = pt_y

        if self.draw_to_path:
            return PathCommand('CGPathAddCurveToPoint',
                       x_points=[ctrl1_x, ctrl2_x, pt_x],
                       y_points=[ctrl1_y, ctrl2_y, pt_y])
        else:
            return Command('CGContextAddCurveToPoint',
                       x_points=[ctrl1_x, ctrl2_x, pt_x],
                       y_points=[ctrl1_y, ctrl2_y, pt_y])


    def get_objc_for_L(self, iterator, prev_value=None):
        # lineto command
        # absolute coordinates
        # syntax is: l <x> <y>
        prev_value = prev_value or iterator.next()

        # pull off one point
        pt = Point(prev_value)
        self.currX = pt.x
        self.currY = pt.y

        if self.draw_to_path:
            return PathCommand('CGPathAddLineToPoint', [pt.x], [pt.y])
        else:
            return Command('CGContextAddLineToPoint', [pt.x], [pt.y])


    def get_objc_for_l(self, iterator, prev_value=None):
        # lineto command
        # lowercase means relative coordinates
        # syntax is: l <x> <y>
        prev_value = prev_value or iterator.next()

        # pull off one point
        pt = Point(prev_value)

        # convert relative to absolute
        pt_x = pt.x + self.currX
        pt_y = pt.y + self.currY
        self.currX = pt_x
        self.currY = pt_y

        if self.draw_to_path:
            return PathCommand('CGPathAddLineToPoint', [pt_x], [pt_y])
        else:
            return Command('CGContextAddLineToPoint', [pt_x], [pt_y])


    def get_objc_for_M(self, iterator, prev_value=None):
        # moveto command, absolute coordinates
        prev_value = prev_value or iterator.next()

        # pull off one point
        pt = Point(prev_value)
        # currX, currY becomes this point
        self.currX = pt.x
        self.currY = pt.y

        if self.draw_to_path:
            return PathCommand('CGPathMoveToPoint', [pt.x], [pt.y])
        else:
            return Command('CGContextMoveToPoint', [pt.x], [pt.y])


    def get_objc_for_m(self, iterator, prev_value=None):
        # moveto command
        # lowercase means relative coordinates
        # syntax is: m <x> <y>
        prev_value = prev_value or iterator.next()

        # pull off one point
        pt = Point(prev_value)

        # convert relative to absolute
        pt_x = pt.x + self.currX
        pt_y = pt.y + self.currY
        self.currX = pt_x
        self.currY = pt_y

        if self.draw_to_path:
            return PathCommand('\nCGPathMoveToPoint', [pt_x], [pt_y])
        else:
            return Command('\nCGContextMoveToPoint', [pt_x], [pt_y])


    def get_objc_for_z(self):
        if self.draw_to_path:
            return PathCommand('CGPathCloseSubpath', [], [], transform=False)
        else:
            return Command('CGContextClosePath', [], [])


class SvgStringParser(object):
    def __init__(self):
        self.formatter = SvgFormatter()

    def get_bounding_box_for_commands(self, commands):
        geometry_x_points = []
        geometry_y_points = []
        for command in commands:
            curr_cmd_X, curr_cmd_Y = command.get_geometry_point()
            if curr_cmd_X is not None:
                geometry_x_points.append(curr_cmd_X)
                geometry_y_points.append(curr_cmd_Y)

        minX = min(geometry_x_points)
        maxX = max(geometry_x_points)
        minY = min(geometry_y_points)
        maxY = max(geometry_y_points)
        return Rect(minX, minY, maxX - minX, maxY - minY)


    def parse_string(self, svg_str):
        """
        Main loop
        """
        objc_commands = []
        last_command = ''
        substrs = iter(svg_str.split(' '))
        substr = ''

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
                    objc_commands.append(self.formatter.get_objc_for_c(substrs))
                elif substr == 'C':
                    # curveto command
                    # lowercase c means relative coordinates
                    # syntax is: c <ctrl1 x> <ctrl1 y> <ctrl2 x> <ctrl2 y> <x> <y>
                    last_command = substr
                    objc_commands.append(self.formatter.get_objc_for_C(substrs))
                elif substr == 'l':
                    # lineto command
                    # lowercase means relative coordinates
                    # syntax is: l <x> <y>
                    last_command = substr
                    objc_commands.append(self.formatter.get_objc_for_l(substrs))
                elif substr == 'L':
                    # lineto command
                    # absolute coordinates
                    # syntax is: l <x> <y>
                    last_command = substr
                    objc_commands.append(self.formatter.get_objc_for_L(substrs))
                elif substr == 'm':
                    # moveto command
                    # lowercase means relative coordinates
                    # syntax is: m <x> <y>
                    last_command = substr
                    objc_commands.append(self.formatter.get_objc_for_m(substrs))
                elif substr == 'M':
                    # moveto command
                    # absolute coordinates
                    last_command = substr
                    objc_commands.append(self.formatter.get_objc_for_M(substrs))
                elif substr == 'z':
                    # closepath command
                    last_command = substr
                    objc_commands.append(self.formatter.get_objc_for_z())
                else:
                    # No command specified, we need to continue the previous command
                    # BUT we already consumed one value from the iterator, so need to pass it
                    if last_command == 'c':
                        objc_commands.append(self.formatter.get_objc_for_c(substrs, prev_value=substr))
                    elif last_command == 'C':
                        objc_commands.append(self.formatter.get_objc_for_C(substrs, prev_value=substr))
                    elif last_command == 'l':
                        objc_commands.append(self.formatter.get_objc_for_l(substrs, prev_value=substr))
                    elif last_command == 'L':
                        objc_commands.append(self.formatter.get_objc_for_L(substrs, prev_value=substr))
                    elif last_command == 'm':
                        objc_commands.append(self.formatter.get_objc_for_m(substrs, prev_value=substr))
                    elif last_command == 'M':
                        objc_commands.append(self.formatter.get_objc_for_M(substrs, prev_value=substr))
                    else:
                        print 'ERROR unknown command %s at position %d' % (substr, svg_str.find(substr))
            except StopIteration:
                break
            except:
                print 'ERROR current substr: %s' % substr
                raise

        # Calculate the bounding box for the shape
        # excluding the control points
        bbox = self.get_bounding_box_for_commands(objc_commands)

        # Zero out the origin, subtract minX, minY from every point
        for command in objc_commands:
            command.add_xy_offset(-bbox.x0, -bbox.y0)

        # Double check, calculate it again
        bbox2 = self.get_bounding_box_for_commands(objc_commands)


        # Print the bounding box
        print ''
        print 'const CGRect pathRect = %s;' % bbox2
        print ''

        if self.formatter.draw_to_path:
            print 'CGAffineTransform %s = CGAffineTransformConcat(CGAffineTransformMakeScale(rect.size.width / pathRect.size.width,' % PATH_TRANSFORM_NAME
            print '                                                                                     rect.size.height / pathRect.size.height),'
            print '                                                          CGAffineTransformMakeTranslation(rect.origin.x - pathRect.origin.x,'
            print '                                                                                           rect.origin.y - pathRect.origin.y));'
            print ''
            print 'CGMutablePathRef %s = CGPathCreateMutable();' % PATH_NAME
            print ''

        # Print the commands
        for command in objc_commands:
            print command
        print ''

