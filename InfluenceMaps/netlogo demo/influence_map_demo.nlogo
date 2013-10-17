extensions [matrix]
patches-own [influence]
turtles-own[agent-path path-index]

globals[HEIGHT WIDTH buffer _filter currentTicks]

to setup
  clear-all
  reset-ticks
  ask patches [set influence 0 
    set pcolor black]
  set WIDTH (max-pxcor - min-pxcor + 1)
  set HEIGHT (max-pycor - min-pycor + 1)
  set buffer matrix:make-constant HEIGHT WIDTH 0
  set _filter matrix:from-row-list  [[1 2 1][2 4 2][1 2 1]]
  set currentTicks 0
  ;create-turtles 1 [
  ;  setxy min-pxcor min-pycor 
  ;  set heading 45]
end

to go
  
  if ticks mod Turtle-Creation-Frequency = 0
  [
    ;; add a new turtle
    create-turtles 1 [
    setxy min-pxcor min-pycor 
    ;;setxy max-pxcor - 2 max-pycor 
    set heading 45]
  ]
  
  if ticks mod Update-Frequency = 0
  [
    ask patches [ apply-convolution ]
    ask patches [ update-from-buffer]
    ;; astar search
    ask turtles 
    [
      set agent-path astar patch-here (patch max-pxcor max-pycor)
      set path-index 0
    ]
  ]
  ask turtles [ navigate-path ]
  tick
end

to navigate-path
  ;;print "navigating"
  if agent-path != nobody
  [
    if patch-here = (item path-index agent-path)
    [
      set path-index path-index + 1
      if (length agent-path) = path-index
      [
        die
      ]
    ]
    face (item path-index agent-path)
    fd 1
  ]
end

to-report astar[patch1 patch2]
  let path []
  let closed matrix:make-constant HEIGHT WIDTH 0
  let costs matrix:make-constant HEIGHT WIDTH -1
  let H matrix:make-constant HEIGHT WIDTH 0
  let from matrix:make-constant HEIGHT WIDTH -1
  ;;print patch1
  ;;print patch2
  let open (lput patch1 [])
  ;;print open
  ;; set the cost of the initial node
  matrix:set costs (([pycor] of patch1) * (-1) + max-pycor) (([pxcor] of patch1) + max-pxcor) 0
  ;; set H
  matrix:set H (([pycor] of patch1) * (-1) + max-pycor) (([pxcor] of patch1) + max-pxcor) estimate patch1 patch2
  ;; set the parent as itself
  matrix:set from (([pycor] of patch1) * (-1) + max-pycor) (([pxcor] of patch1) + max-pxcor) astar-patch-hash patch1
  
  let node Nobody
  let path-found False
  while [not (empty? open or path-found)]
  [
    set node (item 0 open)
    ;;print (word "Current Node: " node)
    ;;print "Open list"
    ;;print open
    set open (remove-item 0 open)
    let nodei ([pycor] of node) * (-1) + max-pycor
    let nodej ([pxcor] of node) + max-pxcor
    ;; set as closed
    matrix:set closed nodei nodej 1
    ;;check if this node is the destination
    ifelse node = patch2
    [
      set path-found True
    ]
    [
      ;;expand node
      let n ([neighbors] of node)
      let sort? False
      ;;for each neighbour
      ask n
      [
        let i pycor * (-1) + max-pycor
        let j pxcor + max-pxcor

        
        let isClosed (matrix:get closed i j) = 1
        let isOpen (matrix:get costs i j) > 0 ;; use the cost value to check if the node is in the open list
        let parentG (matrix:get costs nodei nodej)
        let parentID astar-patch-hash node
        ;; get the cost
        let g (parentG + cost node self)
        
        ifelse not (isClosed or isOpen)
        [
          ;; unexplored node
          ;; set the cost
          matrix:set costs i j g
          ;; estimate the distance to goal
          matrix:set H i j (estimate self patch2)
          ;; set the parent
          matrix:set from i j parentID
          ;; add to the open list
          set open lput self open
          set sort? True
        ]
        [
          ifelse isOpen and g < (matrix:get costs i j)
          [
            ;; set the new cost
            matrix:set costs i j g
            ;; set the new parent
            matrix:set from i j parentID
            set sort? True
          ]
          [
            if isClosed and g < (matrix:get costs i j) ;; although we are using an admissible heuristic, let's put this check anyway
            [
              ;; remove from closed list
              matrix:set closed i j 0
              ;; set the new costs
              matrix:set costs i j g
              ;; set the new parent
              matrix:set from i j parentID
              ;; add to the open list
              set open lput self open
              set sort? True
            ]
          ]
        ]
      ]
      
      if sort?
      [
        set open sort-by [comparer ?1 ?2 costs H] open
      ]
    ]
  ]
  ;;construct the path
  set node patch2
  let nodei ([pycor] of node) * (-1) + max-pycor
  let nodej ([pxcor] of node) + max-pxcor
  let parentID matrix:get from nodei nodej
  let id astar-patch-hash node
  set path fput node path
  while [id != parentID]
  [
    set node get-patch parentID
    set nodei ([pycor] of node) * (-1) + max-pycor
    set nodej ([pxcor] of node) + max-pxcor
    set id parentID
    set parentID matrix:get from nodei nodej
    set path fput node path
  ]
  ;;print "path"
  ;;print path
  report path
