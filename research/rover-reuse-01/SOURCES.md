# ROVER-REUSE-01 — First-pass external sources (Sol, 2026-10-25)

**Provenance:** Public web sources inspected by Sol on October 25, 2026. This list is a starting bibliography, **not** model-specific validation, direct laboratory reproduction, a farm safety assessment or permission to copy third-party designs.

## High-value prior art

1. **Camara, Waltham, Churchill & Fox (2023), _OpenPodcar: An Open Source Vehicle for Self-Driving Car Research_**, Journal of Open Hardware 7(1). DOI [10.5334/joh.46](https://doi.org/10.5334/joh.46). [Journal landing page](https://ojs.lib.uwo.ca/index.php/openhardware/article/view/17859). Describes a scooter-donor platform with CAD/BOM/build instructions and Arduino, ROS/Gazebo control. Reports approximately **US$7,000 total when built from new components in 2022**. This figure is not a current used scooter price and does not establish farm suitability.

2. **Soni, Waltham, Ibrahim, Crampton & Fox (2026), _OpenPodcar2: a robust, ROS2 vehicle for self-driving research_**, research preprint arXiv:2604.24242. [Abstract](https://www.alphaxiv.org/abs/2604.24242) / [arXiv](https://arxiv.org/abs/2604.24242). Describes revised electronics, ROS2/Nav2/Gazebo integration, and reports around **US$7,000 from new parts or US$2,000 using a used donor** in that team's prototype. This is a **reported build budget**, not a quote for our chassis or proof of outdoor capability. Confirm paper and source availability independently before reuse.

3. **_Enabling Autonomous Navigation for Affordable Scooters_** (2018). [Open-access paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC6022038/). Reports an off-the-shelf mobility scooter with added control for speed/direction and automated steering, targeting an approximately $2,000 system including its $700 donor at the time. Useful for assessing actuator/steering burden; historical costs cannot be treated as current procurement data.

4. **Cornell Tech Interaction Lab, Mobile Hoverboard Robot Base**, [project page](https://irl.tech.cornell.edu/mobile_hoverboard_robot_base/). Demonstrates a low-cost differential-drive mobile robotics research base using reused hoverboard motors and an ODrive controller. **Not a powered wheelchair or farm-qualified rover**; useful contrasting architecture for differential control and teleoperation.

## Safety standards as research signposts

- [ISO 18497-1:2024](https://www.iso.org/standard/82684.html) — Design principles/vocabulary for partially automated, semi-autonomous and autonomous agricultural machines.
- [ISO 18497-2:2024](https://www.iso.org/standard/82686.html) — Design principles for obstacle protective systems.
- [ISO 18497-3:2024](https://www.iso.org/standard/82687.html) — Autonomous operating zones.
- [ISO 18497-4:2024](https://www.iso.org/standard/82688.html) — Verification methods and validation principles.

**Scope warning:** These are relevant research pointers, not a statement of certification or applicability of any specific vehicle. Full normative texts and legal requirements were **not obtained or assessed**. ISO 18497-1 expressly excludes public-road operations and systems put into use before its publication, among other scope boundaries. Never describe compliance or safety assurance as established.

## Investigation gaps to fill

- **Manufacturer manuals:** actual donor model's steer geometry, reverse/brake behavior, pack voltage/chemistry, grade and ground-clearance rating. **UNKNOWN.**
- **Real local donor market:** dated authentic offer with defects and accessories explicitly captured. No listings independently captured in this initial source note. **UNKNOWN.**
- **Farm terrain:** measured path widths, slope, ruts, softness, wet conditions, crop clearance and biodiversity-sensitive areas. **NOT MEASURED.**
- **Battery health and electronics:** any real donor's service history, insulation or controller compatibility. **NOT INSPECTED.**
- **Suitability decision:** `NEEDS_MORE_EVIDENCE`. No hardware procurement or field test authorized.

This source inventory will grow through separately attributed contributions; do not paste one agent's conclusions into another agent's supposedly independent first-pass note.
