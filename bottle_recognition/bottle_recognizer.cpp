#include "bottle_recognizer.hpp"

BottleRecognizer::BottleRecognizer() {
    tag_detector = new AprilTags::TagDetector(AprilTags::tagCodes16h5);

    display_window_name = "bottle_recognizer";
}

BottleRecognizer::~BottleRecognizer() {
    delete tag_detector;
}

void BottleRecognizer::setup() {
    cv::namedWindow(display_window_name, 1);

    // find and open a USB camera (built in laptop camera, web cam etc)
    video_capture = cv::VideoCapture(1);
    if(!video_capture.isOpened()) {
        cerr << "ERROR: Can't find video device " << 1 << "\n";
        exit(1);
    }

    video_capture.set(CV_CAP_PROP_FRAME_WIDTH, 640);
    video_capture.set(CV_CAP_PROP_FRAME_HEIGHT, 480);
}

string BottleRecognizer::get_locations() {
    cv::Mat image;
    cv::Mat image_gray;

    vector<AprilTags::TagDetection> bottle_list;

    unsigned num_repeats = 0;
    while (true) {
        video_capture >> image;
        cv::cvtColor(image, image_gray, CV_BGR2GRAY);

        bottle_list = tag_detector->extractTags(image_gray);

        if (any_of(bottle_list.begin(), bottle_list.end(), [](int i) {
            return i.hammingDistance > 1;
        })) {
            if (num_repeats > 3) {
                return "FATAL: Hamming Distance greater than 1.";
            }

            ++num_repeats;
        }
        else {
            break;
        }
    }

    return assign_locations(bottle_list);
}


