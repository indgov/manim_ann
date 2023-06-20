from __future__ import annotations

from manimlib import *
#from dataclasses import dataclass
import numpy as np
import random

random.seed(4)
np.random.seed(0)

def l2(p1, p2):
    return (p1 - p2) ** 2

def two_means(nums, anim_data=[], n_iters=200):
    #i, j = random.sample(range(len(nums)), k=2)
    #breakpoint()
    i, j = 0, 2
    centroid_i, centroid_j = nums[i], nums[j]
    n_i, n_j = 1, 1

    for _ in range(n_iters):
        point = random.choice(nums)

        distance_i = l2(point, centroid_i) #* n_i
        distance_j = l2(point, centroid_j) #*n_j

        centroid_i_prev, centroid_j_prev = centroid_i, centroid_j

        if distance_i < distance_j:
            centroid_i = (centroid_i * n_i + point) / (n_i + 1)
            n_i += 1
            
            
        if distance_i > distance_j:
            centroid_j = (centroid_j * n_j + point) / (n_j + 1)
            n_j += 1
        
        anim_data.append({
            "point": point,
            "centroid_i_prev": centroid_i_prev,
            "centroid_j_prev": centroid_j_prev,
            "centroid_i": centroid_i,
            "centroid_j": centroid_j 
        })
    
    return centroid_i, centroid_j
    

nums = [-4., -3.5, -3, -2.5, -2, -1.5, -1, -.5, 0, .5, 1., 1.5, 2., 2.5, 3., 3.5, 4]
nums = [-5, -4.8, -4.6, -4.4, -4.2, -3, -2.8, -2.6, -2.4, 2.6, 2.8, 3, 3.2, 4.4, 4.6, 4.8, 5]

class InteractiveDevelopment(Scene):
    def construct(self):
        nl2 = NumberLine([-6, 6], include_numbers=True)
        self.add(nl2)

        points = []
        for n in nums:
            point = Dot([n, 0., 0.])
            points.append(point)
            self.play(GrowFromCenter(point), run_time=.05)

        anim_data = []
        #breakpoint()
        two_means(nums, anim_data)

        centroid_i, centroid_j = anim_data[0]["centroid_i_prev"], anim_data[0]["centroid_j_prev"]
        centroid_i = Dot([centroid_i, 2, 0])
        centroid_j = Dot([centroid_j, 2, 0])
        self.play(GrowFromCenter(centroid_i), run_time=.05)
        self.play(GrowFromCenter(centroid_j), run_time=.05)

        for i, data in enumerate(anim_data):
            run_time = 1 / (i + 1)

            point = data["point"]
            centroid_i_prev = data["centroid_i_prev"]
            centroid_j_prev = data["centroid_j_prev"]
            centroid_i_next = data["centroid_i"]
            centroid_j_next = data["centroid_j"]

            #d = Dot([point, 0, 0])
            dl1 = Line([centroid_i_prev, 2, 0], [point, 0, 0])
            dl2 = Line([centroid_j_prev, 2, 0], [point, 0, 0])

            #self.play(GrowFromCenter(d))
            self.play(ShowCreation(dl1), run_time=run_time)
            self.play(ShowCreation(dl2), run_time=run_time)

            #d.fade()
            #breakpoint()

            anims = []
            anims.append(ApplyMethod(centroid_i.move_to, [centroid_i_next, 2, 0]))
            anims.append(ApplyMethod(dl1.put_start_and_end_on, np.array([centroid_i_next, 2, 0]), np.array([point, 0, 0])))
            self.play(AnimationGroup(*anims), run_time=run_time)

            anims = []
            anims.append(ApplyMethod(centroid_j.move_to, [centroid_j_next, 2, 0]))
            anims.append(ApplyMethod(dl2.put_start_and_end_on, np.array([centroid_j_next, 2, 0]), np.array([point, 0, 0])))
            self.play(AnimationGroup(*anims), run_time=run_time)


            self.play(Uncreate(dl1), run_time=run_time)
            self.play(Uncreate(dl2), run_time=run_time)