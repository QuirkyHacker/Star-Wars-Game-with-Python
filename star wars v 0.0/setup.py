import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Lisek\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Lisek\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("star_wars.py")]

cx_Freeze.setup(
	name = "Star Wars v0.0",
	options = {"build_exe": {"packages": ["pygame"], 
	           "include_files":["X_Wing.png", "Tie_Fighter.png", "bg_space.bmp"]}},

	executables = executables

)
