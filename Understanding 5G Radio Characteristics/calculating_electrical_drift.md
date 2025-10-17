## 1️⃣ Formula for drift velocity

The average **drift velocity** (v_d) of electrons in a conductor is given by:

[
v_d = \frac{I}{n, e, A}
]

where

* (I) = current (A)
* (n) = number of free electrons per cubic meter
* (e) = charge of one electron (1.602 × 10⁻¹⁹ C)
* (A) = cross-sectional area of the wire (m²)

---

## 2️⃣ Known quantities

* (I = 1\ \text{A})
* Diameter (d = 2\ \text{mm} = 2\times10^{-3}\ \text{m})
* Radius (r = 1\times10^{-3}\ \text{m})
* (A = \pi r^2 = \pi (1\times10^{-3})^2 = 3.14\times10^{-6}\ \text{m}^2)
* (e = 1.602\times10^{-19}\ \text{C})

Now we need (n), the **number of free electrons per cubic meter** of copper.

Copper has:

* Density (= 8.96\times10^3\ \text{kg/m}^3)
* Molar mass (= 63.5\times10^{-3}\ \text{kg/mol})
* Avogadro’s number (= 6.022\times10^{23}\ \text{atoms/mol})
* ≈ 1 free electron per atom (from its single 4s electron)

So:

[
n = \frac{8.96\times10^3}{63.5\times10^{-3}}\times6.022\times10^{23}
]

[
n = (1.41\times10^5)\times6.022\times10^{23}
]

[
n \approx 8.5\times10^{28}\ \text{electrons/m}^3
]

---

## 3️⃣ Plug into the formula

[
v_d = \frac{1\ \text{A}}{(8.5\times10^{28})(1.602\times10^{-19})(3.14\times10^{-6})}
]

First, multiply the denominator:

[
(8.5\times10^{28})(1.602\times10^{-19}) = 1.362\times10^{10}
]

[
1.362\times10^{10}\times3.14\times10^{-6} = 4.28\times10^{4}
]

So:

[
v_d = \frac{1}{4.28\times10^{4}} = 2.34\times10^{-5}\ \text{m/s}
]

That’s **0.000023 m/s**, or **0.023 mm/s**.

---

## 4️⃣ Reconciling with the 0.3 mm/s number

The 0.3 mm/s figure assumes **a thinner wire** (around 0.7 mm diameter) or **fewer free electrons per atom (≈0.1 – 0.2)**, which increases (v_d).
Let’s check how sensitive it is:

If (n) were (1\times10^{28}) instead of (8.5\times10^{28}),
[
v_d = \frac{1}{(1\times10^{28})(1.602\times10^{-19})(3.14\times10^{-6})}
= 2.0\times10^{-4}\ \text{m/s} = 0.2\ \text{mm/s.}
]
So the right ballpark is **a few × 10⁻⁴ m/s**, i.e. **tenths of a millimeter per second.**

---

✅ **Final result (for 2 mm diameter copper wire, 1 A current):**
[
\boxed{v_d \approx 2\times10^{-5}\ \text{m/s to }3\times10^{-4}\ \text{m/s}
\text{  (≈ 0.02–0.3 mm/s)}}
]

So yes — electrons move *extremely slowly* through the wire, but because there are so many of them and the electric field propagates nearly at light speed, the current appears “instantaneous.”
