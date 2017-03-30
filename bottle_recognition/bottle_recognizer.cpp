#include "bottle_recognizer.hpp"

#ifdef DEBUG
#define _(x) x
#else
#define _(x)
#endif

BottleRecognizer::BottleRecognizer() {
    _(cout << "BottleRecognizer >> start, time: " << get_milli_sec() << endl;)

    tag_detector = new AprilTags::TagDetector(AprilTags::tagCodes16h5);

    display_window_name = "bottle_recognizer";

    for (int slot = 0; slot < 9; ++slot) {
        bottle_slots[slot] = new bottle_slot_t;

        if (slot == 0) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 1) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 2) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 3) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 4) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 5) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 6) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 7) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
        else if (slot == 8) {
            bottle_slots[slot]->x = 0.0;
            bottle_slots[slot]->y = 0.0;
            bottle_slots[slot]->z = 0.0;
            bottle_slots[slot]->occupied = false;
        }
    }

    _(cout << "BottleRecognizer >> end, time: " << get_milli_sec() << endl;)
}

BottleRecognizer::~BottleRecognizer() {
    _(cout << "~BottleRecognizer >> called, time: " << get_milli_sec() << endl;)
    delete tag_detector;
}

void BottleRecognizer::setup() {
    _(cout << "setup >> start, time: " << get_milli_sec() << endl;)

    cv::namedWindow(display_window_name, 1);

    // find and open a USB camera (built in laptop camera, web cam etc)
    video_capture = cv::VideoCapture(1);
    if(!video_capture.isOpened()) {
        cerr << "ERROR: Can't find video device " << 1 << "\n";
        exit(1);
    }

    video_capture.set(CV_CAP_PROP_FRAME_WIDTH, 640);
    video_capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);

    for (auto iter = bottle_slots.begin(); iter != bottle_slots.end(); ++iter) {
        iter->second->occupied = false;
    }

    _(cout << "setup >> end, time: " << get_milli_sec() << endl;)
}

string BottleRecognizer::get_locations() {
    _(cout << "get_locations >> start, time: " << get_milli_sec() << endl;)

    reset_slot_occupancy();

    cv::Mat image;
    cv::Mat image_gray;

    vector<AprilTags::TagDetection> bottle_list;

    unsigned num_repeats = 0;
    while (true) {
        video_capture >> image;
        cv::cvtColor(image, image_gray, CV_BGR2GRAY);

        bottle_list = tag_detector->extractTags(image_gray);

        if (std::any_of(bottle_list.begin(), bottle_list.end(), 
            [](AprilTags::TagDetection i) { return i.hammingDistance > 2; })) {
            if (num_repeats > 3) {
                return "FATAL: Hamming Distance greater than 2.";
            }

            ++num_repeats;
        }
        else {
            break;
        }
    }

    if (bottle_list.empty()) {
        return "FATAL: No Bottles Detected";
    }

    for (size_t i = 0; i < bottle_list.size(); ++i) {
        print_detection(bottle_list[i]);
    }

    _(cout << "get_locations >> end, time: " << get_milli_sec() << endl;)
    return assign_locations(bottle_list);
}

string BottleRecognizer::calibrate_locations(string known_location_str) {
    vector<pair<int, int>> known_locations = decode_calibration_str(known_location_str);

    

    return "Calibration Failed";
}

void BottleRecognizer::decode_calibration_str(string known_location_str) {
    vector<pair<int, bottle_slot_t>> known_locations;

    vector<string> location_pairs = split_str(' ', known_location_str);
    size_t num_locations_given = location_pairs.size();
    known_locations.resize();

    for (size_t i = 0; i < num_locations_given; ++i) {
        vector<string> pair_elems = split_str('|', location_pairs[i]);

        known_locations[i] = make_pair(pair_elems[0], pair_elems[1]);
    }

    return location_pairs;
}

string BottleRecognizer::assign_locations(vector<AprilTags::TagDetection>& bottle_list) {
    _(cout << "assign_locations >> start, time: " << get_milli_sec() << endl;)
    
    string reply_str = "";

    while (bottle_list.size()) {
        AprilTags::TagDetection curr_bottle = bottle_list.back();
        bottle_list.pop_back();

        float smallest_dist = numeric_limits<float>::max();
        int slot_id = -1;
        for (auto iter = bottle_slots.begin(); iter != bottle_slots.end(); ++iter) {
            if (iter->second->occupied) {
                continue;
            }

            float curr_dist = calc_tag2slot_dist(curr_bottle, *(iter->second));
            if (curr_dist < smallest_dist) {
                smallest_dist = curr_dist;
                slot_id = iter->first;
            }
        }

        if (slot_id == -1) {
            return "FATAL: Can't match bottle with slots";
        }

        bottle_slots[slot_id]->occupied = true;

        reply_str += "{" + to_string(slot_id) + "|" + to_string(curr_bottle.id) + "}";
    }

    _(cout << "assign_locations >> end, time: " << get_milli_sec() << endl;)
    return reply_str;
}

void BottleRecognizer::print_detection(AprilTags::TagDetection& detection) const {
    cout << "  Id: " << detection.id
             << " (Hamming: " << detection.hammingDistance << ")";

    Eigen::Vector3d translation;
    Eigen::Matrix3d rotation;
    detection.getRelativeTranslationRotation(0.05, 600, 600, 640/2, 480/2, 
        translation, rotation);

    Eigen::Matrix3d F;
    F <<
        1, 0,  0,
        0,  -1,  0,
        0,  0,  1;

    Eigen::Matrix3d fixed_rot = F*rotation;
    double yaw, pitch, roll;
    wRo_to_euler(fixed_rot, yaw, pitch, roll);

    cout << "  distance=" << translation.norm()
             << "m, x=" << translation(0)
             << ", y=" << translation(1)
             << ", z=" << translation(2)
             << ", yaw=" << yaw
             << ", pitch=" << pitch
             << ", roll=" << roll
             << endl;
}

void BottleRecognizer::reset_slot_occupancy() {
    _(cout << "reset_slot_occupancy >> start, time: " << get_milli_sec() << endl;)

    for (auto iter = bottle_slots.begin(); iter != bottle_slots.end(); ++iter) {
        iter->second->occupied = false;
    }

    _(cout << "reset_slot_occupancy >> end, time: " << get_milli_sec() << endl;)
}

float BottleRecognizer::calc_tag2slot_dist(AprilTags::TagDetection tag_location, bottle_slot_t bottle_slot) {
    _(cout << "calc_tag2slot_dist >> start, time: " << get_milli_sec() << endl;)

    Eigen::Vector3d translation;
    Eigen::Matrix3d rotation;
    tag_location.getRelativeTranslationRotation(0.166, 600, 600, 640/2, 480/2, 
        translation, rotation);

    Eigen::Matrix3d F;
    F <<
        1, 0,  0,
        0,  -1,  0,
        0,  0,  1;

    Eigen::Matrix3d fixed_rot = F*rotation;
    double yaw, pitch, roll;
    wRo_to_euler(fixed_rot, yaw, pitch, roll);

    float distance = sqrt(pow(translation(0) - bottle_slot.x, 2) 
        + pow(translation(1) - bottle_slot.y, 2) 
        + pow(translation(2) - bottle_slot.z, 2));

    _(cout << "calc_tag2slot_dist >> end, time: " << get_milli_sec() << endl;)
    return distance;
}

