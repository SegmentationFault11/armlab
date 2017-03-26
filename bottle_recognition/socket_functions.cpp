#include "socket_functions.hpp"

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