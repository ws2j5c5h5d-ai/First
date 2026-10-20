# Coolant line routing in liquid-cooled humanoids and robot actuators (as of Oct 2026)

## Which real humanoids/robots use liquid cooling, and what is publicly known about their layout?

### Takeaway
Confirmed liquid-cooled actuators exist in: Honor "Lightning"/D1 (2026 half-marathon winner, leg drive motors), UT Austin/Apptronik DRACO (legs, 2017–2019), Apptronik's Sagittarius exoskeleton and earlier prototypes, Xiaomi CyberOne's 2026 hand, and research actuators (RoMeLa/UCLA, HKUST-GZ AMDT, Jin/Kobayashi/Doi). Hydraulic Atlas (retired 2024) is the closest well-documented analogue for "fluid lines in a humanoid", and Boston Dynamics put its fluid routing inside 3D-printed structure. For no commercial humanoid has the routing been published as a drawing, photo or teardown.

### Cited Findings
- **Honor Lightning / D1:** won the Beijing E-Town half-marathon on 19 Apr 2026 in 50:26 — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- Honor's official description: "liquid-cooling pipes penetrate deep into the motors like capillaries", the "high-power liquid pump" has a heat-exchange flow rate above 4 L/min, and "each of the four drive motors in the lower limbs is equipped with an independent liquid-cooling circuit" — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon); same wording in Chinese ("液冷管道如同毛细血管般深入电机内部…每分钟超4升") — [IT之家](https://www.ithome.com/0/940/862.htm), [科技日报](https://www.stdaily.com/web/gdxw/2026-04/23/content_506973.html)
- The pump is the Huake Lengxin (华科冷芯) HD01 magnetically levitated micro-pump: above 20,000 rpm, 6 L/min, 18 m head, about 30 mm in size, under 100 g, survives 500 g shock while running. The supplier says it went through five iterations for Honor — [36Kr](https://eu.36kr.com/en/p/3775418378027520), [NCSTI/千龙网](https://www.ncsti.gov.cn/kjdt/xwjj/202604/t20260420_244348.html), [雷峰网](https://www.leiphone.com/category/ai/8c0LRtFiKS4clo08.html)
- Supplier's description of a "typical robot liquid-cooling module": liquid-cooling ring (液冷环) on the joint motor, a micro-pump, a water-cooled radiator (水冷散热器) and connecting tubing. Heat goes from the ring into the fluid and then to the radiator. The pump must stay under about 50 mm and overcome "complex pipeline resistance" — [腾讯新闻/千机社](https://news.qq.com/rain/a/20260419A0453O00)
- Lightning: 169 cm tall, about 45 kg (humanoid.guide), 25 DoF, leg length about 90–95 cm, peak joint torque 400 N·m, hip/knee motors roughly 110–150 mm in diameter (estimated) — [humanoid.guide](https://humanoid.guide/product/honor-d1/), [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- Estimated heat dissipated in the knee motor while running at 7 m/s: about 150 W, which air convection cannot remove continuously — [IEEE Spectrum (Avik De)](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- Unitree uses air cooling, so liquid cooling is one of "two paths" in the industry — [36Kr](https://eu.36kr.com/en/p/3775418378027520)
- **Tiangong (Beijing Humanoid Robot Innovation Center), 2025 half-marathon winner:** used optimized air ducts ("最优散热风道…定向气流"), not liquid cooling — [iTherM](http://itherm.cn/index/news/news_show/article_id/130.html). HKUST-GZ AMDT Lab says related liquid-cooling technology was adopted by "numerous" 2026 marathon robots, including Lightning and Tiangong. That would make Tiangong's 2026 version liquid-cooled, but I found no confirmation — [AMDT Lab](https://amdt.hkust-gz.edu.cn/projects/Liquid_Cooling_Joint_Actuators)
- **DRACO (UT Austin HCRL + Apptronik):** liquid-cooled bipedal lower body with 10 DoF, using viscoelastic liquid-cooled actuators (VLCA) — [Apptronik](https://apptronik.com/company/our-work), [UT HCRL](https://sites.utexas.edu/hcrl/2019/06/), [Humanoids 2019 paper](https://openalex.org/works/W2948468563)
- On the VLCA test bed the pump, radiator and reservoir were Swiftech products (PC water cooling) weighing about 1 kg. Liquid cooling raised the continuous current limit 3.59×, giving 216 W/kg continuous and 650 W/kg short-term — [arXiv 1711.01649](https://arxiv.org/html/1711.01649v2)
- Apptronik: the Sagittarius exoskeleton's knees and ankles were liquid-cooled. The CEO said the liquid-cooled exoskeleton was "too complex… heavy" — [Apptronik](https://apptronik.com/our-work), [Apptronik/TechCrunch](https://apptronik.com/news-collection/apptronik-readies-its-humanoid-robot-for-a-summer-unveil). IEEE Spectrum: Apptronik tried liquid cooling on some prototypes but, as far as the author knows, not on Apollo — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- NASA Valkyrie: Apptronik/UT HCRL contributed liquid-cooled actuators to Valkyrie 2 — [Apptronik/TechCrunch](https://apptronik.com/news-collection/apptronik-readies-its-humanoid-robot-for-a-summer-unveil)
- **Xiaomi CyberOne (2026 redesign):** the hand has 3D-printed metal liquid-cooling channels inside it, described as working like sweat glands — [Interesting Engineering](https://interestingengineering.com/ai-robotics/xiaomi-cyberone-humanoid-robotic-hand)
- **Kengoro (Univ. Tokyo JSK, 2016):** the laser-sintered aluminium skeleton carries water and "sweats" it next to the motors. It has no radiator and no external tubes, and about one cup of deionized water lasts half a day — [IEEE Spectrum](https://spectrum.ieee.org/this-robot-can-do-more-pushups-because-it-sweats)
- **Hydraulic Atlas (BD, retired April 2024):** the legs combined "the structure, the manifold and the fluid routing and actuator cylinders all into one [3D-printed] structure". The HPU "sits in the center of the robot" (torso), wrapped around the reservoir. A printed manifold with 18 valves serves the upper body — [All3DP (Aaron Saunders keynote)](https://all3dp.com/boston-dynamics-vp-of-engineering-talks-about-3d-printing). A 2026 paper describes this as "embedding hydraulic channels into limb structures via AM, eliminating external tubing" — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0264127526009226)
- **RoMeLa (UCLA):** liquid-cooled proprioceptive actuator for legged robots, with a thermal model for "multiple liquid cooled actuators within a single cooling system" — [Semantic Scholar](https://www.semanticscholar.org/paper/Design%2C-Modeling%2C-and-Analysis-of-a-Liquid-Cooled-Zhu-Hooks/68b760f60ce01da2ea9a376d4eb255e6201cd1b8)
- **Tesla Optimus:** no public source found for liquid-cooled actuators. The rotary actuators use frameless torque motors and harmonic drives, the linear actuators use planetary roller screws (a secondary source) — [optimusk.blog](https://optimusk.blog/blog/tesla-optimus-hardware-specs/)

### Inferences
- In 2026, "liquid-cooled humanoid" realistically means mainly legs: hip and knee drive motors, sometimes ankles. Arms and upper body are usually air-cooled. Honor confirms liquid cooling only for "four drive motors in the lower limbs" (probably hip pitch and knee on each side; not confirmed).
- Hydraulic Atlas is not coolant cooling. It is still the best-documented example of a humanoid "fluid architecture": central unit in the torso, fluid paths inside the structure, no visible hoses.

### Gaps
- No photo, CAD or teardown of the Lightning cooling layout is public: pump position, radiator position and pipe routing are unknown.
- Xiaomi has not said where the hand's pump and radiator sit (forearm or torso?).
- Tesla, Figure, Unitree H2 and UBTech: no confirmed liquid cooling of actuators found.

## Where are the pump, radiator and manifold placed? Central loop or per-joint loops?

### Takeaway
The architecture shown publicly is central: one or a few pumps and a radiator in the torso/pelvis area feed several actuators, with Honor using a separate circuit per leg motor. Exact placement is documented only for hydraulic Atlas (HPU in the centre of the torso), the VLCA test bed (off-board PC components) and the Jin et al. leg (all cooled actuators above the knee).

### Cited Findings
- Honor: "independent liquid-cooling circuit" for each of 4 lower-limb drive motors, plus a "high-power liquid pump" (singular in the press text) with more than 4 L/min — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- Typical module: liquid-cooling ring + micro-pump + water-cooled radiator + tubing. The pump is built "in the robot interior" ("可轻松集成于机器人内部") — [雷峰网](https://www.leiphone.com/category/ai/8c0LRtFiKS4clo08.html)
- VLCA patent: "a single pump can provide fluid flow to multiple motors". Pump power was 12 W against 533 W motor power (2.2%) — [US20170341227A1](https://patents.google.com/patent/US20170341227A1/en)
- Jin/Kobayashi/Doi (Humanoids 2025): conventional designs put actuators at the ankle, which makes tube routing complex and risks leaks there. They propose putting **all actuators above the knee and cooling them collectively** ("concentrated" liquid cooling) to cut leak risk and part count. The design was tested in kicking and jumping — [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11203109/), [J-STAGE](https://www.jstage.jst.go.jp/article/jsmermd/2025/0/2025_2A2-A04/_article/-char/en)
- Hydraulic Atlas: HPU "sits in the center of the robot", with sensing, filtration and valves integrated around the reservoir. A separate upper-body manifold has 18 valves — [All3DP](https://all3dp.com/boston-dynamics-vp-of-engineering-talks-about-3d-printing)
- Supplier 空调国际 (June 2026) proposes a "主动集中液冷" (active centralized liquid cooling) system for 1 kW total: 120×120 mm parallel-flow radiator, 38 mm-thick e-fan, micro electric water pump. The joint cooling channels are integrated into the motor housing ("plug-and-play" joint modules). Servo joints produce 60–80% of total robot heat, and heat can jump from 500 W to 1–2 kW within seconds — [syaq.org/盖世汽车](http://www.syaq.org/guancha/98158.html)
- Xi'an Jiaotong (Device 2025): microfluidic chip cooling on a humanoid used a commercial water-cooling radiator with built-in pump as "heart" and "skin", connected to flexible cold modules at several joints — [Cell Device](https://www.cell.com/device/fulltext/S2666-9986(24)00498-8), [PDF](https://cell.com/device/pdf/S2666-9986%2824%2900498-8.pdf)
- Hydraulic patent (2026, humanoid hand): shows two variants, a hose bundle running **outside** the torso and arm, and hoses routed **inside** the arm, with pump and pressure/exhaust manifolds possibly integrated in the arm — [US12752419B2](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12752419)

### Inferences
- A realistic illustration would have a compact pump (about 30 mm, under 100 g) and a radiator with fan in the torso, pelvis or back-pack area, a distribution manifold in the pelvis, and paired supply/return lines down each thigh to the hip and knee motors.
- Honor's "independent circuit per motor" probably means parallel branches from a manifold, or several pumps. Which one is not public.
- The radiator needs airflow, so it is plausibly behind a vented back or chest panel. Not confirmed for any robot.

### Gaps
- No public source gives the radiator size or position in Lightning.
- Whether Honor uses one pump or several is ambiguous: press texts say "a pump", but there are four independent circuits.

## How do lines cross rotating joints?

### Takeaway
Nothing public describes rotary unions or hollow-shaft coolant passages in any liquid-cooled humanoid. Known approaches are flexible tubing loops (DRACO-era PC-cooling PVC tube), avoiding joint crossings by moving actuators toward the body (Jin et al.), and channels built into the structure (Atlas, Kengoro, Xiaomi hand). Industrial robots show the conventions: hoses through a hollow wrist, or an external dress pack with a service loop.

### Cited Findings
- Jin et al.: tube routing complexity and leak risk are the "unignorable drawbacks" of liquid cooling, especially at the ankle. Their answer is not to cross the knee or ankle with coolant at all (all actuators above the knee) — [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11203109/)
- VLCA/DRACO: "high-flex PVC tubing" connected the commercial radiator, reservoir, pump and fittings — [US20170341227A1](https://patents.google.com/patent/US20170341227A1/en)
- Industrial practice: a water-cooled welding torch's cooling-water hose either spans the upper arm externally (which interferes with the workspace) or runs **through the hollow wrist** — [US7326880B2](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7326880). Hollow wrists carry a protection hose holding cables, air and hydraulic lines, and need room for the hose to bend — [US20060243087A1](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20060243087)
- General guidance: for limited-angle joints, a "properly sized service loop" is cheaper than a slip ring or rotary union. The loop must be checked at worst-case joint combinations. Fluid rotary unions exist but are separate from slip rings — [Robotics Engineering Lab](https://roboticsengineeringlab.com/articles/cable-management-robot)
- Hose rules: never bend below the minimum bend radius (measured to the hose centreline), install with zero twist (use swivel fittings), and size hoses generously for moving interfaces — [sekkei-tech](https://sekkei-tech.com/2026/08/03/piping-hose-routing-machine-design-fluid-systems-en)
- Hydraulic wheel-legged robot WLR-3P: a "hoseless" design with a 3D-printed hoseless hydraulic joint (HHJ) at hip and waist, and pipelines printed into the thigh — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10250005)
- Xi'an Jiaotong: flexible manifolds with gradient stiffness at the joints absorb joint torque and displacement — [Cell Device](https://www.cell.com/device/fulltext/S2666-9986(24)00498-8)

### Inferences
- Humanoid hip and knee joints rotate less than 180°, so a short loop of flexible tube (C or S shape) on the inside or back of the joint is the most plausible solution. A rotary union adds weight and leak points. This is an inference, not documented for a specific humanoid.
- Rule-of-thumb minimum bend radius for small soft PVC/PU/silicone tubes is about 3–5× OD (generic engineering practice; no robot-specific source found).

### Gaps
- No published example of a coolant rotary union or hollow-shaft coolant passage in a humanoid joint.
- No bend radius or slack figures specific to humanoids.

## How do lines attach at the actuator: jacket, ring or cold plate?

### Takeaway
The dominant pattern is a cooling jacket or ring around the stator: a cylindrical housing with circumferential channels concentric with the motor. Inlet and outlet fittings sit side by side on one face or flange (DRACO: on the front plate next to the output shaft). Cold plates are used for drives and electronics.

### Cited Findings
- VLCA patent: the motor sits in a **liquid-cooling jacket with several fluid channels encircling the motor**. A removable front section carries the output shaft and the fluid interface, with **inlet and outlet fittings next to each other**, sealed with O-rings and held by screws. The 3D-printed jacket is rated for 1.5 bar pump pressure. A separate water block with a single machined channel cools the servo drive's heat sink — [US20170341227A1](https://patents.google.com/patent/US20170341227A1/en)
- HKUST-GZ-type liquid cooling ring (LCR, Oct 2026): axially layered, circumferentially closed annular channels, concentric with the actuator. The ring is 120 mm inner diameter, 126 mm outer, 3 mm thick. A partitioned inlet–outlet manifold splits flow into parallel annular channels. At a 250 W peak load (115 W/cm²) the motor stays below 85 °C, against about 380 °C without cooling. h ≈ 1340 W/m²K at 0.6 L/min — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0735193326017914)
- Honor: pipes run "deep into the motors like capillaries" (marketing wording; the geometry is not disclosed) — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- Industry: channels integrated into the motor housing make "plug-and-play" integrated joint modules. Micro-channel cold plates increase heat-exchange area 3–5× — [syaq.org](http://www.syaq.org/guancha/98158.html)
- Thin-film option: 0.2 mm liquid-cooling films with a 0.5 mm piezo micro-pump (汉得利 Bestar), aimed at dexterous hands where gaps are under 2 mm. Still unproven in joints — [eefocus](https://www.eefocus.com/article/2082378.html)

### Inferences
- For an illustration: a metal ring or sleeve around the motor stator inside the joint housing, with two small barbed or push-in fittings (supply and return) leaving the housing side by side, radially or axially, usually on the side facing the body/limb tube so the lines run along the link.

### Gaps
- Fitting type (barb, push-in, quick-disconnect) and orientation on Honor's or any commercial humanoid's joints are not documented.

## Typical line sizes, flow rates, coolant and heat loads

### Takeaway
Documented flow rates run from about 0.6 L/min per ring to more than 4–6 L/min for the whole system. Heat loads are about 150–250 W per hot leg joint, and 0.5–2 kW for the whole robot. Tube diameters for humanoids are not published anywhere I found.

### Cited Findings
- Honor system: more than 4 L/min. Pump capacity: 6 L/min at 18 m head — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon), [雷峰网](https://www.leiphone.com/category/ai/8c0LRtFiKS4clo08.html)
- VLCA test bed: 0.036 L/s (= 2.16 L/min) through the motor jacket, drive water block and radiator in series. The 100 W motor reached 283 W continuous with liquid cooling — [US20170341227A1](https://patents.google.com/patent/US20170341227A1/en)
- LCR study: 0.6 L/min is a "feasible" per-joint flow, with a 250 W peak heat load — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0735193326017914)
- Knee motor dissipation when running: about 150 W — [IEEE Spectrum](https://spectrum.ieee.org/china-humanoid-robot-marathon)
- Whole-robot heat swings from 500 W to 1–2 kW; joint-module power above 2 kW — [syaq.org](http://www.syaq.org/guancha/98158.html), [雷峰网](https://www.leiphone.com/category/ai/8c0LRtFiKS4clo08.html)
- Coolant: deionized water in Kengoro — [IEEE Spectrum](https://spectrum.ieee.org/this-robot-can-do-more-pushups-because-it-sweats). The VLCA used PC water-cooling components — [arXiv](https://arxiv.org/html/1711.01649v2)
- Tube material: high-flex PVC (VLCA) — [US20170341227A1](https://patents.google.com/patent/US20170341227A1/en)

### Inferences
- PC-cooling tubing (as used on DRACO) is typically about 6–13 mm OD. For 1–2 L/min branches, about 4–8 mm OD tubing is plausible. This is an inference from standard PC and automotive practice, not a humanoid source.
- Coolant is most likely water/glycol or deionized water with inhibitor. Not confirmed for Honor.

### Gaps
- No published line OD/ID, fitting size or coolant formulation for Honor, Xiaomi or any commercial humanoid.

## Are lines inside the limb shell or outside?

### Takeaway
Every documented commercial or near-commercial example keeps fluid lines inside the shell or inside the structure (Atlas's printed legs, Kengoro's frame, Xiaomi's printed hand channels; Honor shows no visible external lines in race imagery). Exposed tubing appears mainly on lab prototypes and test beds.

### Cited Findings
- Atlas: fluid routing integrated into the printed leg structure — [All3DP](https://all3dp.com/boston-dynamics-vp-of-engineering-talks-about-3d-printing). AM-embedded channels "eliminating external tubing" — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0264127526009226)
- Kengoro: coolant inside the skeleton frame — [IEEE Spectrum](https://spectrum.ieee.org/this-robot-can-do-more-pushups-because-it-sweats)
- Xiaomi: liquid-cooling channels inside the hand — [Interesting Engineering](https://interestingengineering.com/ai-robotics/xiaomi-cyberone-humanoid-robotic-hand)
- Honor Lightning press: "internal liquid-cooling system" — [Mashable](https://mashable.com/article/chinese-robot-half-marathon-winner); the pump supplier stresses that small size helps "整机堆叠集成，有助于外观美观" (stacked integration inside the robot, which helps appearance) — [雷峰网](https://www.leiphone.com/category/ai/8c0LRtFiKS4clo08.html)
- A patent shows both external hose bundles and internal routing as valid options for a humanoid arm — [US12752419B2](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12752419)
- Internal routing protects lines and keeps the envelope clean, but is harder to service and needs rounded entries and grommets — [Robotics Engineering Lab](https://roboticsengineeringlab.com/articles/cable-management-robot)

### Inferences
- A "realistic" marketing image could show lines inside the limb shell along the back of the thigh, with short visible flexible loops only at the hip and knee, or show a cutaway of the shell. Fully exposed, hose-laden limbs would look like a lab prototype (DRACO/VLCA style).

### Gaps
- I did not verify from photos whether Honor's lines are visible anywhere on the exterior; I found no close-up imagery or teardown.
