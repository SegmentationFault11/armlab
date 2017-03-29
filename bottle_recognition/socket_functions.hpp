#pragma once

#include <iostream>
#include <cstdlib>
#include <exception>
#include <stdexcept>
#include <algorithm>
#include <cstring>
#include <string>
#include <climits>
#include <vector>
#include <cstdint>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/types.h>

#include "helper.hpp"

using namespace std;

int setup_socket(int);

int accept_socket(int);

string read_msg(int socket);

void send_msg(int socket, string msg);