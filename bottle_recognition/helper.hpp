#pragma once

#include <cmath>
#include <chrono>

#include "apriltags/TagDetector.h"
#include "apriltags/Tag16h5.h"

unsigned get_milli_sec();

double standardRad(double);

void wRo_to_euler(const Eigen::Matrix3d&, double&, double&, double&);

vector<string> split_str(char, string);