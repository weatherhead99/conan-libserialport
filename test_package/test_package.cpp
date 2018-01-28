#include <cstdlib>
#include <iostream>
#include <libserialport.h>

int main()
{
    const char* version = sp_get_package_version_string();
    std::cout << "libserialport version: " << version << std::endl;
    return EXIT_SUCCESS;
}
