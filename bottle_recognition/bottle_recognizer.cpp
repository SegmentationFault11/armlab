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

    vector<bottle_t> bottle_list;

    while (true) {
        video_capture >> image;

        bool error = processImage(image, image_gray, bottle_list);

        if (!error) {
            break;
        }
    }

    return "sf";
}

bool BottleRecognizer::processImage(cv::Mat& image, cv::Mat& image_gray, vector<bottle_t>& bottle_list) {
    cv::cvtColor(image, image_gray, CV_BGR2GRAY);

    vector<AprilTags::TagDetection> detections = tag_detector->extractTags(image_gray);

    for (size_t i = 0; i < detections.size(); i++) {
        detections[i].draw(image);
    }
    imshow(display_window_name, image);

    (void) bottle_list;

    return false;
}