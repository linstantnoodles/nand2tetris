# nand2tetris-solutions

My solutions to each project in the wonderful [nand2tetris](https://www.nand2tetris.org/) course. Each project directory also includes `notes.md` document containing tips, explanations, and ramblings.

nand2tetris is available as two separate courses on coursera:

1. Part 1: Build a Modern Computer from First Principles: From Nand to Tetris
2. Part 2: Build a Modern Computer from First Principles: Nand to Tetris Part II 

* Folders `01` through `06` in this repo correspond to the actual nand2tetris project numbers in the first part of the course. The final project is an assembler for the HACK assembly language.
* The `vm-translator` folder contains my work for nand2tetris project 7 & 8 where you build the virtual machine language translator.
* The `09` folder contains a program I wrote for project 9 using JACK (a high level, OO, java-like language).
* The `jack-compiler` folder contains my work for projects 10 * 11 where you build a compiler for the JACK.
* Finally, the `os-services` folder contains my work for project 12 (final project) where you build a suite of operating system services using JACK that can ultimately boot and run your machine!

## Is the code tested? 

Yes! Every module has been verified to work (on my machine :D). I've also written some of my own tests for the the programming assignments (such as the vm translator and parts of the compiler).

## Your code does not follow their API guidelines ...

I went a bit rouge on some of the programming portions, so my design may not line up with what they suggest...

## Feedback

I would love to know if anything can be made better. Please let me know by submitting a PR!

## TODO (Cleanup tasks / Optimizations)

In order of importance ...

* optimize the drawRectangle function in `Screen.jack`. Rendering objects takes forever right now. I think the bottleneck lives in drawLine, which is still doing pixel by pixel drawing for both vertical and horizontal lines.
* test `Memory.jack` more thoroughly by internally inspecting the linked list. Would also be fun to write a defrag
* refactor / cleanup multiplication and division algorithms in `Math.jack`. I rushed through this and I'm not sure if it's optimal right now
* write up implementation notes / tips for the os services
