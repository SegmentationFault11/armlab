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
#include <exception>
#include <stdexcept>
#include <unistd.h>
#include <sys/time.h>

#ifdef EXPOSURE_CONTROL
#include <libv4l2.h>
#include <linux/videodev2.h>
#include <fcntl.h>
#include <errno.h>
#endif

#include "helper.hpp"

#include "opencv2/opencv.hpp"

#include "apriltags/TagDetector.h"
#include "apriltags/Tag16h5.h"
#include "apriltags/Tag25h7.h"
#include "apriltags/Tag25h9.h"
#include "apriltags/Tag36h9.h"
#include "apriltags/Tag36h11.h"

using namespace std;

typedef struct BottleSlot {
    float x;
    float y;
    bool occupied;

} bottle_slot_t;

typedef struct TagPose {
    Eigen::Vector3d translation;
    float distance;
    float yaw;
    float pitch;
    float roll;
} tag_pose_t;

typedef class BottleRecognizer {
private:

    AprilTags::TagDetector* tag_detector;

    cv::VideoCapture video_capture;

    string display_window_name;

    unordered_map<int, bottle_slot_t*> bottle_slots;

    string slot_locations_file;

public:

    BottleRecognizer();
    ~BottleRecognizer();

    void setup();

    string get_locations();

    string calibrate_locations(string);

private:

    unordered_map<int, int> decode_calibration_str(string);

    vector<AprilTags::TagDetection> detect_tags();

    string assign_locations(vector<AprilTags::TagDetection>&);

    void print_detection(AprilTags::TagDetection&) const;

    void reset_slot_occupancy();

    float calc_tag2slot_dist(AprilTags::TagDetection, bottle_slot_t);

    tag_pose_t get_tag_pose(AprilTags::TagDetection) const;
    
} bottle_recognizer_t;