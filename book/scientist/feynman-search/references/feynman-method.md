# Feynman Method — 4 steps for clear explanation

The technique is a learning loop. You finish only when you can explain to someone with no background.

## The 4 steps

1. **Pick a concept.** Write its name at the top of a blank page.
2. **Teach it as if to a 12-year-old.** Use plain words. No jargon. If you reach for a technical term, replace it with a description.
3. **Identify gaps.** Where you stumble or simplify too far, mark it. Those gaps are what you don't truly know.
4. **Refine and use analogy.** Go back to the source. Find a familiar comparison. Loop until the explanation flows.

> "If you can't explain it simply, you don't understand it well enough." — *attributed to Einstein, popularised by Feynman*
>
> "The real problem in speech is not precise language. The problem is clear language. The desire is to have the idea clearly communicated to the other person." — *Feynman*
>
> "Everything in life was an adventure. Learning — just the pleasure of finding things out." — *Feynman*

## Worked translation 1 — Quantum entanglement

**Bad (jargon):** "Two particles in a Bell state exhibit non-local correlations such that measurement of one instantaneously determines the state of the other."

**Feynman style:** "Imagine you have a pair of magic gloves. You ship one glove to Mars in a sealed box. The moment you open your box on Earth and see a left glove, you *know* the box on Mars holds a right glove — even though no signal travelled between them. That's the puzzle: nothing is sent, but the two answers always agree. Real entangled particles do this with measurements that aren't fixed in advance."

What got moved: jargon → analogy. Gap acknowledged: *"aren't fixed in advance"* hints at Bell inequalities without naming them.

## Worked translation 2 — Path integral formulation (Feynman's own work)

**Bad:** "The amplitude of a transition is the integral of e^(iS/ℏ) over all paths."

**Feynman style:** "Light, given a starting point and an ending point, doesn't pick *one* path. It tries them all at once, and the final answer is what's left after the paths cancel each other out — most cancel, the boring straight line survives. This is what 'classical' physics is: the surviving sum of every weird possibility nature explored."

## Worked translation 3 — Backpropagation (modern ML)

**Bad:** "Compute gradients of the loss with respect to each weight via reverse-mode automatic differentiation through the computational graph."

**Feynman style:** "You guessed wrong. To fix it, you walk backwards through every step that produced the guess and ask 'how much did *this* step contribute to the wrongness?' Each step takes a tiny corrective nudge proportional to its blame. Do this on millions of guesses and the network slowly learns. Backprop is just shared blame, distributed efficiently."

## Translation checklist

- [ ] No word a 12-year-old wouldn't know without context
- [ ] One concrete analogy from daily life
- [ ] Names the *one* aha moment (not five at once)
- [ ] Marks at least one gap or simplification honestly

## What Feynman would refuse

- **False clarity.** "We don't really know" beats a confident lie.
- **Names without referents.** Memorising "what something is called" is not knowing it.
- **Single-pass explanation.** The 4 steps loop. Real understanding emerges on iteration 2 or 3.
- **Math as decoration.** If you can't say why a symbol is there, drop it.
