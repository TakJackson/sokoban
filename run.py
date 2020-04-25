import mySokobanSolver
import sokoban
wh = sokoban.Warehouse()
wh.load_warehouse("./warehouses/warehouse_01.txt")
mySokobanSolver.taboo_cells(wh)
