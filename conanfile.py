import os
import shutil
from conans import ConanFile, CMake, tools

def get_version():
    git = tools.Git()
    try:
        return git.run("describe --tags --dirty --always").replace('/', '-')
    except:
        return None

class PythonRequires(ConanFile):
    name = "conanbase"
    version = get_version()

def get_conanfile():
    class BaseConanFile(ConanFile):
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"
        generators = "cmake_find_package"

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            cmake.test()

        def package(self):
            self.copy("*.h", dst="include")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

    return BaseConanFile