end

to-report comparer[ p1 p2 costs H ]
  let i1 ([pycor] of p1) * (-1) + max-pycor
  let j1 ([pxcor] of p1) + max-pxcor
  
  let i2 ([pycor] of p2) * (-1) + max-pycor
  let j2 ([pxcor] of p2) + max-pxcor
  
  let f1 (matrix:get costs i1 j1) + (matrix:get H i1 j1)
  let f2 (matrix:get costs i2 j2) + (matrix:get H i2 j2)
  
  report f1 <= f2
end

to-report estimate[p1 p2] ;; returns the euclidean distance between the two patches
  let x ([pxcor] of p2) - ([pxcor] of p1)
  let y ([pycor] of p2) - ([pycor] of p1)
  report sqrt (x * x + y * y)
end

to-report cost[p1 p2] ;; return the cost of moving from p1 to p2
  let x ([pxcor] of p2) - ([pxcor] of p1)
  let y ([pycor] of p2) - ([pycor] of p1)  
  report sqrt (x * x + y * y) + ([influence] of p1) * 20 ;; add the influence of the current patch (20 is the red max value)
end

to-report astar-patch-hash[p] ;; trasform patch's pxcor and pycor into an ID
  let i ([pycor] of p) * (-1) + max-pycor
  let j ([pxcor] of p) + max-pxcor
  report i * WIDTH + j
end

to-report get-patch[id] ;; get the patch from the id
  let i floor (id / WIDTH)
  let j id mod WIDTH
  ;;print (word id "Matrix position [" i "," j "]")
  set i (i * -1) + max-pycor
  set j j - max-pxcor
  ;;print (word "Patch position [" j "," i "]")
  ;;print patch j i
  report patch j i
end

to apply-convolution
  let i pycor * (-1) + max-pycor
  let j pxcor + max-pxcor
  let newInfluence 0
  
  ;print (word i " " j)
  
  let up-left i = 0 and j = 0
  let up i = 0 and j > 0 and j < WIDTH - 1
  let _left j = 0 and i > 0 and i < HEIGHT - 1
  let up-right i = 0 and j = WIDTH - 1 
  let _right j = WIDTH - 1 and i > 0 and i < HEIGHT - 1
  let down-right i = HEIGHT - 1 and j = WIDTH - 1
  let down i = HEIGHT - 1 and j > 0 and j < WIDTH - 1
  let down-left i = HEIGHT - 1 and j = 0
  
  ifelse i > 0 and j > 0 and i < HEIGHT - 1 and  j < WIDTH - 1
  [
    ;;print "not in the border"
    let _neighbors  matrix:make-constant 3 3 0
    matrix:set _neighbors 0 0 [influence] of patch-at -1 1
    matrix:set _neighbors 0 1 [influence] of patch-at 0 1
    matrix:set _neighbors 0 2 [influence] of patch-at 1 1
    matrix:set _neighbors 1 0 [influence] of patch-at -1 0
    matrix:set _neighbors 1 1 influence
    matrix:set _neighbors 1 2 [influence] of patch-at 1 0
    matrix:set _neighbors 2 0 [influence] of patch-at -1 -1
    matrix:set _neighbors 2 1 [influence] of patch-at 0 -1
    matrix:set _neighbors 2 2 [influence] of patch-at 1 -1
    
    ;print matrix:pretty-print-text _neighbors
    
    set _neighbors matrix:times-scalar (matrix:times-element-wise _filter _neighbors) 0.0625
    
    ;print matrix:pretty-print-text _neighbors
    
    let _elements matrix:to-row-list _neighbors
    foreach _elements
    [
      set newInfluence newInfluence + sum ?
    ]
  ]
  [
    ;; 8 cases
    ;; up-left corner
    if up-left
    [
      set newInfluence up-left-convolution
    ]
    if _left
    [
      set newInfluence left-convolution
    ]
    if up
    [
      set newInfluence up-convolution
    ]
    if up-right
    [
      set newInfluence up-right-convolution
    ]
    if _right
    [
      set newInfluence right-convolution
    ]
    if down-right
    [
      set newInfluence down-right-convolution
    ]
    if down
    [
      set newInfluence down-convolution
    ]
    if down-left
    [
      set newInfluence down-left-convolution
    ]
  ]
  set newInfluence ( Momentum * influence + (1 - Momentum) * newInfluence )
  if newInfluence < min-Influence
  [
    set newInfluence 0
  ]
  ;;print newInfluence
  matrix:set buffer i j newInfluence
  ;;print matrix:pretty-print-text buffer
