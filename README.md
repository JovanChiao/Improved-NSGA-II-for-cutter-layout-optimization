# Improved-NSGA-II-for-cutter-layout-optimization
Optimization of cutter layout for shield cutterhead based on improved NSGA-II algorithm
  1. Changeable variables: Number of cutters(NUM_VARIABLES), Population size(popu), Iteration number(gene).
  2. Population initialization improvement: Spiral arrangement of the cutter on the spokes (optional: concentric arrangement or random arrangement);
  3. Objectives:<br>
     (1) Minimum radial load;<br>
     (2) Minimum overturning moment;<br>
     (3) Minimum standard deviation of rock breakage;<br>
     (4) Maximum cutter dispersion.<br>
  4. Constrains: <br>
    (1) Center of mass position deviation less than the allowable error;<br>
    (2) Cutter spacing meets requirements;<br>
    (3) Individual Cutter load capacity meets requirements;<br>
    (4) Cutter do not interfere with each other (cutting paths do not overlap).
