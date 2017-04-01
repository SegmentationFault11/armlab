# Targets
	TARGETS = bottle_recognition_main.cpp bottle_recognizer.cpp socket_functions.cpp helper.cpp

# Object files
	OBJECTS = apriltags/libapriltags.a

# Designated compiler
	CXX = g++ -std=c++11

# Executable
	EXECUTABLE = bottle_recognizer

# Mac Include Paths
	MAC_INCLUDE_PATHS = -I/usr/local/include -I/usr/local/include/eigen3

# Linux Include Paths
	LINUX_INCLUDE_PATHS = -I/usr/include -I/usr/include/eigen3

# Library Paths
	LIBRARY_PATHS = -L/usr/local/lib

# Mac Linkers
	MAC_LINKERS = -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_video -lopencv_calib3d

# Linux Linkers
	LINUX_LINKERS = $(MAC_LINKERS) -lopencv_videoio	

# Optimization Level
	OX = -O3

# Compilation Flags
	COMPILATION_FLAGS = -Wall -Wextra -pthread -ldl

mac:
	$(CXX) -o $(EXECUTABLE) $(COMPILATION_FLAGS) $(OX) $(TARGETS) $(OBJECTS) $(MAC_INCLUDE_PATHS) $(LIBRARY_PATHS) $(MAC_LINKERS)

linux:
	$(CXX) -o $(EXECUTABLE) $(COMPILATION_FLAGS) $(OX) $(TARGETS) $(OBJECTS) $(LINUX_INCLUDE_PATHS) $(LIBRARY_PATHS) $(LINUX_LINKERS)

debug:
	$(CXX) -o $(EXECUTABLE) -DDEBUG $(COMPILATION_FLAGS) $(OX) $(TARGETS) $(OBJECTS) $(INCLUDE_PATHS) $(LIBRARY_PATHS) $(MAC_LINKERS)
