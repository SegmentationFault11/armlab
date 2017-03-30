#pragma once

#include <cmath>
#include <chrono>
#include <fstream>
#include <string>
#include <vector>
#include <stdexcept>
#include <exception>

#include "apriltags/TagDetector.h"
#include "apriltags/Tag16h5.h"

unsigned get_milli_sec();

double standardRad(double);

void wRo_to_euler(const Eigen::Matrix3d&, double&, double&, double&);

vector<string> split_str(char, string);

vector<pair<string, string>> read_params_file(string);

void write_param_file(string, vector<pair<string, string>>&);