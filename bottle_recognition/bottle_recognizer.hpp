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

typedef struct Bottle {
    uint8_t id;
    float x;
    float y;

} bottle_t;

typedef class BottleRecognizer {
private:

    AprilTags::TagDetector* tag_detector;

    cv::VideoCapture video_capture;

    string display_window_name;

public:

    BottleRecognizer();
    ~BottleRecognizer();

    void setup();

    string get_locations();

    string assign_locations(vector<bottle_t>&);
    
} bottle_recognizer_t;