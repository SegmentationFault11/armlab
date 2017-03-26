#include <iostream>
#include <string>

#include "socket_functions.hpp"

using namespace std;

int main() {

    int soc = setup_socket(12000);

    int client_soc = -1;
    while ((client_soc = accept_socket(soc))) {

        if (client_soc == -1) {
            cerr << "Invalid socket" << endl;
            exit(1);
        }

        string msg = read_msg(client_soc);

        cout << "Reply: " << endl;

        string reply;
        cin >> reply;

        send_msg(client_soc, reply);
    }

    return 0;
}