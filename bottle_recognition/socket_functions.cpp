#include "socket_functions.hpp"

#ifdef __APPLE__
    #define MSG_NOSIGNAL 0
#endif

using namespace std;

int setup_socket(int port) {
    int new_socket;

    // Create a socket
    if ((new_socket = ::socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        throw runtime_error("Error requesting socket");
    }

    // Enable reusability
    int one = 1;
    if (::setsockopt(new_socket, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(int)) < 0) {
        throw runtime_error("Error setsocket");
    }

    // Set up socket configuration struct
    struct sockaddr_in socket_addr;
    bzero((char *) &socket_addr, sizeof(socket_addr));
    socket_addr.sin_family = AF_INET;
    socket_addr.sin_port = htons(port);
    socket_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    // Bind the socket to its configuration struct
    if (::bind(new_socket, (struct sockaddr*) &socket_addr, (socklen_t) sizeof(socket_addr)) < 0) {
        throw runtime_error("Error binding socket");
    }

    // If the kernal choses the port, retrieve the allocated port number
    socklen_t len = sizeof(socket_addr);
    if (port) {
        if (getsockname(new_socket, (struct sockaddr *) &socket_addr, &len) < 0) {
            throw runtime_error("Error with getsockname");
        }
    }
    port = ntohs(socket_addr.sin_port);

    // Make socket listen to incoming communication
    if (::listen(new_socket, 10) == -1) {
        throw runtime_error("Error listening with socket");
    }

    return new_socket;
}

// Wrapper that accetps the incoming communication
int accept_socket(int serv_soc) {
    return accept(serv_soc, (struct sockaddr*) NULL, NULL);
}

string read_msg(int socket) {
    string msg = "";
    size_t msg_length = 0;

    char buf[1];
    while (true) {
        int bytes_received = recv(socket, &buf, 1, 0);

        if (bytes_received != 1 && bytes_received != 0) {
            throw runtime_error("Error reading from socket");
        }

        if (*buf == '\0') {
            break;
        }

        msg += *buf;
        ++msg_length;

        if (msg_length > 512) {
            cout << "Received message too long" << endl;

            return "";
        }
    }

    return msg;
}

void send_msg(int socket, string msg) {
    size_t msg_length = msg.size();

    size_t bytes_sent = 0;

    while (bytes_sent < msg_length) {
        bytes_sent += send(socket, msg.c_str() + bytes_sent, msg_length - bytes_sent, MSG_NOSIGNAL);
    }
}
