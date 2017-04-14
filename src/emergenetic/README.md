# EmerGen(e)tic 1.0         

## License

EmerGen(e)tic is copyright © 2017 Ben Goldsworthy (rumperuu).
                                                                          
EmerGen(e)tic is free software: you can redistribute it and/or modify        
it under the terms of the GNU General Public License as published by       
the Free Software Foundation, either version 3 of the License, or          
(at your option) any later version.                                        
                                                                           
EmerGen(e)tic is distributed in the hope that it will be useful,             
but WITHOUT ANY WARRANTY; without even the implied warranty of             
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              
GNU General Public License for more details.                               
                                                                           
You should have received a copy of the GNU General Public License          
along with EmerGen(e)tic.  If not, see <http://www.gnu.org/licenses/>.                             

## Contact

Email: me@bengoldsworthy.uk

## Description

EmerGen(e)tic is a Dana framework for testing the use of genetic
algorithms as applied to the components of an emergent system.

## Usage

After compiling the `emergenetic.dn` file, the program can be run. It
expects four command-line arguments, and can take a fifth optional one. 

The command is as follows:
   `dana emergenetic <module> <script> <generations> <candidates> [verbose]`

* <module> is the name of the module folder that you wish to use for your 
tests.
* <script> is the name of the script file for this particular test, located 
within the `/scripts/` directory and without the trailing `.script` file 
extension.
* The <generations> and <candidates> arguments are the number of 
generations to run the test for, and the number of candidates to produce 
per generation.
* The optional 'verbose' argument, if present, produces far more verbose 
output text. This can be useful for debugging.
