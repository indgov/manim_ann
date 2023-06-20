from __future__ import annotations

from manimlib import *
#from dataclasses import dataclass
import numpy as np

#@dataclass
class Node:
     def __init__(self, split_pt, left, right, nums=None):
          self.split_pt = split_pt
          self.left = left
          self.right = right
          self.nums = nums

nums = [-4., -3.5, -3, -2.5, -2, -1.5, -1, -.5, 0, .5, 1., 1.5, 2., 2.5, 3., 3.5, 4]
node = Node(
    split_pt=0.,
    left=Node(
        -2,
        left=Node(
            -3,
            left=None,
            right=None,
            nums=nums[:5]
        ),
        right=Node(
            -1,
            left=None,
            right=None,
            nums=nums[5:9]
        )
    ),
    right=Node(
        2,
        left=Node(
            1,
            left=None,
            right=None,
            nums=nums[9:13]
        ),
        right=Node(
            3,
            left=None,
            right=None,
            nums=nums[13:]
        )
    )
)
tree_node = Node(
    split_pt=0.,
    left=Node(
        -3.6,
        left=Node(
            -4.6,
            left=None,
            right=None,
            nums=nums[:5]
        ),
        right=Node(
            -2.7,
            left=None,
            right=None,
            nums=nums[5:9]
        )
    ),
    right=Node(
        3.8,
        left=Node(
            2.9,
            left=None,
            right=None,
            nums=nums[9:13]
        ),
        right=Node(
            4.7,
            left=None,
            right=None,
            nums=nums[13:]
        )
    )
)

start_ht = 3.
lines, tree_lines = [], []

def dfs(node, lines, depth=1):
    lines.append(Line(
        [node.split_pt, start_ht - (depth - 1) * .5, 0.],
        [node.split_pt, start_ht - depth * .5, 0.]
    ))
    if node.left and node.left.split_pt:
            lines.append(Line(
                [node.split_pt, start_ht - depth * .5, 0.],
                [node.left.split_pt, start_ht - depth * .5, 0.],
            ))
            dfs(node.left, lines=lines, depth=depth + 1)
    if node.right and node.right.split_pt:
            lines.append(Line(
                [node.split_pt, start_ht - depth * .5, 0.],
                [node.right.split_pt, start_ht - depth * .5, 0.],
            ))
            dfs(node.right, lines=lines, depth=depth + 1)

dfs(node, lines=lines)
dfs(tree_node, lines=tree_lines)

paths = []

def dfs_path(node, num, searching=True, ix=0):
    if searching:
        paths.append(lines[ix])

    if node.left is None and node.right is None:
        return ix

    if node.left:
        ix += 1

        _searching = False
        if searching and num <= node.split_pt and node.left.split_pt:
            paths.append(lines[ix])
            _searching = True

        ix = dfs_path(node.left, num, searching=_searching, ix=ix + 1)

    if node.right:
        ix += 1

        _searching = False
        if searching and num > node.split_pt and node.right.split_pt:
            paths.append(lines[ix])
            _searching = True

        ix = dfs_path(node.right, num, searching=_searching, ix=ix + 1)

    return ix

#breakpoint()
num = -4
dfs_path(node, num)

class InteractiveDevelopment(Scene):
    def construct(self):
        nl2 = NumberLine([-6, 6], include_numbers=True)
        self.add(nl2)

        points = []
        for n in nums:
            point = Dot([n, 0., 0.])
            points.append(point)
            self.play(GrowFromCenter(point), run_time=.05)

        dot = Dot(lines[0].start).set_color(BLUE)
        self.play(GrowFromCenter(dot), run_time=.03)

        for line in lines:
            self.play(ShowCreation(line), run_time=.1)

        for i, path in enumerate(paths):
            self.play(MoveAlongPath(dot, path), rate_func=linear, run_time=.1)
            if i % 2 == 0:
                pass
                #self.wait(.5)


        curr = node
        while True:
            if curr.nums is not None:
                break
            if num <= curr.split_pt:
                curr = curr.left
            else:
                curr = curr.right
        
        dashed = []
        for n in curr.nums:
            dashed_line = DashedLine(paths[-1].end, [n, 0, 0])
            dashed.append(dashed_line)
            self.play(ShowCreation(dashed_line), run_time=.02)
            #self.wait(.3)

        for dashed_line in dashed:
            self.play(Uncreate(dashed_line), run_time=.02)


        #breakpoint()
        new_points = [-5, -4.8, -4.6, -4.4, -4.2, -3, -2.8, -2.6, -2.4, 2.6, 2.8, 3, 3.2, 4.4, 4.6, 4.8, 5]
        anims = []
        for point, new_point in zip(points, new_points):
            _, y, z = point.get_center()
            #self.play(point.animate.move_to([new_point, y, z]), run_time=.05)
            anims.append(ApplyMethod(point.move_to, [new_point, y, z]))
        
        self.play(AnimationGroup(*anims))

        #breakpoint()
        for path in paths[::-1]:
            self.play(MoveAlongPath(dot, Line(path.end, path.start)), rate_func=linear, run_time=.1)

        for path in paths[:3]:
            self.play(MoveAlongPath(dot, path), run_time=.1)

        #breakpoint()
        for path in paths[:3][::-1]:
            self.play(MoveAlongPath(dot, Line(path.end, path.start)), rate_func=linear, run_time=.1)


        anims = []

        for line, tree_line in zip(lines, tree_lines):
            anims.append(ApplyMethod(line.put_start_and_end_on, tree_line.start, tree_line.end))

        self.play(AnimationGroup(*anims))

        #l2 = VMobject()
        #line_ = Line(LEFT, d1.get_center()).set_color(ORANGE)
        #self.add(d1, l1, l2)
        #l2.add_updater(lambda x: x.become(line_))
        #self.play(MoveAlongPath(d1, l1), rate_func=linear)
        #self.wait()
        #self.play(MoveAlongPath(d1, l2), rate_func=linear)
        #self.play(MoveAlongPath(d1, l3), rate_func=linear)