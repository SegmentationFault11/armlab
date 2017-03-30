#include "helper.hpp"

#ifdef DEBUG
#define _(x) x
#else
#define _(x)
#endif

const double PI = 3.14159265358979323846;
const double TWOPI = 2.0*PI;

unsigned get_milli_sec() {
    return std::chrono::duration_cast<std::chrono::milliseconds>
        (std::chrono::system_clock::now().time_since_epoch()).count();
}

double standardRad(double t) {
    _(cout << "standardRad >> start, time: " << get_milli_sec() << endl;)

    if (t >= 0.) {
        t = fmod(t+PI, TWOPI) - PI;
    } else {
        t = fmod(t-PI, -TWOPI) + PI;
    }

    _(cout << "standardRad >> end, time: " << get_milli_sec() << endl;)
    return t;
}

void wRo_to_euler(const Eigen::Matrix3d& wRo, double& yaw, double& pitch, double& roll) {
    _(cout << "wRo_to_euler >> start, time: " << get_milli_sec() << endl;)

    yaw = standardRad(atan2(wRo(1,0), wRo(0,0)));
    double c = cos(yaw);
    double s = sin(yaw);
    pitch = standardRad(atan2(-wRo(2,0), wRo(0,0)*c + wRo(1,0)*s));
    roll  = standardRad(atan2(wRo(0,2)*s - wRo(1,2)*c, -wRo(0,1)*s + wRo(1,1)*c));

    _(cout << "wRo_to_euler >> end, time: " << get_milli_sec() << endl;)
}

// Split a string into a vector of strings using a delimitor
vector<string> split_str(char delim, string s) {
    stringstream ss;
    ss.str(s);
    vector<string> elems;
    string item;
    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

vector<pair<string, string>> read_params_file(string param_file_name) {
	ifstream param_file(param_file_name);

	if (!param_file) {
		throw runtime_error("Unable to read param file: " + param_file_name);
	}

	vector<pair<string, string>> params_properties;

	string line;
	vector<string> param_pair;
	while (getline(param_file, line)) {
		if (line.empty()) {
			continue;
		}

		param_pair = split_str(' ', line);
		if (param_pair.size() != 2) {
			throw runtime_error("Paramfile in incorrect format, " + to_string(param_pair.size()) + " elements detected in a line");
		}

		params_properties.push_back(make_pair(param_pair[0], param_pair[1]));
	}

	return params_properties;
}

void write_param_file(string param_file_name, vector<pair<string, string>>& params_properties) {
	ofstream param_file;
	param_file.open(param_file_name, std::ofstream::out | std::ofstream::trunc);
	if (!param_file) {
		throw runtime_error("Unable to open param file: " + param_file_name);
	}

	size_t num_properties = params_properties.size();
	for (size_t i = 0; i < num_properties; ++i) {
		param_file << params_properties[i].first + " " + params_properties[i].second;
	}

	param_file.close();
}