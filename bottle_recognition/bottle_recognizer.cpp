#include "bottle_recognizer.hpp"

typedef struct Bottle {
    uint8_t id;
    float x;
    float y;

} bottle_t;

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

    while (true) {
        video_capture >> image;
        processImage(image, image_gray);
    }
}

vector<bottle_t> processImage(cv::Mat, cv::Mat);