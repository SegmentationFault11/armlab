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

#include "apriltags/TagDetector.h"
#include "apriltags/Tag16h5.h"
#include "apriltags/Tag25h7.h"
#include "apriltags/Tag25h9.h"
#include "apriltags/Tag36h9.h"
#include "apriltags/Tag36h11.h"

using namespace std;

typedef class BottleRecognizer {
private:

    AprilTags::TagDetector* tag_detector;

public:

    BottleRecognizer();
    ~BottleRecognizer();

    string get_locations();
    
} bottle_recognizer_t;