#include "bottle_recognizer.hpp"

BottleRecognizer::BottleRecognizer() {
    tag_detector = new AprilTags::TagDetector(AprilTags::tagCodes16h5);
}

BottleRecognizer::~BottleRecognizer() {
    delete tag_detector;
}

string BottleRecognizer::get_locations() {
    return "why";
}