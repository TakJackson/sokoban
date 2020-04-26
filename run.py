import mySokobanSolver
import sokoban
print("running test...")
wh = sokoban.Warehouse()
wh.load_warehouse("./warehouses/warehouse_05.txt")
print(mySokobanSolver.taboo_cells(wh))

