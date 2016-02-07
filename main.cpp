#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string>

#include "gumbo.h"

int main(int argc, char** argv)
{

   std::cout << "Welcome to the paper search command line utility\n"; 

   if(argc != 2) {
      std::cout << "Usage: paperSearch <html filename>\n";
      exit(EXIT_FAILURE);
   }  

   const char* filename = argv[1];

   std::ifstream in(filename, std::ios::in | std::ios::binary);
   if (!in) {
     std::cout << "File " << filename << " not found!\n";
     exit(EXIT_FAILURE);
   }

   std::string contents;
   in.seekg(0, std::ios::end);
   contents.resize(in.tellg());
   in.seekg(0, std::ios::beg);
   in.read(&contents[0], contents.size());
   in.close();

   GumboOutput* output = gumbo_parse(contents.c_str());
   /* Code for extracting paper info */
   // std::cout << cleantext(output->root) << std::endl;
   
   /* --------- */
   gumbo_destroy_output(&kGumboDefaultOptions, output);
   
   std::cout << "End Program\n";

   return 0;
}
