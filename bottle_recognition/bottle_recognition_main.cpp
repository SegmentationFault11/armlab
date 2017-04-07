#include <iostream>
#include <string>
#include <vector>

//#include "opencv2/opencv.hpp"

#include "socket_functions.hpp"
#include "bottle_recognizer.hpp"
#include "helper.hpp"

#ifdef DEBUG
#define _(x) x
#else
#define _(x)
#endif

using namespace std;

int main() {
    _(cout << "main >> start, time: " << get_milli_sec() << endl;)

    //cvRedirectError(handleError);
    //cv::redirectError(handleError);

    BottleRecognizer recognizer;
    recognizer.setup();

    int soc = setup_socket(12000);

    _(cout << "main >> waiting on socket, time: " << get_milli_sec() << endl;)
    int client_soc = -1;
    while ((client_soc = accept_socket(soc))) {
        _(cout << "main >> incoming socket, time: " << get_milli_sec() << endl;)

        if (client_soc == -1) {
            cerr << "Invalid socket" << endl;
            exit(1);
        }

        string msg = read_msg(client_soc);

        string response;
        if (msg == "Get Locations") {
            response = recognizer.get_locations();
        }
        else if (msg.substr(0, 20) == "Calibrate Locations ") {
            response = recognizer.calibrate_locations(msg.substr(20, msg.size() - 20));
        }
        else {
            response = "Invalid Request";
        }

        send_msg(client_soc, response);
    }

    _(cout << "main >> end, time: " << get_milli_sec() << endl;)
    return 0;
}