end

to-report up-left-convolution ;; apply the concolution for the special case up-left corner
  let newInfluence 0
  ;print "up left"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 1 1 3 3
  let _neighbors matrix:make-constant 2 2 0
  
  matrix:set _neighbors 0 0 influence
  matrix:set _neighbors 0 1 [influence] of patch-at 1 0
  matrix:set _neighbors 1 0 [influence] of patch-at 0 -1
  matrix:set _neighbors 1 1 [influence] of patch-at 1 -1
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.111
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  report newInfluence
end

to-report up-right-convolution
  ;print "up right"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 1 0 3 2
  let _neighbors matrix:make-constant 2 2 0
  let newInfluence 0
  matrix:set _neighbors 0 0 [influence] of patch-at -1 0
  matrix:set _neighbors 0 1 influence
  matrix:set _neighbors 1 0 [influence] of patch-at -1 -1
  matrix:set _neighbors 1 1 [influence] of patch-at  0 -1
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.111
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  report newInfluence
end

to-report down-left-convolution
  let newInfluence 0
  ;print "down left"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 0 1 2 3
  let _neighbors matrix:make-constant 2 2 0
  
  matrix:set _neighbors 0 0 [influence] of patch-at 0 1
  matrix:set _neighbors 0 1 [influence] of patch-at 1 1
  matrix:set _neighbors 1 0 influence
  matrix:set _neighbors 1 1 [influence] of patch-at 1 0
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.111
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  report newInfluence
end

to-report down-right-convolution
  ;print "down right"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 0 0 2 2
  let _neighbors matrix:make-constant 2 2 0
  let newInfluence 0
  matrix:set _neighbors 0 0 [influence] of patch-at -1 1
  matrix:set _neighbors 0 1 [influence] of patch-at  0 1
  matrix:set _neighbors 1 0 [influence] of patch-at -1 0
  matrix:set _neighbors 1 1 influence
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.111
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  report newInfluence
end

to-report up-convolution
  ;print "up"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 1 0 3 3
  let _neighbors matrix:make-constant 2 3 0
  let newInfluence 0
  
  matrix:set _neighbors 0 0 [influence] of patch-at -1 0
  matrix:set _neighbors 0 1 influence
  matrix:set _neighbors 0 2 [influence] of patch-at  1 0
  matrix:set _neighbors 1 0 [influence] of patch-at -1 -1
  matrix:set _neighbors 1 1 [influence] of patch-at  0 -1
  matrix:set _neighbors 1 2 [influence] of patch-at  1 -1
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.0833
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  
  report newInfluence
end

to-report left-convolution
  ;print "left"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 0 1 3 3
  let _neighbors matrix:make-constant 3 2 0
  let newInfluence 0
  
  matrix:set _neighbors 0 0 [influence] of patch-at 0 1
  matrix:set _neighbors 0 1 [influence] of patch-at 1 1
  matrix:set _neighbors 1 0 influence
  matrix:set _neighbors 1 1 [influence] of patch-at  1 0
  matrix:set _neighbors 2 0 [influence] of patch-at  0 -1
  matrix:set _neighbors 2 1 [influence] of patch-at  1 -1
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.0833
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  
  report newInfluence
end


