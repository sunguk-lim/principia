# Symmetric Eigendecomposition

## Meaning

A symmetric matrix can mix coordinates while still having perpendicular directions that it only scales. Symmetric eigendecomposition exposes those directions. It is a change of coordinates for the same [[linear-transformation]], not a replacement of a matrix by its diagonal entries in the original coordinates.

## Mechanism

Let A be a real n-by-n matrix with A transpose equal to A. An eigenvector q is a nonzero vector satisfying Aq=lambda*q, where scalar lambda is its eigenvalue. Choose normalized, mutually perpendicular eigenvectors as columns of Q. Their [[vector-dot-product]] values give Q transpose times Q=I, the identity. Then [[matrix-multiplication]] reconstructs A=Q*D*Q transpose, where D has the eigenvalues on its diagonal and zeros elsewhere. Q transpose converts an input into eigenvector coordinates; D scales them; Q converts back.

For positive eigenvalues, a matrix power A^p is Q*diag(lambda_i^p)*Q transpose. An inverse root is therefore not the elementwise root of A's entries. Zero or negative eigenvalues require special care: inverse roots are not defined there without changing the problem, for example by adding positive damping.

## One example

Let A=[[3,1],[1,3]]. Directions q_1=[1,1]/sqrt(2) and q_2=[1,-1]/sqrt(2) are perpendicular. Direct multiplication gives Aq_1=4*q_1 and Aq_2=2*q_2. The inverse square root scales these directions by 1/2 and 1/sqrt(2), respectively. For x=[2,0], its two eigenvector coordinates are both sqrt(2); rescaling and converting back yields approximately [1.2071,-0.2071]. The off-diagonal effect survives: inverse-root scaling is not independent scaling of the original two coordinates.

## Check your understanding

Can repeated eigenvalues make the reported eigenvectors unique? No: rotations within the repeated-eigenvalue subspace are valid. Check reconstruction and orthogonality residuals, not exact signs or column bytes. Test symmetry, positive eigenvalue bounds, finite precision and decomposition failures before using inverse powers.
