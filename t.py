axes = Axes(
    # x-axis ranges from -1 to 10, with a default step size of 1
    x_range=(-1, 10),
    # y-axis ranges from -2 to 2 with a step size of 0.5
    y_range=(-2, 2, 0.5),
    # The axes will be stretched so as to match the specified
    # height and width
    height=6,
    width=10,
    # Axes is made of two NumberLine mobjects.  You can specify
    # their configuration with axis_config
    axis_config={
        "stroke_color": GREY_A,
        "stroke_width": 2,
    },
    # Alternatively, you can specify configuration for just one
    # of them, like this.
    y_axis_config={
        "include_tip": False,
    }
)
# Keyword arguments of add_coordinate_labels can be used to
# configure the DecimalNumber mobjects which it creates and
# adds to the axes
axes.add_coordinate_labels(
    font_size=20,
    num_decimal_places=1,
)
self.add(axes)

dot = Dot(color=RED)
dot.move_to(axes.c2p(0, 0))
self.play(FadeIn(dot, scale=0.5))
self.play(dot.animate.move_to(axes.c2p(3, 2)))
self.wait()
self.play(dot.animate.move_to(axes.c2p(5, 0.5)))

start = [0, 0, 0]
end = [1, 1, 0]

point = Dot(start)
trail = DashedLine(start, start, dash_length=.15)

self.play(GrowFromCenter(point))
self.play(AnimationGroup(
    MoveToTarget(point, end),
    MoveToTarget(trail, end),
    lag_ratio=.5
))







d1 = Dot().set_color(ORANGE)
l1 = Line(LEFT, RIGHT)
l2 = VMobject()
#line_ = Line(LEFT, d1.get_center()).set_color(ORANGE)
#self.add(d1, l1, l2)
#l2.add_updater(lambda x: x.become(line_))
self.play(MoveAlongPath(d1, l1), rate_func=linear)