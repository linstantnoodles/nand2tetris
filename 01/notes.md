# Project 01

## NOT

It's not immediately clear how to construct a NOT gate using NAND since one takes a single input and the other takes two inputs. However, the solution will more likely leap to mind once you recognize that there's no reason you can't send the same input to both input pins on the NAND gate. 

Why does that work?

I think there's a few concepts at play here that you need to understand to grasp the full picture: 

1. A NAND A is equivalent to NOT(A AND A)
2. `A * A` (`*` is the boolean algebra symbol for AND) is always A by the idempotent law. In other words, when you apply the AND operator to an element itself, it retains its value no matter how many times it's applied. A simpler explanation for this is: true and true will always be true. false and false will always be false.
3. Since `A AND A` gives back itself, we can reduce it to `A` which makes the full expression `NOT(A)`.

## AND

Assuming you already have the `NOT` chip built using `NAND`, the intuition behind using NAND for this chip is

1. Knowing that NAND is equivalent to a combination of NOT and AND. 
2. By the double negation law, `NOT(NOT(AND X Y))` is the same as `AND X Y`.

Therefore, all you need to do is feed the NAND chip output into NOT.

Why does the double negation law work? I think we can get an intuition for this with an example: 

Statement 1: I am a human 
Negation of statement 1: I am not a human 
Negation of the negation: I am not NOT a human 

Well, when you're not NOT something, you are something. The two negatives cancel out and you get a positive.

## OR 

I was really suprised to learn that OR _can_ be constructed from NAND's and found my solution even less intuitive that the NOT and AND chips.

There's a couple of directions you can take to grasp this.

The first is by creating a logic table for OR.

|a   |b   |result   |
|---|---|---|
|0   |0   |0   |
|0   |1   |1   |
|1   |0   |1   |
|1   |1   |1   |

