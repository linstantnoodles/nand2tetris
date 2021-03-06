## Thinking about sequential 

The hardest part of these chips was thinking about inputs with respect to time. 

It really helps to make sure you understand the notation before writing your implementation, so lets do that.

Lets use the `Bit` chip as an example: 

```
 * 1-bit register:
 * If load[t] == 1 then out[t+1] = in[t]
 *                 else out does not change (out[t+1] = out[t])
```

First, what is `t`? `t` is a clock time unit. Remember what a clock time unit is?

The clock is a device that delivers alternating signals to our sequential chips. Each tick-tock (0/1 signal) is a cycle. It's an idea that lets us think about the _real_ time between CPU cycles (which is continuous) as discrete.

We can think about `t` in a couple different ways: it can be the curret cycle or the previous cycle. How we define it doesn't *really* matter since the specification above for the bit register will hold regardless of whether we choose to think about `t` as current or past time.

The simplest way for me to think about it is to define `t` as the current cycle. 

So if I translate the spec to english: 

`If load[t] == 1` -> if the current load bit is 1

`then out[t+1] = in[t]` -> then the current input will be the next output

`else out does not change (out[t+1] = out[t])` -> else, the current output will be the next output

Armed with this slightly clearer definition, we can now think about how we want to deal with our current input values. 

1. We can use a multiplexor to decide whether to output the current output (from our flip flop) or the current input. Since we've been dealing with combinatorial chips all along, it may be using the chips output as input. However, that's perfectly natural with sequential chips because they're always emitting their output as determined by the input from the _previous_ cycle.
2. We can now feed this value into our flip flop, which will automagically take care of sending our new (or same) output value once the clock ticks.

## RAM 8

A single register stores 16 bits. The contents of those bits is a word. How do we take a register and build a small RAM? 

First, what's RAM?

requirements:

1. read/write operations should be able to access any word with equal speed
2. every register in RAM has an address
3. we must be able to select which register to read / write to

how do we meet these requirements for a RAM size of 8 (not to be confused with word size, which is a single register AKA 16 bits)?

1. we use a demultiplexor with our 3 bit selector to determine the load value for each register
2. we feed that result into every register
3. we output the value of the current address

couple of takeaways here: 

* you're sending a load bit to *all* the registers (this tells them whether to persist their values or load the new one). This seems counter-intuitive because even though we're sending the load bit to _all_ registers, only one of them will perform a load (if load is 1).
* you're always outputing the output of a *single* register

## RAM 64

Extending it to 64 means that we'll need to use some bits to decide _which_ of our set of RAM8's do we want to perform a load for. The individual RAM8's will then take care of doing the actual loading. Just like before, we are sending an input to _all_ of our 64 registers.
