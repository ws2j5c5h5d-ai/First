# Placement of quick-disconnect couplings and screw-in fittings in liquid-cooled and pneumatic robot systems (validation of EISELE part locations)

Research date: 2026-10-20. Notation: "Confirmed" = taken from a cited source. "Inference" = my own reasoning or calculation, not stated by any source.

## Q1: Where do engineers put drip-free quick disconnects (QDs) in liquid-cooled systems?

### Takeaway
Industry practice puts drip-free/dry-break QDs **at module boundaries and service points**: CDU↔manifold, manifold↔server/blade, tool changer master↔tool, and battery module↔pack. The point of a QD is that one module can be removed without draining the loop. No source describes QDs as a way to bridge a moving joint. Joints use hoses, or rotary unions for continuous rotation. Placing SA2113 inline at the shoulder/arm-module or torso interface matches this practice, provided the coupling sits on a **static** interface and not across the moving joint itself.

### Cited Findings
- CPC tech guide: QDs are "vital in creating reliable cooling systems and supporting the modularity for serviceability". The loop's main QD locations are CDU-to-manifold, rack manifold-to-server, and in-server/cold plate. "The closer [the] connection points are to electronics, the greater the need for non-spill performance." Smallest Everis LQ2 = 1/8" nominal flow size, Cv 0.4. — [CPC Location and QD Specification Tech Guide](https://www.cpcworldwide.com/Portals/0/Downloadable-Content/TRM/Literature/Tech-Guides/CPC-Location-and-QD-Specification-Tech-Guide.pdf)
- Saint-Gobain: the manifold-to-server-tray connection "is typically a quick-disconnect coupling… allows the server tray to be removed for maintenance without draining the loop". Dripless/dry-break designs are standard so that residual coolant is not dropped "onto the server hardware below". OCP UQD defines hand-mate, drip-free, hot-pluggable connectors. — [Saint-Gobain: Inside the Direct-to-Chip Cooling Loop](https://www.ics.saint-gobain.com/resources/blog/inside-direct-chip-cooling-loop-components-coolant-chemistry-and-system-design-data)
- Eaton: "Fittings are used when disconnection of equipment is infrequent, since repeated removal can cause leaks… A coupling is a better fluid connector for systems that require fast assembly or routine maintenance. For example, modular equipment like a liquid-cooled chassis requires quick disconnect couplings." Non-spill (dry-break) is the variant for cases where any spill is a risk. — [Eaton: Fluid coupling and connector selection](https://www.eaton.com/us/en-us/products/thermal-management-solutions/power-electronics-cooling/couplers-hose-clamps-and-fitting-selection.html)
- Stäubli: drip-free QDs "enable hot-swap maintenance". Stäubli lists compact couplings "at blade level, adapted to connect cold plate" and blind-mate versions for racks. It quotes 5,000–10,000 mating cycles. — [Stäubli Data Centers](https://www.staubli.com/us/en/fluid-connectors/lp/data-centers.html); [Stäubli IT liquid cooling](https://www.staubli.com/us/en/fluid-connectors/industries/data-centers.html)
- Robot tool changers: ATI fluid/air modules pass coolant and air between master (robot side) and tool through **self-sealing ports** at the tool interface. Examples: FS2 has 4× G1/4 self-sealing plus G1/8 pass-through ports, max 6.9 bar. Several modules are marked "Not for vacuum service". — [ATI FS2](https://www.ati-ia.com/products/toolchanger/QCModule.aspx?ID=FS2); [ATI FH12](https://www.ati-ia.com/products/toolchanger/QCModule.aspx?ID=FH12)
- Schunk SWS tool changer: "transmission of fluid systems with self-sealing couplings possible" at the change interface. — [Schunk SWS](https://schunk.com/us/en/automation-technology/tool-changer/sws/c/PGR_1135)
- EV battery (patent application, 2026): quick-connect cooling/mounting connectors at the **module-to-pack interface**. The stated motive is that conventional packs have "many hoses and fluid connections… susceptible to leaking". — [US20260121164A1](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20260121164)
- EISELE SA2113-1 (SA2113K dry-break coupling) and SA2113-2 (SA2113S dry-break plug nipple): stainless steel 1.4404, FKM seal, M5, NW 2.5 mm, 0–10 bar, 0–100 °C, medium cooling water. Air and inert gases are also permitted. "Shut-off on both sides without dripping", "space-saving design for compact applications". — [EISELE SA2113-1](https://www.eisele-connectors.com/en/products/SA2113-1); [EISELE SA2113-2](https://www.eisele-connectors.com/en/products/SA2113-2); [EISELE quick couplings overview](https://www.eisele-connectors.com/en/product-overview/quick-disconnect-couplings)

### Inferences
- SA2113 at the arm-module/torso interface (e.g., where a detachable arm meets the shoulder flange) is plausible and matches the "module boundary / service point" pattern used in data centers, tool changers and EV packs. Two other plausible spots: the pump/radiator module service port, and a fill/drain point.
- SA2113 placed **across** a rotating joint is not plausible. No source uses a QD as a joint element. Joints carry flexible hose loops, or rotary unions for continuous rotation (see Q3).
- M5 / NW 2.5 is very small, smaller than the smallest CPC LQ2 (1/8"). This fits a low-flow branch (one arm or actuator) but not the main trunk of a whole-body loop.

### Gaps
- I found no public teardown or document showing where any commercial humanoid (Atlas, Optimus, Figure, Unitree) places coolant QDs. One 2026 Figure patent describes **air** cooling of torso compute and battery ([US12707556B1](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12707556)), so liquid cooling is not universal in humanoids.
- I found no Stäubli or CPC application note specific to humanoid robots.

## Q2: Are G1/8 screw-in fittings typical for small cold plates and actuator cooling jackets?

### Takeaway
G1/8 (and its 1/8" NPT equivalent) is a common small port for compact fluid modules and tool-changer pass-throughs. In PC/electronics water cooling, G1/4 is the de facto standard. Even smaller jackets use M5. The EISELE VT5528 aluminium series is explicitly meant for cooling water on aluminium heat sinks and power electronics. VT5528-0202 (G1/8 → OD4) on a small aluminium cold plate or actuator jacket is therefore plausible.

### Cited Findings
- EISELE VT5528 (Series 5528): aluminium, FKM, -0.95 to 16 bar, -20 to 120 °C, media compressed air, vacuum and cooling water. VT5528-0202 = G1/8, OD4. Listed application areas include power electronics, laser/semiconductor, wind turbines and transformers. — [EISELE VT5528-0202](https://www.eisele-connectors.com/en/products/VT5528-0202)
- EISELE: "Series 5500 with screw-in fittings of corrosion-resistant aluminum is designed for use in combination with aluminum heat sinks." — [EISELE screw-in fittings](https://www.eisele-connectors.com/en/product-overview/more/screw-in-fittings)
- The EISELE LIQUIDLINE catalogue lists "For electric heatsinks made of aluminum: Robotics…" and "Welding robots" among its cooling-water applications. — [EISELE LIQUIDLINE catalogue](https://pim.eisele.eu/Werbetr%C3%A4ger/Eisele_catalog_Liquidline_fr.pdf)
- PC water cooling: "Almost every watercooling component has the G1/4 thread" (community source, low authority). — [Reddit r/watercooling](https://www.reddit.com/r/watercooling/comments/37koqp/what_does_the_g14_thread_means_will_it_fit_with_a)
- An industrial water-cooled servo spindle (PushCorp STC1202) uses M5×0.8 push-lock fittings with 6 mm tubing on one of its ports. Larger water-cooled servo motors (Baumüller DSD2-132) use G1/2. — [PushCorp STC1202 manual](https://manuals.plus/m/6c5b74a452252de42be9db1e04399446fd0cb4ce4f60461b90c7b5ea3df2afed.pdf); [Baumüller DSD2](https://vecgroup.com/assets/pdf/%D0%A1%D0%B5%D1%80%D0%B2%D0%BE%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D1%82%D0%B5%D0%BB%D0%B8%20Baumuller%20DSD2-028-100.pdf)
- Tool changer fluid modules include G1/8 BSPP pass-through ports. — [ATI FS2](https://www.ati-ia.com/products/toolchanger/QCModule.aspx?ID=FS2)
- Humanoid joint cooling research (2026): an integrated annular liquid cooling ring around a humanoid joint actuator (ID 120 mm, OD 126 mm, 3 mm thick) with a "defined inlet–outlet manifold". It was evaluated at a 250 W peak load, with h ≈ 1340 W/m²K at **0.6 L/min**. — [ScienceDirect, Int. Commun. Heat Mass Transf. 2026](https://www.sciencedirect.com/science/article/pii/S0735193326017914)
- Earlier work on liquid-cooled cold plates for multiple heat sources in a humanoid robot (Kim et al., 2009) is cited in a 2025 Cell Device paper on flexible microfluidic chip cooling for humanoids. — [Cell Device 2025](https://cell.com/device/pdf/S2666-9986%2824%2900498-8.pdf)

### Inferences
- The thread scales with size: G1/8 for compact cold plates and actuator jackets (chest electronics, hip actuator), G1/4 for PC-class blocks, G1/2 for large industrial motors. VT5528-0202 suits a chest cold plate or hip actuator jacket, provided the plate wall can take a G1/8 port (roughly ≥8–10 mm boss). The boss size is my estimate and is not sourced.
- Aluminium fitting on an aluminium plate avoids galvanic pairing. This fits EISELE's stated purpose for Series 5500. It also argues against brass or stainless fittings on aluminium plates.

### Gaps
- I found no vendor datasheet (Wakefield, Boyd/Eaton, Lytron) stating G1/8 as the standard port for small cold plates. The Wakefield datasheets retrieved did not show port threads in the excerpts.

## Q3: Are M3/M5 push-in fittings standard for grippers, suction cups and hands? Is a swivel push-in OK on a moving wrist?

### Takeaway
Yes. M3 and M5 are the standard pneumatic ports on small grippers and vacuum pads (Festo, SMC, Schunk, Schmalz), and 3–4 mm tubing is normal there. Standard swivel elbows (EISELE 887, "-0.95 to 15 bar, compressed air, vacuum") are for **orienting the tube at installation**. Continuous or repeated rotation needs bearing-type rotary fittings (SMC KS/KX, EISELE rotary connector). An 887 mounted *on* the gripper body, which moves together with its tube, is fine. An 887 used as a rotating element in the wrist is not.

### Cited Findings
- Festo QSM mini push-in series: M3/M5 threads for 2/3/4 mm tubing, "compact for maximum component density in confined installation spaces". Operating medium: compressed air and vacuum (-0.95 bar). QSM-M5-3 weighs 3.4 g. — [Festo QSM catalogue](https://www.festo.com/media/catalog/203555_documentation.pdf); [Festo QSM-M5-3](https://www.festo.com/us/en/a/153302)
- Festo grippers: pneumatic connection M3 on small sizes and M5 on mid sizes (DHWS 10/16 = M3, 25 = M5; HGPP 10/12 = M3, 16–25 = M5; HGPT similar). — [Festo DHWS](https://ftp.festo.com/public/pneumatic/SOFTWARE_SERVICE/Documentation/2017/EN/DHWS_EN.PDF); [Festo HGPP](https://ftp.festo.com/public/pneumatic/SOFTWARE_SERVICE/Documentation/2017/EN/HGPP_EN.PDF); [Festo HGPT](https://ftp.festo.com/public/pneumatic/SOFTWARE_SERVICE/Documentation/2022/US/HGPT_ENUS.PDF)
- SMC cobot gripper unit JMHZ2-16D ships with M5 miniature fittings and Ø2 PU tubing. — [SMC JMHZ2 manual](https://www.smcworld.com/upfiles/manual/en-jp/files/MHx-OMY0007.pdf)
- SMC ZP/ZP3 vacuum pads: connection threads M3/M5 (female) and M5/M6 (male) for small pads, with Ø2–Ø6 tube one-touch inlets. — [SMC ZP3](https://www.smcpneumatics.com/pdfs/ZP3_Pads.pdf); [SMC ZP](https://content2.smcetech.com/pdf/ZP_Pad.pdf)
- Schmalz suction-cup connectors with M5 male/female thread, about 1.2–1.4 g. — [Schmalz SC 030 M5-AG](https://www.schmalz.com/en-us/products/automation-743270/vacuum-grippers-746238/vacuum-suction-cups-301609/flat-suction-cups-round-301610/10.01.06.02802)
- EISELE 863 (straight screw-in, M3, OD3): nickel-plated brass, NBR, -0.95 to 15 bar, compressed air and vacuum, NW 1.5 mm, 2 g. — [EISELE 863-4218](https://www.eisele-connectors.com/en/products/863-4218)
- EISELE 887 (elbow screw-in, swiveling, M3/M5): nickel-plated brass, NBR, -0.95 to 15 bar, -20 to 80 °C, compressed air and vacuum. — [EISELE 887-4218](https://www.eisele-connectors.com/en/products/887-4218)
- EISELE offers a separate ball-bearing **rotary connector**, up to 800 rpm, "for conveying compressed air from a rigid component to a rotating component". EISELE calls it "the first fully rotating connector in Eisele's product spectrum", which implies its swivel elbows are not rotating connectors. It comes only in G1/4 with OD8–12, so it is too large for a hand. — [EISELE Rotary connector flyer](https://pim.eisele.eu/Werbetr%C3%A4ger/Eisele_Flyer_Rotary_connector_en.pdf); [Eurotec 2017](https://eurotec-online.com/rotary-connector-for-rotating-components-eisele-offers-new-practical-connector-from-basicline-push-in-fitting?debut_articles=40)
- SMC KS/KX rotary one-touch fittings carry a ball-race bearing "for oscillating or rotating applications" and are "applicable to use for oscillating and rotating sections in robots". This is a separate product class from standard swivel elbows. — [SMC KS/KX](https://www.smcworld.com/webcatalog/en-id/seriesList/?id=KS-KX-E); [SMC KS](https://www.smcusa.com/products/ks-rotary-one-touch-fitting-inch~22022)
- Power & Motion: rotary unions are the fitting type for continuous rotation. Hoses should load swivels minimally, otherwise "seals can wear prematurely and leak". — [Power & Motion: Rotary Unions and Swivels](https://www.powermotiontech.com/hydraulics/hydraulic-fittings-couplings/article/21118782/united-equipment-accessories-rotary-unions-and-swivels)

### Inferences
- 863-4218 and 887-4218 at gripper ports, finger actuators or suction cups are consistent with industry practice. Both are vacuum-rated to -0.95 bar, which is confirmed.
- On a moving wrist: mount the 887 rigidly on the hand/gripper and let a slack tube loop (or a hollow-wrist routing) absorb the wrist motion. The user's spec says "NOT for continuous swivel motion", and the existence of separate rotary product lines at EISELE and SMC supports that restriction. It is safe to depict 887 as "angled outlet on the gripper body", but not as a "wrist rotation joint".

### Gaps
- I found no EISELE text that states verbatim "not for continuous swiveling" for the 887. That restriction comes from the user's spec sheet; the EISELE web page excerpt did not show it.
- **529-5018G**: the EISELE product page returns "Product was not found" for both 529-5018G and 529-5018. I could not confirm its media or vacuum rating. Most EISELE BASICLINE pneumatic fittings (863, 887, VT5528) are rated -0.95 bar, and BASICLINE as a family is stated for "compressed air, vacuum, gases and fluids" ([EISELE Basicline](https://www.eisele-connectors.com/en/product-overview/pneumatic-connectors)). That is only a family-level hint, and the datasheet must be checked. The "P12" union-nut style suggests a clamp/union-nut screw-in fitting (EISELE BASICLINE lists "screw-in fittings with union nuts that can be used for all pneumatic applications"), but this is unverified.

## Q4: Is 4 mm or 6/4 mm OD tubing realistic for joint cooling flow (0.2–0.6 l/min)?

### Takeaway
Yes, for a single actuator branch. The only humanoid joint-cooling paper found uses 0.6 L/min as an operating point. A rough calculation shows that a 4 mm OD tube (about 2.5–3 mm ID) carries 0.2–0.6 L/min at moderate to high velocity. 6/4 tubing gives a much lower pressure drop. Using 4 mm OD in the illustration is realistic for branches. A trunk serving several joints would more likely use 6/4 or larger.

### Cited Findings
- Humanoid joint liquid cooling ring evaluated at 0.6 L/min, h ≈ 1340 W/m²K. The study states its "flow rates and inlet temperature conditions correspond to feasible operating parameters for practical robotic cooling systems". — [ScienceDirect 2026](https://www.sciencedirect.com/science/article/pii/S0735193326017914)
- CPC liquid-cooling QDs start at 1/8" (3.2 mm) tubing ID for the smallest connectors (NS4, NS212 etc.). — [CPC Thermal Management Brochure](https://www.cpcworldwide.com/Portals/0/Downloadable-Content/TRM/Literature/Brochures/CPC-Thermal-Management-Brochure.pdf)
- Eaton advises accounting for pressure drop across connectors and checking fluid velocities to prevent erosion corrosion. — [Eaton](https://www.eaton.com/us/en-us/products/thermal-management-solutions/power-electronics-cooling/couplers-hose-clamps-and-fitting-selection.html)

### Inferences (my own calculations, water at about 20 °C, smooth tube)
- 4 mm OD, assumed 2.5 mm ID: 0.2 L/min gives v ≈ 0.7 m/s, Re ≈ 1700 (laminar), Δp ≈ 0.035 bar/m. 0.6 L/min gives v ≈ 2.0 m/s, Re ≈ 5100 (turbulent), Δp ≈ 0.3 bar/m. A few metres per branch is feasible with a small pump, but the upper end is velocity-heavy.
- 6/4 mm (4 mm ID) at 0.6 L/min: v ≈ 0.8 m/s, Δp ≈ 0.03–0.04 bar/m. This is more comfortable for longer runs (torso to leg).
- The fittings' nominal bores are NW 3 (VT5528-0202) and NW 2.5 (SA2113). They are similar to a 4 mm OD tube ID, so they are not a big extra restriction, but each coupling adds a local loss.
- Consistency check: SA2113 is rated 0–10 bar and VT5528 is rated up to 16 bar, both far above the expected loop pressure (inference). SA2113 has a 100 °C upper limit, which is fine for actuator coolant that is usually kept well below 85 °C (the paper targets <85 °C).

### Gaps
- I found no published humanoid design that states the tubing OD used for joint cooling.
- The tube ID is assumed. EISELE OD4 tubing ID was not checked.

## Q5: Risk statements: couplings at moving joints, fatigue, leakage near electronics

### Takeaway
Sources consistently warn about three things: side loads and hose weight on QDs cause seal deformation and leaks; repeated connect/disconnect fatigues seals; and every extra joint is a potential leak point. Best practice is to keep connections few, accessible and strain-relieved, put them away from or below sensitive electronics, and add leak detection.

### Cited Findings
- OCP ACS leak-detection white paper (US national lab example): QDs leaked over time from seal fatigue after many connect cycles, and from **side load from hanging coolant lines deforming the seals**. Supporting the lines fixed it. The IT equipment was spared because "the quick disconnect fittings are located outside of the IT systems". — [OCP ACS Cold Plate Leak Detection White Paper](https://www.opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1/)
- A Dell patent places a leak-detection enclosure around the cold-plate hose fittings because "even small amounts of moisture leaked… can lead to corrosion… and premature system failure". — [US12356586B2](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12356586)
- Saint-Gobain: hose routing imposes unanticipated bends and tension, so it calls for "adequate strain relief at both fitting ends and explicit bend radius requirements". It also notes that polymer fittings can creep. — [Saint-Gobain](https://www.ics.saint-gobain.com/resources/blog/inside-direct-chip-cooling-loop-components-coolant-chemistry-and-system-design-data)
- Machine-design routing guide: unsupported hose spans "fatigue at their end fittings"; "each elbow adds pressure drop and a potential leak point"; hoses must not be twisted; "use swivel fittings at one end of dynamic hose assemblies to allow installation without twist". — [sekkei-tech 2026](https://sekkei-tech.com/2026/08/03/piping-hose-routing-machine-design-fluid-systems-en)
- Eaton: repeated removal of fittings can cause leaks, so use couplings where disconnection is frequent. Compression fittings are "not recommended for applications with vibration, thermal cycling or other dynamic forces". — [Eaton](https://www.eaton.com/us/en-us/products/thermal-management-solutions/power-electronics-cooling/couplers-hose-clamps-and-fitting-selection.html)
- CPC: the closer a connection is to electronics, the greater the need for non-spill performance. — [CPC Tech Guide](https://www.cpcworldwide.com/Portals/0/Downloadable-Content/TRM/Literature/Tech-Guides/CPC-Location-and-QD-Specification-Tech-Guide.pdf)
- 2026 news: Tesla Optimus and Boston Dynamics Atlas reportedly "faced heat-shedding problems during sustained real-world operation". This comes from secondary tech press with no primary evidence, so it is low confidence. — [Gagadget 2026](https://gagadget.com/en/725815-unitree-g1-a-14000-humanoid-robot-with-cooler-motors-and-a-movable-head/)

### Inferences
- For the illustration:
  - SA2113 belongs at a static, strain-relieved module flange (shoulder/torso), ideally where a leak would not drip onto the chest electronics. Placing it below or beside the electronics is better than above it.
  - VT5528 belongs as fixed ports on the cold plate or actuator jacket.
  - The hose between the jacket and the next static point has to absorb the joint motion. Coupling sides should be fixed to structure on both halves.
  - In this application, M3/M5 push-in fittings at the hand carry only air or vacuum, so a leak there does not threaten electronics. It does matter for gripping function.

### Gaps
- I found no humanoid-specific failure data on coolant fittings at joints.
