## HalfAdder

This chip takes two bits, adds them together, and then outputs the result and the carry bit. How do you add? Well, since we're just dealing with bits, we can use boolean functions!

Lets look at the boolean table for "adding".

|a   |b   |result |
|---|---|---|
|0   |0   |0   |
|0   |1   |1   |
|1   |0   |1   |
|1   |1   |0   |

This table is equivalent to the table of our XOR function. We also know that there's only one case we have a carry bit: when both `a` and `b` are True. 

Just like that, we have a chip that _almost_ adds since it doesn't include the carry in its answer. _Half_ adds.

## FullAdder

Now lets account for the carry bit. This means we need this chip to add not one but three bits. Just like the half adder, it will also produce a carry.

## Inc16

Given a 16 bit bus representing a number, we can start by incrementing the first bit. This will produce a sum (which is first bit output) and a carry bit. Given that we only need the carry bit and the next bit to compute our next output bit, we can rely on a chain of half adders only.

## Add16

This chip marks the birth of our general purpose arithmetic compute hardware. 

1. We can start with a half adder to add the first bit of both buses
2. We resort to a full adder to add the carry from step 1 and the next _two_ bits. 

Why do we need to use full adders this time instead of half ones like we did with Inc16? Well, unlike `Inc16`, we need to use a chain of full adders here because we're no longer adding two bits - there's not the carry, the bit from number A, and another bit from number B.

## ALU

The trickiest bit of this chip for me is trying to implement this logic: 

```
// if (out == 0) set zr = 1
```

How do we determine if a 16 bit bus represents zero? Well, if all of it's values are zero! So wouldn't it be great if we had a chip that took a 16 bit bus as an input and returned 1 if all the bits are zero?

Yes but that chip doesn't exist. The closest thing we got is an Or8Way which takes a bus and returns a bit.

Lets work with what we have and see how we can make that chip work for us.

1. Or8Way will return 1 if any of the bits are 1 and 0 if none of the bits are 1. 
2. By negating the result of Or8Way, we will get 1 if none of the bits are 1 (we have an 8 bit zero).
3. We have 16 bits, so we'll need to divide this task into two buses.
4. We can't feed output pin back into input and we can't subbus an internal pin. Therefore, we need to think ahead during our earlier computes and feed them our answers into 8 bit internal pins.

# twos complement

We need way of encoding negative numbers using existing hardware (adders). So the challenge is the following: if we know how to add, can we teach our hardware how to subtract without adding custom subtractors? 

The answer is yes and it's because any subtraction can be reframed as addition of a negative number and vice versa. Once we solve operations on negatives, we pretty much also solved the problem of subtractoin.

Ok, so I mentioned this "reframing" idea but how do we represent negative numbers so that they can be used in addition? 

Here's the intuition: think modulo math or the ring structure

* If you put your finger at any point on a circle and move in either direction, you can get to the same destination by moving the _other_direction. 
* Given a movement counter clockwise in this number ring  (moving to the left), what's the equivalent (complementary) move to the right? well, that depends on the size of the ring and the number of steps you take. Turns out, you can find the "complementary" steps (the complement) by subtracting the steps from the size of the ring. 

The intuition here is that since it's a circle, the result of the subtraction will take you to the SAME spot on the circle. 

Given a single digit decimal number (hence ring size of 10):

move -1 (same as moving +9) 
move -2 (same as moving +8)
move -3 (same as moving +7) 

Moving one step one way in a circle is like running as far as possible (minus one step) the other way

We now have a way to both represent and perform operations of negative numbers.

So how big is this ring? Where does the space of negatives begin and end? 

1. The ring size depends on the digits and number of symbols we have. So in the decimal system, we have a ring size of 10
2. The number of times you can move one way equals of times you can move other way. Turns out, you meet somewhere in the middle. So if you start moving from 0 to both directions, you will get all the signed representations in our digit space

## More on negative numbers aka additive inverses

The *additive inverse* of any number is when combined gets you 0. In a number line, the additive inverse of 9 is -9 (so you go 9 in different direction until you reach 0). we use the "-" sign to denote that we mean the additive inverse of a number. In mathematics, you can just add a - sign and the concept will be understood.

In computers, how do we represent the additive inverse of a number? Well, we know how to represent positive numbers: 00, 01, 10, 11, etc using a binary system. How do we represent the additive inverse of a positive number (aka a negative number?) Turns out, you can do it with radix complements (there's a natural symmetry in a ring structure between the right of 0 and the left of 0). This solves both the representation problem (since half the space is negatives) AND operations problem (since adding by its complement will give you the same result).



