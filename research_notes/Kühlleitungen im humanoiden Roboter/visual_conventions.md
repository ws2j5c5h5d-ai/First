# Visual conventions for coolant hoses on liquid-cooled robot limbs (as of Oct 2026)

Scope: what real hardware looks like, as a reference for a realistic illustration of coolant lines in a humanoid. "Confirmed" means sourced. "Inference" is marked as such. I could not view photos directly. Visual details come from text descriptions, figure captions and datasheets, not from looking at images.

## 1. Real liquid-cooled legs and humanoids: are hoses outside, and are there loops at the joints?

### Takeaway
In the documented research hardware (UT Austin HCRL / Apptronik DRACO), each motor sits in a separate cooling jacket. A pump, radiator and reservoir from the PC water-cooling market feed the jackets through flexible tubing. Honor's 2026 marathon winner "Lightning" has an independent circuit per lower-limb drive motor and an external radiator. None of the sources I found describe exactly how the hoses run around the knee or ankle. Treat any knee or ankle loops as an inference from general hose practice, not as something documented.

### Cited Findings
- DRACO (UT Austin HCRL + Apptronik) used "liquid-cooling motor jackets" on its VLCAs (viscoelastic liquid-cooled actuators), giving 2.5x higher continuous torque. The actuators are prismatic, ball-screw linear units mounted along the leg links. — [Ahn et al., arXiv 1906.03811](https://arxiv.org/pdf/1906.03811)
- VLCA testbed: a Maxon EC-max 40 motor in "a custom housing designed for the liquid cooling system". "The liquid pump, radiator, and reservoir are products of Swiftech", weighing about 1 kg. — [Kim et al., arXiv 1711.01649](https://arxiv.org/html/1711.01649v2)
- In the predecessor retrofit (Paine & Sentis 2015), the radiator, reservoir, pump and fittings are Swiftech PC water-cooling parts. "High-flex PVC (polyvinyl chloride) tubing was used to connect these components together." The motor jacket was 3D-printed from watertight acrylic polymer and ran at about 1.5 bar. The paper notes that one pump can serve several motors. — [Paine & Sentis, Actuators 4(3) 2015](https://www.mdpi.com/2076-0825/4/3/182)
- DRACO leg prototype video (2017): "Draco liquid cooled prototype leg". — [HCRL blog](https://sites.utexas.edu/hcrl/2017/07/25/behold-the-draco-liquid-cooled-compliant-robotic-leg-prototype-%F0%9F%8F%8B%EF%B8%8F%E2%80%8D%E2%99%80%EF%B8%8F%F0%9F%8F%83%E2%80%8D%E2%99%82%EF%B8%8F%F0%9F%8F%87); [YouTube](https://www.youtube.com/watch?v=iUS0qoHO6Ac)
- Apptronik describes Draco as a "liquid-cooled, 10-degree-of-freedom bipedal system". — [Apptronik](https://apptronik.com/company/our-work)
- Honor Lightning (half marathon, 19 Apr 2026, 50:26): "liquid-cooling pipes penetrate deep into the motors like capillaries"; pump flow above 4 L/min; "Each of the four drive motors in the lower limbs is equipped with an independent liquid-cooling circuit." — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- During the race, "Honor's robots carried liquid-cooling radiators and continued to run". Engineers also sprayed liquid nitrogen on exposed joints such as the knees. — [36Kr / IT Times](https://eu.36kr.com/en/p/3779311984284678)
- The Lightning pump comes from the supplier Huake Lengxin. Unitree uses air cooling instead (ducts plus two fans per leg). AgiBot's (ZhiYuan) PowerFlow joint and CloudMinds' A1 also use liquid cooling. — [36Kr](https://eu.36kr.com/en/p/3775418378027520)
- Unitree G1 spec: "Cooling System: Local air cooling" and "Full Joint Hollow Electrical Routing". So there is no liquid-cooled G1 variant on the spec page. — [Unitree G1](https://www.unitree.com/mobile/g1/)
- HKUST-GZ AMDT Lab has a project on "Integrated Liquid Cooling Joint Actuators for Humanoid Robot Applications". It says related technology was adopted by Honor Lightning and Tiangong. The page gives no visual or hose details. — [AMDT](https://amdt.hkust-gz.edu.cn/projects/Liquid_Cooling_Joint_Actuators)
- A 2025 IEEE paper describes a "leg structure with concentrated liquid-cooling actuators" for humanoids. Only the abstract was available. — [Jin et al., IEEE](https://ieeexplore.ieee.org/document/11203109)
- The hydraulic Atlas used 3D-printed links with "hose-less routing of the hydraulic fluid" built into the structure. — [arXiv 2411.11734](https://arxiv.org/html/2411.11734v1)
- JSK's Kengoro had "no room to add active water cooling with tubes and a radiator". It used porous "sweating" frames instead. SCHAFT used liquid-cooled motors. — [IEEE Spectrum 2016](https://spectrum.ieee.org/this-robot-can-do-more-pushups-because-it-sweats)

### Inferences
- In the DRACO/VLCA style, each actuator jacket probably has two short flexible tubes (in and out) that run along the link to a pump and radiator on the torso or pelvis. With linear actuators mounted along the links, the tubes mostly cross a joint near its pivot. That makes small, slack arcs at the hip, knee and ankle more plausible than large loops.
- For Lightning-style designs, one supply and one return per cooled motor gives about 4 lines per leg if knee and hip are cooled. In practice this could be fewer if lines share a manifold. Honor has not confirmed the details.
- Production-oriented humanoids (Unitree, Atlas) route things through hollow joints or integrated channels. A clean commercial design is therefore likely to hide most lines, and visible external hoses read as "prototype" or "test rig".

### Gaps
- I found no published photo description of how Lightning's or Tiangong's hoses are routed (internal vs external, at the knee or ankle) or what colour they are.
- I found no specific MIT or KAIST liquid-cooled actuator hardware. The HKUST-GZ project page has no figures in text form.
- I could not verify any liquid-cooled Unitree H1 or G1 variant. Unitree's public stance is air cooling.

## 2. Industrial dress-pack practice: routing across axes, loops, clamps, bend radius

### Takeaway
On a 6-axis arm, the dress pack runs in corrugated PA tubing or a triflex-style chain. It is fixed at defined points on each segment (axes 1–2, 2–3, 3–6), has a retraction system on the upper arm (axis 3), and has short service loops at each fixed point. The hose is kept close to the joint axes so its length changes little. Bend radius targets are about 5–12× OD for dynamic flexing.

### Cited Findings
- igus recommends splitting the dress pack into three segments (axes 6→3, 3→2, 2→1). Each segment gets strain relief with a "one- to two-foot service loop" and a junction box. Around axis 1 it uses a "reverse-bend cable carrier". — [igus](https://www.igus.com/robot-dress-pack/robot-cable-management-solutions)
- Corrugated tubing covers the lines "from the base plate below Axis 1 to their exit at Axis 6"; "the most widely used material is polyamide (PA12)". A spring-return system handles "the service loop portion... between Axis 3 and Axis 6". The axis-6 support is called the "tennis racket / frying pan". — [Helukabel via RoboticsTomorrow](https://www.roboticstomorrow.com/article/2021/12/robotic-dress-pack-component-basics/17947)
- LEONI LSH: "A specially designed casing guides the dresspack from axes 3 - 6 at variable lengths. A spring retraction system, inside the casing, adjusts the length." — [LEONI brochure](https://2.imimg.com/data2/UG/EI/MY-2495974/robotic-dress-pack.pdf)
- igus RSP: the retraction unit mounts on axis 3, and the chain is fixed at the axis-6 "tennis racket". — [igus RSP](https://www.igus.com/robot-dress-pack/triflex-rsp-assembly-instructions)
- triflex R has a "built-in torsion stop, defined bend radius and split cavity". Cobot kits fix it with hook-and-loop (Velcro) straps on the links. — [igus](https://www.igus.com/robot-dress-pack/dresspack-for-robot-manufacturers); [igus CRX](https://www.igus.com/robot-dress-pack/triflexr-dresspacks-for-fanuc-crx)
- Routing rules: fix the package "at defined points on each axis, not only at the base and the tool"; "clamp each core at its own diameter"; leave service loops that "cannot foul anything through the cycle"; run "air, coolant... so that a leak drains away from electrical cores". For bend radius, "12× outer diameter is a common design target" for high-flex cable, and you should check the radius at the extreme poses. — [Becker Robotic](https://becker-robotic.com/knowledge-base/routing-rules)
- A dynamic dress-pack branch should start at about 10× cable OD, with drag-chain fill under about 60%. — [roboticscableassembly.com](https://roboticscableassembly.com/blog/robot-dress-pack-cable-routing-guide)
- Robot cable minimum dynamic bend radius is 5–7.5× OD, and the energy-chain bend factor is "typically 5× to 10×". — [LCSC](https://www.lcsc.com/blog/top-robotic-cable-products-selection-guide-for-2026/)
- Length change near the axis (confirmed): a wrist hose centreline through the joint has "constant length during the bending". Hoses mounted on the outside of a joint "bind against the joint" and see large bending changes. The Berkshire Grey patent instead routes them out-of-plane to minimise changes in bending. — [US20060243087A1](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20060243087); [US20250042019A1](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20250042019)
- Torsion dominates on the wrist axes (4–6). Spread the twist over a free length; a twist clamped at both ends of a short run fails at the clamp. — [Becker Robotic](https://becker-robotic.com/knowledge-base/routing-rules)
- Tubing data:
  - SMC PU TU0604 (6×4 mm): min bend radius 15 mm. TU0425: 10 mm. TU1208: 35 mm.
  - SMC PU comes in many colours, including clear, blue, black and red. Water use is rated 0–40 °C.
  - Festo PUN-H 6×1: min bend radius 10 mm, but the "flow-relevant" bend radius is 26 mm. It is also sold as PUN-DUO, two tubes welded side by side.
  - FEP ½" OD: bend radius 2".
  - Sources: [SMC TU](https://static.smc.eu/pdf/TU-29COLOR-A_EU.pdf); [Festo PUN](https://ftp.festo.com/Public/PNEUMATIC/SOFTWARE_SERVICE/Documentation/2025/EN/PUN_PUN_DUO_EN.PDF); [Festo DUO datasheet](https://ftp.festo.com/Public/PNEUMATIC/SOFTWARE_SERVICE/DataSheet/EN_US/197397.pdf); [Polyconn FEP](https://www.polyconn.com/fep-tubing-1-2-od)
- Hydraulic hose practice: keep a minimum free length of about 4×OD plus ½ the bend radius next to a fitting, and don't start the bend within one diameter of the ferrule. Between moving planes, hang the hose in an arc ("like a rainbow") and secure the middle with a clamp. — [NAHAD via hoseandfittings](https://www.hoseandfittings.com/product-groups/hydraulic-hoses/hose-routing); [mfgrobots](https://www.mfgrobots.com/Article/equipment/industry/46828.html)

### Inferences
- What this means for the humanoid image:
  - Run the lines along the back of the thigh and shank, or along the inner side, and cross the knee close to the pivot axis on its flexion-neutral side. For the knee that is roughly the lateral or medial face at the axis, not across the kneecap.
  - Give each crossing a gentle C-shaped arc, not a tight loop.
  - Fix the lines just above and below each joint with small P-clips or saddle clamps. A lightweight robot might use hook-and-loop straps or printed clips.
  - Keep the lines straight and fixed along the link between clamps.
- Size check: a 6 mm PU tube needs at least about 15 mm radius, roughly a thumb's width, and about 26 mm or more for good flow. Lines bent sharper than that at the knee look wrong.
- An industrial-style corrugated conduit or triflex chain on a humanoid limb would look like an industrial arm and is probably too bulky. Spiral wrap or a textile sleeve around the supply/return pair is more plausible for a prototype.

### Gaps
- I found no humanoid-specific dress-pack guidance. All the rules above are transferred from industrial arms and general hose practice.

## 3. Colour coding: supply vs return, pneumatics, vacuum

### Takeaway
For liquid cooling there is a strong industry convention of blue = supply/cold/inlet and red = return/hot/outlet. It is usually applied as coloured rings on couplings or as coloured tubing. Pneumatic PU tubing is mostly blue (or black, or blue/black). No binding standard was found for robot coolant hose colour.

### Cited Findings
- Stäubli RPL couplings: "Red and blue rings ensure instant identification of hot and cold water circuits." — [Stäubli RPL](https://www.staubli.com/global/en/fluid-connectors/products/quick-and-dry-disconnect-couplings/temperature-control/rpl-full-flow.html)
- Stäubli SCG and DAG thermal-management couplings: blue or red rings "identify the inlet and the outlet circuits". — [SCG](https://www.staubli.com/global/en/fluid-connectors/products/quick-and-dry-disconnect-couplings/thermal-management/scg-nickel-plated-brass.html); [DAG](https://www.staubli.com/global/en/fluid-connectors/products/quick-and-dry-disconnect-couplings/thermal-management/dag-automatic-coupling.html)
- Stäubli UQD (data-centre liquid cooling): "visual marking in blue and red to easily identify the inlet and outlet circuits". — [Stäubli UQD](https://www.staubli.com/cz/en/fluid-connectors/products/quick-and-dry-disconnect-couplings/thermal-management/uqd-universal-quick-disconnect.html)
- OCP liquid-cooling guide: "Color-coding red and blue on the coupling halves is another popular way to eliminate cross connection, all though it is not 100% fool proof." It also keys supply and return with male vs female couplings. — [OCP](https://www.opencompute.org/documents/ocp-manual-couplings-at-hoses-pdf/)
- Pneumatic PU tubing is typically solid blue (SMC). Festo PUN is offered in blue, blue/black, yellow, green, red, silver and black. — [SMC](https://www.smcpneumatics.com/americansmc/Tubing/2_Polyurethane_Tubing.pdf); [Festo PUN](https://ftp.festo.com/Public/PNEUMATIC/SOFTWARE_SERVICE/Documentation/2025/EN/PUN_PUN_DUO_EN.PDF)
- igus RSP example: a red hose for the pressure-equalising unit and a green air supply. This shows that pneumatic colours are often project-specific. — [igus RSP](https://www.igus.com/robot-dress-pack/triflex-rsp-assembly-instructions)
- Research rigs used generic "high-flex PVC" tubing from PC water cooling (Paine & Sentis). That kind of tubing is typically clear. Colour inferred; the source doesn't state it. — [MDPI](https://www.mdpi.com/2076-0825/4/3/182)

### Inferences
- A plausible palette:
  - Coolant: a supply/return pair, either both black or translucent with blue and red rings or tape at the ends and connectors. Alternatively, one blue and one red PU tube.
  - Pneumatics, if any: blue PU.
  - Vacuum: often clear or another distinct colour (no standard source found).
- Bright fully-red/fully-blue tubes read as "demonstrative". Black or clear tubes with coloured markings at the ends read as more "engineered".

### Gaps
- I found no ISO standard that prescribes robot coolant hose colours. The colour standards I know of for pipelines (e.g. DIN 2403 / ISO 14726) apply to building or ship piping; I did not verify them for this purpose. I found no vacuum-line colour convention.

## 4. Visual errors to avoid in renders

### Takeaway
The main errors are physical: lines running through bearings or rotating housings, bends tighter than the tube allows, lines on the outside of a large-swing joint with no slack, missing clamps, and too many lines.

### Cited Findings
- Lines through a continuously rotating joint need a rotary union or swivel. "Rotary unions/joints seal and transfer fluids like water... from static to 360° continuous rotating parts." — [Moflon](https://www.moflon.com/rotary-unions)
- The new electric Atlas has "fully rotational joints" (continuous rotation). An external hose across such a joint would wrap around it. — [IEEE Robots Guide](https://robots.ieee.org/robots/atlas)
- Hoses mounted on the outside of a joint bind against the joint when it flexes. — [US20250042019A1](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20250042019)
- Painting-robot wrists that carry hoses internally need conduits and even hose drives to avoid twisting the hose. Internal routing is engineered, not free. — [US20080011116A1](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20080011116)
- Don't install hoses twisted, don't bend them below the minimum bend radius, and don't put sharp bends at the fitting. — [NAHAD](https://www.hoseandfittings.com/product-groups/hydraulic-hoses/hose-routing)
- Don't clamp a whole bundle with a single ring, and don't leave loops that can foul anything during the motion cycle. — [Becker Robotic](https://becker-robotic.com/knowledge-base/routing-rules)
- Coolant lines should drain away from electronics if they leak. — [Becker Robotic](https://becker-robotic.com/knowledge-base/routing-rules)

### Inferences
- Line count: one supply/return pair per cooled actuator. Only the high-load joints (hip pitch, knee, possibly ankle) are likely to be cooled; Honor cools "four drive motors in the lower limbs". So a leg should show about 2–6 coolant lines, not a dozen. Arms are likely uncooled. Honor only mentions lower-limb cooling.
- Avoid:
  - lines passing through bearing faces or gear housings
  - lines that disappear into a rotating housing with no visible grommet or bulkhead fitting
  - lines draped across the front of the knee (they would be stretched during flexion)
  - perfectly taut lines between links
  - a shared radiator with no visible pump and reservoir (or pump plus integrated reservoir)
- Endpoints: lines should end at visible barbed or push-in fittings, or at small quick-disconnects, on each motor jacket, as an inlet and outlet a few cm apart.

### Gaps
- I found no published "common render mistakes" list. This section is synthesised from engineering rules.
