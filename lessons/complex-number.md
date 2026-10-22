# Complex Number

## Meaning

A complex number packages two real coordinates into one arithmetic object. Write z=a+ib, where a and b are real and i is the imaginary unit with i²=-1. The coefficient b is the imaginary part; it is a real number, not ib itself. This representation adds a multiplication rule, not merely a second coordinate label.

## Mechanism

Using [[arithmetic]], define addition componentwise and multiplication by distribution together with i²=-1:

$$(a+ib)+(c+id)=(a+c)+i(b+d),$$
$$(a+ib)(c+id)=(ac-bd)+i(ad+bc).$$

Here z=a+ib and w=c+id are complex numbers and a,b,c,d their real coordinates. Define the conjugate of z as z̄=a-ib. Then z z̄=a²+b² is real and nonnegative. For w=c+id, the real part of z w̄ is ac+bd, the ordinary real coordinate-pair dot product. Conjugation is important: the real part of zw without conjugation would be ac-bd instead.

## Worked example

Take z=2+3i and w=4-i. Their product is (8+3)+i(-2+12)=11+10i. The conjugate of w is 4+i, so z w̄=(8-3)+i(2+12)=5+14i. Its real part 5 also equals 2×4+3×(-1), confirming the dot-product identity. Multiplying z by i gives -3+2i: the pair (2,3) becomes (-3,2), a quarter-turn without changing squared length, since 2²+3²=(-3)²+2²=13.

The special rotation example does not mean every complex multiplier preserves length: multiplying by 2 doubles coordinates and quadruples squared length. Complex arithmetic can be implemented using real pairs without a native complex dtype. Test multiplication and conjugation conventions explicitly when changing representations; swapping conjugation changes signs even when array shapes agree. This node defines arithmetic only; analytic functions and their derivatives are separate topics.

## Check your understanding

**Question:** Is the imaginary part of 2+3i equal to 3i? **Answer:** No; its imaginary coefficient is the real number 3.