to-report right-convolution
  ;print "right"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 0 0 3 2
  let _neighbors matrix:make-constant 3 2 0
  let newInfluence 0
  
  matrix:set _neighbors 0 0 [influence] of patch-at -1 1
  matrix:set _neighbors 0 1 [influence] of patch-at  0 1
  matrix:set _neighbors 1 0 [influence] of patch-at -1 0
  matrix:set _neighbors 1 1 influence
  matrix:set _neighbors 2 0 [influence] of patch-at  -1 -1
  matrix:set _neighbors 2 1 [influence] of patch-at   0 -1
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.0833
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  
  report newInfluence
end

to-report down-convolution
  ;print "down"
  ;;get the submatrix
  let subFilter matrix:submatrix _filter 0 0 2 3
  let _neighbors matrix:make-constant 2 3 0
  let newInfluence 0
  
  matrix:set _neighbors 0 0 [influence] of patch-at -1 1
  matrix:set _neighbors 0 1 [influence] of patch-at  0 1
  matrix:set _neighbors 0 2 [influence] of patch-at  1 1
  matrix:set _neighbors 1 0 [influence] of patch-at -1 0
  matrix:set _neighbors 1 1 influence
  matrix:set _neighbors 1 2 [influence] of patch-at  1 0
  
  ;print matrix:pretty-print-text _neighbors
  ;print matrix:pretty-print-text subFilter
  set _neighbors matrix:times-scalar (matrix:times-element-wise subFilter _neighbors) 0.0833
  
  ;print matrix:pretty-print-text _neighbors
  
  let _elements matrix:to-row-list _neighbors
  foreach _elements
  [
    set newInfluence newInfluence + sum ?
  ]
  
  report newInfluence
end

to update-from-buffer
  let i pycor * (-1) + max-pycor
  let j pxcor + max-pxcor
  ;;print (word i " " j " influence " influence)
  set influence matrix:get buffer i j
  ;;print (word i " " j " influence " influence)
  set pcolor scale-color red influence 0 1
end

to patch-draw
  if mouse-down?     ;; reports true or false to indicate whether mouse button is down
    [
      ;; mouse-xcor and mouse-ycor report the position of the mouse --
      ;; note that they report the precise position of the mouse,
      ;; so you might get a decimal number like 12.3, but "patch"
      ;; automatically rounds to the nearest patch
      ask patch mouse-xcor mouse-ycor
        [ set influence 1 
          set pcolor scale-color red influence 0 1]
      display
    ]
end
@#$#@#$#@
GRAPHICS-WINDOW
211
10
650
470
16
16
13.0
1
10
1
1
1
0
0
0
1
-16
16
-16
16
1
1
1
ticks
30.0

BUTTON
67
72
130
105
Run
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
69
138
139
171
Setup
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
65
206
185
239
Add influence
patch-draw
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
736
77
941
110
Update-Frequency
Update-Frequency
1
600
30
1
1
ticks
HORIZONTAL

SLIDER
736
149
908
182
Min-Influence
Min-Influence
0
1
0.1
0.05
1
NIL
HORIZONTAL

SLIDER
734
216
906
249
Momentum
Momentum
0
1
0
0.05
1
NIL
HORIZONTAL

BUTTON
68
29
131
62
Step
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
742
297
969
330
Turtle-Creation-Frequency
Turtle-Creation-Frequency
0
300
30
1
1
NIL
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

A basic demo of how we can use 'influence map' to modify an agent path. The agent starts in the bottom left corner and have to arrive at the top right corner

## HOW IT WORKS

It applies a gaussian convolution filter to propagate and dissipate the influence.

## HOW TO USE IT

Start pressing 'Add influence' button and click on different patches to add it (the patch will turn red). The press the run button and see how the path of the agent will become straighter again once the incluence decrease enough.

Use the Min-Influence slider to set a threshold which set the influence to 0 if the value is less than it.

Use the Momentum slider as a blending parameter between the new influence and the previous one.

Use the Update-Frequency slider to set the number of ticks between influence update and repathing.

Use the Turtle-Creation-Frequency to set the frequency which the turtles are created

## THINGS TO NOTICE

Notice how the influence values change the agent's straight line path

## NETLOGO FEATURES

Matrix extension
A* algorithm implementation


## CREDITS AND REFERENCES

Mouse Example for the influence drawing
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 5.0.3
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 1.0 0.0
0.0 1 1.0 0.0
0.2 0 1.0 0.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

@#$#@#$#@
0
@#$#@#$#@
