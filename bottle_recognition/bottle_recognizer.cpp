#include "bottle_recognizer.hpp"

#ifdef DEBUG
#define _(x) x
#else
#define _(x)
#endif

#ifdef __LINUX__
#define EXPOSURE_CONTROL 
#endif

BottleRecognizer::BottleRecognizer() {
    _(cout << "BottleRecognizer >> start, time: " << get_milli_sec() << endl;)

    tag_detector = new AprilTags::TagDetector(AprilTags::tagCodes36h11);

    display_window_name = "bottle_recognizer";

    slot_locations_file = "slot_locations.properties";

    vector<pair<string, string>> slot_locations_properties;
    try {
        slot_locations_properties = read_params_file(slot_locations_file);
    } 
    catch (const runtime_error& re) {
        cerr << re.what();
        exit(1);
    }

    for (int slot = 0; slot < 9; ++slot) {
        bottle_slots[slot] = new bottle_slot_t;
        bottle_slots[slot]->occupied = false;
    }

    size_t num_params = slot_locations_properties.size();
    for (size_t i = 0; i < num_params; ++i) {
        int offset = i%3;
        if (offset == 0) {
            bottle_slots[i/3]->x = stof(slot_locations_properties[i].second);
        }
        else if (offset == 1) {
            bottle_slots[i/3]->y = stof(slot_locations_properties[i].second);
        }
        else if (offset == 2) {
            bottle_slots[i/3]->z = stof(slot_locations_properties[i].second);
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

#ifdef EXPOSURE_CONTROL
    // manually setting camera exposure settings; OpenCV/v4l1 doesn't
    // support exposure control; so here we manually use v4l2 before
    // opening the device via OpenCV; confirmed to work with Logitech
    // C270; try exposure=20, gain=100, brightness=150

    string video_str = "/dev/video0";
    video_str[10] = '0' + 1;
    int device = v4l2_open(video_str.c_str(), O_RDWR | O_NONBLOCK);

    v4l2_close(device);
#endif 

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

vector<AprilTags::TagDetection> BottleRecognizer::detect_tags() {
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
                throw runtime_error("FATAL: Hamming Distance greater than 2.");
            }

            ++num_repeats;
        }
        else {
            break;
        }
    }

    if (bottle_list.empty()) {
        throw runtime_error("FATAL: No Bottles Detected");
    }

    return bottle_list;
}

string BottleRecognizer::get_locations() {
    _(cout << "get_locations >> start, time: " << get_milli_sec() << endl;)

    reset_slot_occupancy();

    vector<AprilTags::TagDetection> bottle_list;
    try {
        bottle_list = detect_tags();
    }
    catch (const runtime_error& re) {
        return re.what();
    }

    for (size_t i = 0; i < bottle_list.size(); ++i) {
        print_detection(bottle_list[i]);
    }

    _(cout << "get_locations >> end, time: " << get_milli_sec() << endl;)
    return assign_locations(bottle_list);
}

string BottleRecognizer::calibrate_locations(string known_location_str) {
    unordered_map<int, int> bottle_2_slot = decode_calibration_str(known_location_str);

    vector<AprilTags::TagDetection> bottle_list;
    try {
        bottle_list = detect_tags();
    }
    catch (const runtime_error& re) {
        return string("Calibration Failed: ") + string(re.what());
    }

    size_t num_bottles = bottle_list.size();
    if (bottle_2_slot.size() != num_bottles) {
        return "Calibration Failed: detected more bottles than given";
    }

    vector<pair<string, string>> slot_locations_properties = read_params_file(slot_locations_file);

    vector<string> param_name(3);
    param_name[0] = "_x";
    param_name[1] = "_y";
    param_name[2] = "_z";
    for (size_t i = 0; i < num_bottles; ++i) {
        int slot_num = -1;

        tag_pose_t tag_pose = get_tag_pose(bottle_list[i]);

        slot_num = bottle_2_slot.at(bottle_list[i].id);

        for (int offset = 0; offset < 3; ++offset) {
            slot_locations_properties[slot_num*3 + offset].second = to_string(tag_pose.translation(offset));
            slot_locations_properties[slot_num*3 + offset].first = to_string(slot_num) + param_name[offset];
        }
    }

    write_param_file(slot_locations_file, slot_locations_properties);

    return "Calibration Success: " + to_string(num_bottles) + " positions updated";
}

unordered_map<int, int> BottleRecognizer::decode_calibration_str(string known_location_str) {
    unordered_map<int, int> bottle_2_slot;

    vector<string> location_pairs = split_str(' ', known_location_str);
    size_t num_locations_given = location_pairs.size();

    for (size_t i = 0; i < num_locations_given; ++i) {
        vector<string> pair_elems = split_str('|', location_pairs[i]);

        bottle_2_slot[stoi(pair_elems[1])] = stoi(pair_elems[0]);
    }

    return bottle_2_slot;
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

    tag_pose_t tag_pose = get_tag_pose(detection);

    cout << "  distance=" << tag_pose.translation.norm()
             << "m, x=" << tag_pose.translation(0)
             << ", y=" << tag_pose.translation(1)
             << ", z=" << tag_pose.translation(2)
             << ", yaw=" << tag_pose.yaw
             << ", pitch=" << tag_pose.pitch
             << ", roll=" << tag_pose.roll
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

    tag_pose_t tag_pose = get_tag_pose(tag_location);

    float distance = sqrt(pow(tag_pose.translation(0) - bottle_slot.x, 2) 
        + pow(tag_pose.translation(1) - bottle_slot.y, 2) 
        + pow(tag_pose.translation(2) - bottle_slot.z, 2));

    _(cout << "calc_tag2slot_dist >> end, time: " << get_milli_sec() << endl;)
    return distance;
}

tag_pose_t BottleRecognizer::get_tag_pose(AprilTags::TagDetection detection) const {
    Eigen::Vector3d translation;
    Eigen::Matrix3d rotation;
    detection.getRelativeTranslationRotation(0.166, 600, 600, 640/2, 480/2, 
        translation, rotation);

    Eigen::Matrix3d F;
    F <<
        1, 0,  0,
        0,  -1,  0,
        0,  0,  1;

    Eigen::Matrix3d fixed_rot = F*rotation;
    double yaw, pitch, roll;
    wRo_to_euler(fixed_rot, yaw, pitch, roll);

    tag_pose_t tag_pose;
    tag_pose.translation = translation;
    tag_pose.yaw = yaw;
    tag_pose.pitch = pitch;
    tag_pose.roll = roll;

    return tag_pose;
}
