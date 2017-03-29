#include <iostream>
#include <string>
#include <vector>

#include "socket_functions.hpp"
#include "bottle_recognizer.hpp"

using namespace std;

int main() {
    BottleRecognizer recognizer;
    recognizer.setup();

    int soc = setup_socket(12000);

    int client_soc = -1;
    while ((client_soc = accept_socket(soc))) {

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

    return 0;
}