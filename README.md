# Improved-NSGA-II-for-cutter-layout-optimization
Optimization of cutter layout for shield cutterhead based on improved NSGA-II algorithm
  1. Changeable variables: Number of cutters(NUM_VARIABLES), Population size(popu), Iteration number(gene).
  2. Population initialization improvement: Spiral arrangement of the cutter on the spokes (optional: concentric arrangement or random arrangement);
  3. Objectives: 
    (1) Minimum radial load; 
    (2) Minimum overturning moment; 
    (3) Minimum standard deviation of rock breakage; 
    (4) Maximum cutter dispersion.
  4. Constrains: 
    (1) Center of mass position deviation less than the allowable error;
    (2) Cutter spacing meets requirements;
    (3) Individual Cutter load capacity meets requirements;
    (4) Cutter do not interfere with each other (cutting paths do not overlap).
