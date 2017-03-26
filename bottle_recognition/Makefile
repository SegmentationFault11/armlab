# Targets
	TARGETS = bottle_recognition_main.cpp bottle_recognizer.cpp socket_functions.cpp

# Designated compiler
	CXX = g++ -std=c++11

# Executable
	EXECUTABLE = bottle_recognizer

# Include Paths
	INCLUDE_PATHS = -I/usr/local/include

# Library Paths
	LIBRARY_PATHS = -L/usr/local/lib

# Linkers
	LINKERS = -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_ml -lopencv_video -lopencv_features2d -lopencv_calib3d -lopencv_objdetect -lopencv_contrib -lopencv_legacy -lopencv_stitching

# Optimization Level
	OX = -O3

# Compilation Flags
	COMPILATION_FLAGS = -Wall -Werror -Wextra -pthread

all:
	$(CXX) $(INCLUDE_PATHS) $(LIBRARY_PATHS) $(LINKERS) $(OX) $(COMPILATION_FLAGS) $(TARGETS) -o $(EXECUTABLE)
	
debug:
	$(CXX) -DDEBUG $(INCLUDE_PATHS) $(LIBRARY_PATHS) $(LINKERS) $(OX) $(COMPILATION_FLAGS) $(TARGETS) -o $(EXECUTABLE)
