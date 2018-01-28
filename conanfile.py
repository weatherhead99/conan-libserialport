import os
from conans import ConanFile, tools, AutoToolsBuildEnvironment

class LibserialportConan(ConanFile):
    name = "libserialport"
    version = "0.1.1"
    license = "LGPL-3.0"
    url = "https://github.com/weatherhead99/conan-libserialport"
    description = "a minimal, cross-platform library that is intended to take care of the OS-specific details when writing software that uses serial ports."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = ["LICENSE.md"]

    def source(self):
        url = "http://sigrok.org/download/source/{0}/{0}-{1}.tar.gz"
        tools.get(url.format(self.name, self.version))

    def build(self):
        win_bash = self.settings.os == "Windows"
        abe = AutoToolsBuildEnvironment(self, win_bash=win_bash)
        abe.configure(args=["--enable-silent-rules",
                            "--prefix=%s" % self.package_folder],
                      configure_dir=os.path.join(self.source_folder,
                                                 "libserialport-%s"
                                                 % self.version)
                      )

        abe.make()

    def package(self):
        self.copy("libserialport.h", dst="include", src=self.build_folder)
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.so.*", dst="lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)

        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("COPYING", dst="licenses", src=self.source_folder,
                  keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["serialport"]