If you try to construct a boolean function for this table by looking at the rows where the result is 1 (stands for True), you'll find yourself in a chicken and egg situation because you'll end up depending on the OR operator (which you don't have).

However, if you look at the rows where the result is false, we'll be able to determine two things: 

1. There's _only_ ONE row that is false / has an output of 0. 
2. If we can write a boolean function that returns 1 when the inputs of of the first row are _not_ met, then we end up with the same logic table! 

Put another way, if `a` is NOT 0 AND `b` is NOT 0, then we must be `1` because according to the original OR table BOTH `a` and `b` must be 0 for the result to be `0`. Did you notice that we only used NOT and AND? :D 

The other angle for approaching this basically starts from the conclusion of the previous approach. Are you ready? Here it is: A OR B is the same as saying that they're not BOTH false! I think this is my favorite intuition for this so far.

## XOR

My first solution to this involved AND, NOT, and OR.  It's far easier to understand compared to the final, more optimized solution but it uses a lot more NAND gates.

Starting from a truth table:

|a   |b   |result   |
|---|---|---|
|0   |0   |0   |
|0   |1   |1   |
|1   |0   |1   |
|1   |1   |0   |

If you look at the rows with a result of True, you'll see that we can produce this truth table with the following boolean function: 

`(NOT A and B) OR (A and NOT B)`

NOT uses 1 NAND. AND uses 2 NANDS. OR uses at least 1 NOT and 1 AND so that's at least 3 NANDS. In sum, if we tried realizing this gate using real chips it would require >= 9 NAND chips.

This made me wonder: could we do better? 

Turns out, the answer is yes according to [wikipedia](https://en.wikipedia.org/wiki/XOR_gate):

> An XOR gate circuit can be made from four NAND gates

Spoiler alert: here's the full derivation process

`(NOT (A AND B)) AND (NOT(NOT A AND NOT B))`

Notice that the first expression is a NAND (this is key). Now after reducing the second expression using de morgans law.

`(NOT (A AND B)) AND (A OR B)`

Now lets distribute the first expression over the second based on the distributive law (AND can be distributed over OR).

`(NOT (A AND B) AND A) OR (NOT (A AND B) AND B)`

Is there a way we can change the OR to and AND? Lets apply demoregans law again with NOT to flip the OR to AND.

`NOT(NOT (A AND B) AND A) AND NOT(NOT (A AND B) AND B)`

Great! This looks like we have 2 NAND's on each side of the middle AND. Unfortunately, our actual result got negated. How do we negate it back? Apply NOT to the whole thing (but without applying de-morgans law because we want to keep the AND that we got in the previous step after flipping OR).

`NOT(NOT(NOT (A AND B) AND A) AND NOT(NOT (A AND B) AND B))`

Can you see where the 4 NAND's are in this expression?

# Mux 

The truth table for the multiplexor is as follows:

|a   |b   |sel| result|
|---|---|---|---|
|0   |0   |0   |0 |
|0   |1   |0   |0 |
|1   |0   |0   |1 |
|1   |1   |0   |1 |
|0   |0   |1   |0 |
|0   |1   |1   |1 |
|1   |0   |1   |0 |
|1   |1   |1   |1 |

The rows where the result is `1` helps us write an OR expression to represent the table.

```
(A AND (NOT B) AND (NOT SEL))  
OR 
(A AND B AND (NOT SEL)) 
OR
((NOT A) AND B AND SEL) 
OR
(A AND B AND SEL) 
```

`A AND B` is repeated twice - one when SEL is 0 and one when sel is 1. We can just eliminate the SEL check in that case.

```
(A AND (NOT B) AND (NOT SEL))  
OR 
(A AND B) 
OR
((NOT A) AND B AND SEL) 
```

# DMux

|in  |sel | {a, b}|
|---|---|---|
|0   |0 |0,0 |
|0   |1 |0,1 |
|1   |0 |1,0 |
|1   |1 |0,1 |

The key observation here is that both the output of `a` and `b` in `{a, b}` are true under one condition. What this means is you can write a boolean function for the `a` pin and the `b` pin!

# Mux4Way16

This is the first time we're dealing with a multi-bit selector and the order of those bits _matter_. 

Take this line for instance:

`out = b if sel == 01`

Turns out the actual bit values are stored in _reverse_ in the virtual hardware. In other words `0` would be at `sel[1]` and `1` would be at `sel[0]`.

For every bit bus you see in the course text (HDL file comments, chapter text), you'll need to remember this difference when writing your chips.

the key to the implementation is to arrange a binary tree like pattern of chips where each level is separated by a mux chip.

# DMux4way 

Given a multi-bit selector, we want our input to one of four pins a, b, c, and d. 

```
{a, b, c, d} = {in, 0, 0, 0} if sel == 00
               {0, in, 0, 0} if sel == 01
               {0, 0, in, 0} if sel == 10
               {0, 0, 0, in} if sel == 11
```

We can solve this by treat each bit as a separate selector again. We'll use the first bit in a DMux, but ... what do we pass in for the input pins `a` and `b`? 

What if we gave it 'a' and 'b'? That will return either 'a' or 'b' depending on the value of our first selector bit and we'll output that to the corresponding output pins `a` and `b`. We'll then do the same for 'c' and 'd'! Will that work? Turns out, no because take the situation of sel == 11. We'll end up with the output {0, in, 0, in}. What we expect is {0, 0, 0, in}. 

This happened because the MSB (the left hand side in the notation aka most significant byte) is not a selector for {0, 0, x, 0} and {0, 0, 0, x}. It's in reality, based on the chart provided, a selector for {x, 0, 0, 0} and {0, 0, x, 0}. So we need to first find the value of x and then use the second bit to determine where it falls. 

```
// This outputs our temp result x basically
DMux(in=in, sel=sel[0], a=outOne, b=outTwo);
// This uses the first selector to place it either on the left hand side or right hand side
DMux(in=outOne, sel=sel[1], a=a, b=c);
// We'll do this for every left / right pair!
DMux(in=outTwo, sel=sel[1], a=b, b=d);
```

# Tips 

* When reading buses, remember that actual bit values are stored in _reverse_ compared to how they're represented in text. The least significant bit will come first. The bus 00000001 will be stored as 10000000. I'm not sure why but it probably has something to do with that fact that it's simply easier to interpret a 0 index as starting from the left. See [here](https://en.wikipedia.org/wiki/Bit_numbering#Most_significant_bit) for more details.































