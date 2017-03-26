#pragma once

#ifdef __LINUX__
#define EXPOSURE_CONTROL 
#endif

#include <iostream>
#include <cstring>
#include <vector>
#include <list>
#include <sys/time.h>
#include <string>
#include <cmath>
#include <unistd.h>

#ifdef EXPOSURE_CONTROL
#include <libv4l2.h>
#include <linux/videodev2.h>
#include <fcntl.h>
#include <errno.h>
#endif

#include "opencv2/opencv.hpp"

#include "AprilTags/TagDetector.h"
#include "AprilTags/Tag16h5.h"
#include "AprilTags/Tag25h7.h"
#include "AprilTags/Tag25h9.h"
#include "AprilTags/Tag36h9.h"
#include "AprilTags/Tag36h11.h"

using namespace std;

typedef class BottleRecognizer {
public:

    string get_locations();
    
} bottle_recognizer_t;