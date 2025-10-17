# Understanding 5G Radio Characteristics

- [Understanding 5G Radio Characteristics](#understanding-5g-radio-characteristics)
  - [Some Basics](#some-basics)
    - [Power... and a rabbit hole](#power-and-a-rabbit-hole)
    - [Some Electric Units](#some-electric-units)
      - [Current](#current)
      - [Volts (electric potential energy)](#volts-electric-potential-energy)
    - [Decibels](#decibels)
      - [Decibels (dB)](#decibels-db)
      - [Decibel-Miliwatt (dBm)](#decibel-miliwatt-dbm)
    - [Examples](#examples)
  - [5G Measurements](#5g-measurements)
    - [Signal-to-Interference-plus-Noise Ratio (SINR)](#signal-to-interference-plus-noise-ratio-sinr)
    - [Reference Signal Receive Power (RSRP)](#reference-signal-receive-power-rsrp)
    - [Received Signal Strength Indicator (RSSI)](#received-signal-strength-indicator-rssi)
    - [Reference Signal Received Quality (RSRQ)](#reference-signal-received-quality-rsrq)
    - [Wrap Up](#wrap-up)

## Some Basics

In order to understand how we measure 5G performance, we first have to understand a bit about physics. At the simplest level, electromagnetic waves propogate out through space until they hit our antenna. When they hit the antenna they induce a tiny voltage usually in the range of microvolts (millionths of a volt). That voltage represents the energy your antenna received from the air. Stronger signal → more voltage → more electrical power.

To understand power, we really have to understand a bit about some other physics concepts.

### Power... and a rabbit hole

Ok, so that's the high level, the next thing we need to understand is power. Power is a measurement of the amount of energy per second. To understand this you first have to **really** understand what a watt is. 1 watt = 1 joule per second, but this obviously begs the question, what is a joule? A joule is $1\text{ Newton}\times1\text{ meter}$. The problem is... what is a newton? A newton is defined from Newton's second law of motion:

$$
F=m\times a
$$

where $m$ is mass in kilograms and $a$ is acceration in meters per second. So $1N=1kg \times m/s^2$ Now, if you're like me, you think to yourself, "What the heck is a $s^2$???". What we're saying is how fast something is accelerating. So let's say your speed is $5m/s$. That you probably understand, you're moving 5 meters every second. However, we want to measure acceleration so we want to know how much our distance per second is changing... per second. So if our acceleration is $5m/s^2$ we're saying that we're going $5m/s$ faster every second. IE:

| Time | Speed  | Change in speed | Acceleration |
| ---- | ------ | --------------- | ------------ |
| 0 s  | 0 m/s  | —               | —            |
| 1 s  | 5 m/s  | +5 m/s          | 5 m/s²       |
| 2 s  | 10 m/s | +5 m/s          | 5 m/s²       |
| 3 s  | 15 m/s | +5 m/s          | 5 m/s²       |

So you can think of it this way:

- The first second tells you “how far per second” → speed.
- The second second tells you “how much that speed changes per second” → acceleration.

Ok, back up one level, but what does this have to do with newtons?

A newton is the amount of effort (force) it takes to accelerate 1kg of mass, at $1m/s^2$. This is the actual meaning behind $F=m\times a$ If you've heard the story of an apple and Newton, holding an apple requires about 1N of force. Why you ask? Most apples weigh around $.1kg$ and the acceleration of gravity is $9.8m/s^2$. So $F=m\times a$ is $\approx 1=.1\times 9.8$. So if it helps you conceptualize a Newton, holding an apple in front of you requires about 1 newton.

Ok... one more level back up, what is a joule then?

One joule is the amount of energy (effort) it takes to push with a force of 1 newton over a distance of meter. Said mathematically that is:

$$
1 \text{ Joule} = 1 \text{ Newton} \times 1 \text{ meter}
$$

So back to our apple example, you can imagine picking up an apple. If you were to pick up an apple and lift it exactly one meter, you expended one joule of energy to do that. Some every day examples:

| Action                              | Approx. energy (J) | Notes                                         |
| ----------------------------------- | ------------------ | --------------------------------------------- |
| Lifting an apple 1 meter            | 1 J                | Classic physics example                       |
| Typing one keystroke                | 0.001 J            | Almost nothing                                |
| Flicking a small light switch       | 1 J                | That satisfying click                         |
| Taking one step while walking       | 5–10 J             | Muscles + gravity                             |
| Lighting one small LED for 1 second | ~0.1 J             | If it’s a 0.1 W LED                           |
| Eating 1 food calorie (kcal)        | 4184 J             | One tiny bite of food has thousands of joules |

So a joule is a really small amount of energy. Finally, we are now ready to discuss watts. What the heck is a watt?

1 watt is 1 joule per second. So you can imagine picking up one apple, one meter, every second. That's a watt.

### Some Electric Units

Ok, so you now have an intuitive understanding of power. You're probably now asking, "What does that have to do with radio waves?" The mathematical answer is that the relationship is that power is equivalent to $P=V \times I$ where $V$ is the voltage and $I$ is the current. The problem is, if you're like me, you may not entirely grasp what those things are in an intuitive way. You've may have heard the water analogy where voltage is pressure and current is flow, but that doesn't really help us understand what something like RSRP or SINR are. For me to explain all this, we have to develop an intuitive understanding of the basic electric units. 

#### Current

Let's start with current. Current is measured in a unit called coulombs. To understand coulombs you need to understand what is "charge".

At the most basic level, electric charge is a property of matter — like mass - that determines how it interacts with electric and magnetic fields.

- Electrons carry negative charge.
- Protons carry positive charge.
- Neutrons have no charge.

A coulomb is a specific amount of charge. 1 coulomb is $6.242 \times 10^{18}$ electrons or protons worth of charge. To be clear, a coulomb isn't a quantity of electrons or protons, but it's equivalent to the charge produced by $6.242 \times 10^{18}$ electrons or protons.

You probably know that we measure current in amps. One amp is the movement of one coulomb of charge flowing per second. To explain a bit more, this is where the water analogy you may have heard comes in. An electrical wire is already filled with electrons just as a hose could already be filled with water. When you apply a voltage (pressure), the electrons start to move. Why you ask? This is the fundamental definition of a conductor. In conductors like copper, aluminum, and gold, the outermost electrons of each atom are not bound tightly. We call this a sea of free electrons. Here's what happens when electricity (electrons) "flows".

- The atoms are arranged in a crystal lattice.
- Each atom gives up one (or more) of its outer electrons.
- Those electrons are delocalized — meaning they’re free to move anywhere inside the metal.

So inside a copper wire:

- The positive atomic cores stay in fixed lattice positions.
- The electrons form a free-moving cloud that can drift around.

**When no voltage is applied:**

- The electrons are moving randomly in all directions because of thermal energy (they “buzz around” at high speeds, $\approx 10^6 m/s$).
- But these random motions cancel each other out - there’s no net flow of charge, so no current.

**When voltage is applied:**

- An electric field is established throughout the wire almost instantly (at a significant fraction of the speed of light).
- This field causes all those free electrons to drift slightly in one direction on average, superimposed on their chaotic thermal motion.

That drift - just a small bias in their otherwise random motion — is the current.

You might be surprised how slow electrons actually drift.

Even though electricity seems instantaneous, the drift velocity of electrons in a wire is typically only:

$$
v_d \approx \frac{I}{n e A}
$$

where

- ($I$) = current,
- ($n$) = number of free electrons per cubic meter (~10²⁹/m³ for copper),
- ($e$) = electron charge,
- ($A$) = cross-sectional area of the wire.

For a 2 mm diameter copper wire carrying 1 ampere:

$$
v_d \approx 0.0003\ \text{m/s} = 0.3\ \text{mm/s}.
$$

So electrons drift only a few tenths of a millimeter per second! You can check out the full math for that calculation [here](./calculating_electrical_drift.md)

But the *signal* moves at nearly light speed

When you flip a switch, the electric field travels through the wire at roughly two-thirds the speed of light (depending on insulation).

That field instantly pushes on electrons all along the wire - just like pushing one end of a long pipe full of marbles makes a marble pop out the other end almost immediately.

So what's the difference between an insulator and a conductor?

- In insulators, electrons are tightly bound to their atoms. They can only "vibrate" in place — no free conduction occurs.
- In semiconductors (like silicon), some electrons can break free and move if you add energy (heat, light, or voltage). This is how transistors work.

So in conductors electrons actually drift through the material. In insulators electrons mostly vibrate but don’t drift. In semiconductors some electrons drift when conditions allow.

So to wrap all this up: One amp ($A$) is the movement of on coulomb ($6.242 \times 10^{18}$ electrons or protons worth of charge) per second. If it helps imagine how much that is, most USB chargers, charge a phone at 2A.

#### Volts (electric potential energy)

Volts I think is a little harder to understand than amps. Formally a volt is how much energy is available per unit of charge:

$$
1 \text{ volt} = 1 \text{ joule per coulomb }1V=1J/C
$$

When we say "1 volt = 1 joule per coulomb," we're saying:

> If you move 1 coulomb of electric charge through a 1-volt difference, that charge gains or loses 1 joule of energy.

That energy isn’t "inside" the charge like a little battery; it's the energy associated with its position in an electric field, just like an apple has energy because of its position in gravity. That is to say, when you expend one joule of energy picking up a .1kg apple, 1m off the ground, you just gave the apple potential energy. Specifically, you gave it 1 joule of potential energy.

Electricity is actually pretty similar. The only difference is that instead of gravity being the source of potential energy, it's electrical fields. 

A volt (V) is defined as one joule per coulomb:

$$
1\ \text{V} = 1\ \frac{\text{J}}{\text{C}}
$$

That means:

if 1 coulomb of electric charge gains (or loses) 1 joule of energy when moving between two points, the voltage (or electric potential difference) between those two points is 1 volt.

So tying this back to power $P=V\times I$. Voltage is telling you how much energy each coulomb carries and current tells you how many coulombs pass per second. If you were to multiply them together, you get how many joulers per second are moving through the circuit. Expressed mathematically:

$$
P = V \times I
$$

where

- (P) = power (in watts, W)
- (V) = voltage (in volts, J/C)
- (I) = current (in amperes, C/s)

If you multiply them:

$$
\text{J/C} \times \text{C/s} = \text{J/s}
$$

and a joule per second is a watt. So when you cancel the terms out you get 1 W = 1 J/s — one joule of energy flowing each second.

### Decibels

The problem with 5G things is that while we measure thing in watts, the power values in wireless is really small. A base station might transmit in tens of watts, but by the time that signal reaches your phone, it's in the range of picowatts ($10^{12}$W) or even femtowatts ($10^{15}$W). So to add one more layer of complexity, this has lead engineers to use decibels to make these values easier to compare and express. Unlike the other units we've talked about, a decibel doesn't relate back to something physical. A decibel is a logarithmic ratio - it compares one power to another.

#### Decibels (dB)

A **decibel** is a logarithmic ratio — it compares one power to another:

$$
\text{dB} = 10 \times \log_{10}\left(\frac{P_1}{P_2}\right)
$$

- It doesn’t have units (it’s a ratio).
- It tells you how many times stronger or weaker one power is compared to another. So in the equation above you can think of it as saying, "How many times stronger or weaker is $P_1$ than $P_2$.

So a few examples:

* 10× more power → +10 dB
* 100× more power → +20 dB
* 0.1× the power → −10 dB

**1. 10× more power → +10 dB**

$$
\frac{P_1}{P_2} = 10
$$

$$
10 \log_{10}(10) = 10 \times 1 = 10\ \text{dB}
$$

**2. 100× more power → +20 dB**

$$
\frac{P_1}{P_2} = 100 = 10^2
$$

$$
10 \log_{10}(100) = 10 \log_{10}(10^2) = 10 \times 2 = 20\ \text{dB}
$$

**3. 0.1× the power → −10 dB**

$$
\frac{P_1}{P_2} = 0.1 = 10^{-1}
$$

$$
10 \log_{10}(0.1) = 10 \log_{10}(10^{-1}) = 10 \times (-1) = -10\ \text{dB}
$$

To wrap dB up, dB is a simple ratio between one power and another.

#### Decibel-Miliwatt (dBm)

So how is it possible then to measure the power of something using dBs then? The problem with powers in 5G as I mentioned before is that they are small. Really small. As I mentioned above, dB is just a ratio of two powers. dBm likewise is a ratio between two powers, except in this case we just define $P_2$. dBm is the same as saying "How many decibels stronger or weaker is this power than 1 milliwatt?" 

Expressed mathematically:

$$
P_{\text{dBm}} = 10 \times \log_{10}\left(\frac{P_\text{watts}}{1\text{ mW}}\right)
$$

Some examples:

- 0 dBm = 1 milliwatt
- +10 dBm = 10 milliwatts (10 × stronger)
- +20 dBm = 100 milliwatts (100 × stronger)
- −10 dBm = 0.1 milliwatt (10 × weaker)
- −90 dBm = 0.000 000 000 001 W (super faint)

$$
\text{dBm} = 10 \log_{10}\left(\frac{P}{1\text{ mW}}\right)
$$

### Examples

1. **0 dBm**

$$
0 = 10 \log_{10}\left(\frac{P}{1\text{ mW}}\right)
$$

$$
\frac{P}{1\text{ mW}} = 10^{0/10} = 1
$$

$$
P = 1\text{ mW}
$$

---

2. **+10 dBm**

$$
10 = 10 \log_{10}\left(\frac{P}{1\text{ mW}}\right)
$$

$$
\frac{P}{1\text{ mW}} = 10^{10/10} = 10
$$

$$
P = 10\text{ mW}
$$

---

3. **+20 dBm**

$$
20 = 10 \log_{10}\left(\frac{P}{1\text{ mW}}\right)
$$

$$
\frac{P}{1\text{ mW}} = 10^{20/10} = 100
$$

$$
P = 100\text{ mW}
$$

---

4. **−10 dBm**

$$
-10 = 10 \log_{10}\left(\frac{P}{1\text{ mW}}\right)
$$

$$
\frac{P}{1\text{ mW}} = 10^{-10/10} = 0.1
$$

$$
P = 0.1\text{ mW}
$$

---

5. **−90 dBm**

$$
-90 = 10 \log_{10}\left(\frac{P}{1\text{ mW}}\right)
$$

$$
\frac{P}{1\text{ mW}} = 10^{-90/10} = 10^{-9}
$$

$$
P = 10^{-9}\text{ mW} = 10^{-12}\text{ W}
$$

---

| Level | Power (mW) | Power (W) |
|--------|-------------|-----------|
| 0 dBm | 1 | 0.001 |
| +10 dBm | 10 | 0.01 |
| +20 dBm | 100 | 0.1 |
| −10 dBm | 0.1 | 0.0001 |
| −90 dBm | 10⁻⁹ | 10⁻¹² |

The table will give you a rough idea for some common ranges in 5G:

| Power (W) | Power (mW)        | dBm      | Interpretation                  |
| --------- | ----------------- | -------- | ------------------------------- |
| 1 W       | 1000 mW           | +30 dBm  | Very strong RF output           |
| 0.1 W     | 100 mW            | +20 dBm  | Typical Wi-Fi transmit power    |
| 0.001 W   | 1 mW              | 0 dBm    | Reference level                 |
| 1 μW      | 0.001 mW          | −30 dBm  | Weak received signal            |
| 1 nW      | 0.000001 mW       | −60 dBm  | Fainter signal                  |
| 1 pW      | 0.000000001 mW    | −90 dBm  | Very faint                      |
| 1 fW      | 0.000000000001 mW | −120 dBm | Barely detectable at a receiver |

So when your phone shows RSRP = −95 dBm, that means:

$$
10^{(-95/10)} \times 1\text{ mW} = 3.16 \times 10^{-13}\ \text{W}
$$

or 0.316 picowatts of received signal power.

One last way to look at it are some common sounds measured in dBm:

| Description                          | Power (W) | dBm      | Analogy        |
| ------------------------------------ | --------- | -------- | -------------- |
| Shouting directly into someone’s ear | 1 W       | +30 dBm  | Loud           |
| Talking normally                     | 1 mW      | 0 dBm    | Baseline       |
| Talking across a football field      | 1 nW      | −60 dBm  | Barely heard   |
| Whisper from a mountaintop away      | 1 fW      | −120 dBm | Almost silence |

Now that we truly understand all the background, we're ready to tackle the 5G measurements.

## 5G Measurements

There are four values we really want to understand: RSRP, RSRQ, SINR, RSSI.

Here’s your updated table with the **units column** added:

| Metric                                             | Measures                                                     | Analogy                                                            | Units                          |
| -------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------ |
| **RSRP** (Reference Signal Received Power)         | How strong the tower’s *intended* signal is                  | Volume of one specific voice in a crowd                            | **dBm** (absolute power level) |
| **RSRQ** (Reference Signal Received Quality)       | How clean that signal is compared to everything else         | Clarity of that voice among all others                             | **dB** (ratio)                 |
| **SINR** (Signal-to-Interference-plus-Noise Ratio) | How dominant the desired signal is over interference + noise | How much louder the voice is than the crowd and static             | **dB** (ratio)                 |
| **RSSI** (Received Signal Strength Indicator)      | The *total* received power — signal + interference + noise   | The overall loudness of the entire room (everyone talking at once) | **dBm** (absolute power level) |

In short:

* **RSRP** isolates the cell's beacon power.
* **RSSI** is the whole soup of power your receiver sees.
* **RSRQ** compares those two to judge how clean the channel is.
* **SINR** measures how much the useful part dominates over the rest.

### Signal-to-Interference-plus-Noise Ratio (SINR)

The point of SINR is to understand how well a receiver, our phone for example, can decode the signal it receives not just how strong the signal is. SINR compares the power of the desired signal to the power of everything unwanted (interference from other signals and random noise). So when we express this mathematically:

$$
\text{SINR} = \frac{P_\text{signal}}{P_\text{interference} + P_\text{noise}}
$$

Where:

- $(P_\text{signal})$ = power of the desired signal
- $(P_\text{interference})$ = combined power of all other unwanted signals (e.g., other cells)
- $(P_\text{noise})$ = thermal or electronic noise floor in the receiver

It’s a ratio — the signal compared to the junk. Usually we express it in decibels (dB):

$$
\text{SINR}_{\text{dB}} = 10 \log_{10}\left(\frac{P_{\text{signal}}}{P_{\text{interference}} + P_{\text{noise}}}\right)
$$

We measure SINR in dB because the values for SINR can vary widely so expressing it in dB gives us more tractable values. Let's assume SINR is 14:

$$
\mathrm{SINR}_{\mathrm{dB}} = 14
$$

If we want to change from the dB logarithmic scale to linear we can do:

$$
\mathrm{SINR} = 10^{\frac{\mathrm{SINR}_{\mathrm{dB}}}{10}}
= 10^{\frac{14}{10}}
= 10^{1.4}
\approx 25.118864315 \;\;\approx\; 25.1
$$

This is then telling us that our signal is 25.1 times more powerful than the noise and interference.

$$
\frac{P_{\text{signal}}}{P_{\text{interference}} + P_{\text{noise}}}
= \mathrm{SINR}
\approx 25.1
$$

Spelled out in our original equation:

$$
10\log_{10}(25.118864315) = 14 \ \text{dB}
$$

What does this mean in the physical world? Your phone’s antenna and receiver are picking up a mixture of electromagnetic waves at the same frequency band.

- The tower you’re connected to contributes the desired waveform.
- Neighboring towers and random RF sources contribute interference.
- The phone’s own electronics and the environment contribute noise (random motion of electrons, cosmic background, etc.).

The phone demodulator estimates the ratio of the clean part of the waveform (that matches its reference signals) to everything else. That’s SINR.

Most importantly, LTE/5G dynamically pick modulation schemes based on SINR:

| SINR (dB) | Typical Modulation | Data Rate Quality    |
| --------- | ------------------ | -------------------- |
| < 0 dB    | BPSK / QPSK        | Barely holding link  |
| 5–10 dB   | 16-QAM             | Moderate throughput  |
| 15–20 dB  | 64-QAM             | High throughput      |
| > 25 dB   | 256-QAM+           | Excellent throughput |

### Reference Signal Receive Power (RSRP)

A cell tower sends out reference signals (pilot tones) at regular intervals. The reference signals are beacons the phone locks onto to measure how strong the connection is for that tower. RSRP is the average power per reference signal resource element. Resource element is out of scope for our conversation here, but it's basically a chunk of data in 5G. It's one subcarrier $\times$ one orthogonal frequency division multiplexing (OFDM) symbol.

In simple terms, RSRP is:

- The pure strength of the cell's reference signal.  
- It’s measured in dBm (a power level, not a ratio).  
- It ignores interference and noise — it just cares about how strong the reference signal itself is.

We can express this mathematically as:

$$
RSRP = \frac{1}{N} \sum_{i=1}^{N} P_{RS,i}
$$

Where:

- $N = \text{number of reference signal resource elements}$  
- $P_{RS,i} = \text{received power of the } i^{th} \text{ reference signal element (in watts)}$  
- $RSRP = \text{average received power of all reference signal elements}$

Some commmon ranges:

| RSRP (dBm)   | Signal strength | Meaning              |
| ------------ | --------------- | -------------------- |
| −60 to −80   | Excellent       | Close to the tower   |
| −80 to −90   | Good            | Normal coverage      |
| −90 to −100  | Fair            | Edge of good service |
| −100 to −110 | Poor            | Possible drops       |
| < −110       | Very poor       | Barely usable        |

So if you have a RSRP of -100, that's the same as saying that your signal is 100 billion times weaker than a milliwatt.

To convert −100 dBm to watts:

$$
P_{dBm} = -100
$$

Step 1 — Convert dBm → mW:

$$
P_{mW} = 10^{\frac{P_{dBm}}{10}} = 10^{\frac{-100}{10}} = 10^{-10}
$$

$$
P_{mW} = 0.0000000001 \text{ mW}
$$

Step 2 — Convert mW → W:

$$
P_{W} = P_{mW} \times 10^{-3} = 10^{-10} \times 10^{-3} = 10^{-13}
$$

$$
P_{W} = 0.0000000000001 \text{ W}
$$

An RSRP of −100 dBm means the received reference signal power is  $( 1\times10^{-13} )$ watts - an incredibly faint signal, roughly 100 billion times weaker than 1 mW.

RSRP is actually a part of SINR. I thought it would be easier to explain in terms of power above, but SINR is:

$$
\text{SINR} = \frac{\text{RSRP}}{P_{\text{interference}} + P_{\text{noise}}}
$$

### Received Signal Strength Indicator (RSSI)

We can now measure the signal to noise ratio and the absolute power of our pilot signal, but what we don't currently measure is the total power of everything. That's what RSSI does. It's the total power of everything:

- The desired cell’s signal  
- Neighboring cells’ signals (interference)  
- Background noise

As you can imagine, the formula is similar to SINR except it's just:

$$
RSSI = P_{signal} + P_{interference} + P_{noise}
$$

In practice, this is the total energy measured across all resource elements in the measured bandwidth.

Since it is a measurement of power we measure it in dBm. There's not much more to say so I'll leave it at that.

### Reference Signal Received Quality (RSRQ)

Now that we understand RSRP and RSSI, we have the tools available to understand RSRQ. RSRQ measures signal quality, combining both the signal strength (RSRP) and the total received power (RSSI) into one metric. It tells you how "efficient" the signal is. IE, it tells you how much of the total received energy actually belongs to the desired cell.

Expressed mathematically it is:

$$
RSRQ = \frac{N \times RSRP}{RSSI}
$$

where:

- $(RSRP)$: average power of the reference signals (dBm)  
- $(RSSI)$: total received power (signal + interference + noise) (dBm)  
- $(N)$: number of resource blocks (the bandwidth used for the measurement)

So if you combine that with the other concepts we've covered:

- RSRP alone tells you how strong the desired tower’s beacon is.  
- RSSI tells you the total energy received — good + bad.  
- So RSRQ is basically the ratio of useful signal power to total power, adjusted for bandwidth.

You're still probably a bit confused by what the $N$ is doing. RSRP **only** measures the power of the resource blocks for the pilot signals we mentioned earlier, whereas RSSI measures measures the power of ALL the resource blocks for some time slot. You can visually imagine it like this:

| Time → |  Slot 1  |  Slot 2  |  Slot 3  |  Slot 4  |  Slot 5  |
|:-------:|:--------:|:--------:|:--------:|:--------:|:--------:|
| **Freq 1** | D | D | R | D | D |
| **Freq 2** | D | . | D | . | R |
| **Freq 3** | R | D | D | D | . |
| **Freq 4** | D | R | D | D | D |
| **Freq 5** | D | D | . | R | D |

R = Reference Signal (used for RSRP)  
D = Data/Noise/Other (contributes to RSSI)

So RSRP is only capturing the power of one resource block per time slot there but RSSI is capturing all 5. So to make the comparison make sense we multiply RSRP by 5 (the number of resource blocks.)

Here are some referenc values to keep in mind:

|    RSRQ (dB)   | Signal Quality | Description                                                      |
| :------------: | :------------- | :--------------------------------------------------------------- |
|  **-3 to -6**  | Excellent      | Very clean signal with low interference and good SINR.           |
|  **-7 to -9**  | Good           | Normal operating conditions for most LTE/5G cells.               |
| **-10 to -12** | Fair           | Some interference or loading on the cell; data rates might drop. |
| **-13 to -15** | Poor           | Heavily loaded or noisy cell; connection may fluctuate.          |
|    **< -15**   | Very Poor      | Borderline unusable — strong interference or far from tower.     |

- RSRQ ≈ RSRP adjusted for how "busy" or "noisy" the channel is.
  - So if RSRP (signal power) is fine but RSRQ is bad, it usually means interference or congestion is the issue, not distance.
- Good LTE/5G networks typically aim to keep RSRQ better than -10 dB.

### Wrap Up

So to wrap things up, here is a final way you can think about viewing RSRP, SINR, and performance metrics.

| Category                | What it tells you                   | Examples                           |
| ----------------------- | ----------------------------------- | ---------------------------------- |
| **Coverage / Strength** | How strong the received signal is   | RSRP, RSSI                         |
| **Quality**             | How clean or usable that signal is  | RSRQ, SINR                     |
| **Performance**         | How much data you can actually move | Throughput, Modulation scheme, CQI |
