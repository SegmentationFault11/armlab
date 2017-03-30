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