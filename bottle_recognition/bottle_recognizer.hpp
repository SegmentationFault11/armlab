#pragma once

#ifdef __LINUX__
#define EXPOSURE_CONTROL 
#endif

#include <iostream>
#include <cstring>
#include <vector>
#include <unordered_map>
#include <list>
#include <string>
#include <algorithm>
#include <cmath>
#include <limits>
#include <unistd.h>
#include <sys/time.h>

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

typedef struct BottleSlot {
    uint8_t slot_id;
    float x;
    float y;
    float z;
    bool occupied;

} bottle_slot_t;

typedef class BottleRecognizer {
private:

    AprilTags::TagDetector* tag_detector;

    cv::VideoCapture video_capture;

    string display_window_name;

    unordered_map<int, bottle_slot_t*> bottle_slots;

public:

    BottleRecognizer();
    ~BottleRecognizer();

    void setup();

    string get_locations();

    string assign_locations(vector<AprilTags::TagDetection>&);

    void print_detection(AprilTags::TagDetection&) const;

    void reset_slot_occupancy();
    
} bottle_recognizer_t;