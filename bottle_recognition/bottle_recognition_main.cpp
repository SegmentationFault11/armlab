#include <iostream>
#include <string>
#include <vector>

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

        string locations = "Invalid Request";
        if (msg == "Get Locations") {
            locations = recognizer.get_locations();
        }

        send_msg(client_soc, locations);
    }


    _(cout << "main >> end, time: " << get_milli_sec() << endl;)
    return 0;
}