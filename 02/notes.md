# twos complement

we need way of encoding negative numbers using existing hardware (adders). If we know how to add, can we teach our hardware how to subtract without adding subtractors? 

key ideas: 

* any subtraction can be reframed as addition of a negative number and vice versa
* solve operations on negatives and you also solve subtraction

key question: how do we represent negative numbers so that they can be used in addition? 

the key idea here is: modulo math or the ring structure

* if you put your finger at any point on a circle and move in either direction, you can get to the same destination by moving the _other_direction. this is the first key high level concept 
* given a movement counter clockwise in this number ring  (moving to the left), what's the equivalent (complementary) move to the right? well, that depends on the size of the ring and the number of steps you take. Turns out, you can find the "complementary" steps (the complement) by subtracting the steps from the size of the ring. 

The intuition here is that since it's a circle, the result of the subtraction will take you to the SAME spot on the circle. 

Given a single digit decimal number:

move -1 (9) 
move -2 (8)
move -3 (7) 

question is ... why is this true? why is the complement such?

there's a few ways to get a feel for this: 

* moving one step one way in a circle is like running as far as possible (minus one step) the other way

we now have a way to both represent and perform operations of negative numbers. the question is .. how big is this ring? and where does the space of negatives begin and end? 

* ring depends on the digits and number of symbols we have
* the # of times you can move one way = # of times you can move other way (there's exactly half)
* if you start moving from 0 to both directions, you will get all the signed representations in our digit space


* the additive inverse of any number is when combined gets you 0 
* in a number line, the additive inverse of 9 is -9 (so you go 9 in different direction until you reach 0). we use the "-" sign to denote that we mean the additive inverse of a number

* in mathematics, you can just add a - sign and the concept will be understood
* in computers, how do we represent the additive inverse of a number? well, we know how to represent positive numbers: 00, 01, 10, 11, etc using a binary system.
* how do we represent the additive inverse of a positive number (aka a negative number?)
* turns out, you can do it with radix complements (there's a natural symmetry in a ring structure between the right of 0 and the left of 0). This solves both the representation problem (since half the space is negatives) AND operations problem (since adding by its complement will give you the same result)



