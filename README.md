# UniversalBuildPlatform

This project is about creating a simple intelocking build platform for hardware projects.
It uses trapezoidal connectors. The design is self-mating, meaning that you print the same part twice and they fit together w/o modification.
(the design has a 0.1mm gap between the trapezoidal elements).


# Universal Mounting System Generator (Fusion 360 Add-In)

A parametric Autodesk Fusion script to rapidly generate modular, multi-node mounting tracks with fully customizable physical dimensions.

---

![Geometry](./image%20(1).png?raw=true)

![Example - robo car](./IMG_5319.jpeg?raw=true)

![Example](./image.png?raw=true)




## 🚀 What It Creates

* **Custom Contour Profile:** Recreates a 14 mm × 5 mm interlocking trapezoidal cell geometry featuring top wings and angled guide slots.
* **Linear Array ($n$ Nodes):** Seamlessly tiles the cell geometry $n$ times horizontally along the X-axis to form a single contiguous profile.
* **Parametric Extension:** Adds a solid, customizable rectangular base extending downwards by a specified `Height` (> 0 mm) to reinforce the strip.
* **3D Extrusion:** Extrudes the entire unified profile along the Z-axis by a specified `Width` (> 0 mm) into a solid 3D body.

---

## ⚡ Why a Modular Mounting System is Brilliant

* **Zero Hardware Lock-In:** You aren't beholden to proprietary, overpriced brackets or flimsy single-use mounts. If your setup changes, you just adapt the grid or swap a node.
* **Infinite Scalability:** Need to mount three items today and thirty tomorrow? The parametric architecture means you just change $n$, click go, and print or mill the exact size you need without redesigning from scratch.
* **Flawless Mechanical Interlock:** Geometric trapezoidal tracks distribute load evenly and snap into place with satisfying procedural precision—no loose parts, no sloppy friction fits.
* **First-Principles Efficiency:** You get maximum structural rigidity using minimal raw material, custom-tailored to the exact physical envelope of your specific rig or workbench.


## Oh, did I mention it fits with gridfinity (3x14mm=42mm, gridfinity standard cell width)?


## 🛠️ Parameters

| Parameter | Type | Range / Constraints | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Number of Nodes ($n$)** | Slider | `1` to `100` | `3` | Number of repeating trapezoidal cells along the X-axis |
| **Width** | Value | `> 0 mm` | `10 mm` | Extrusion depth of the body along the Z-axis |
| **Height** | Value | `> 0 mm` | `1 mm` | Downward base extension height below $Y = 0$ |

---

## 📂 Installation & Usage

1. Open **Autodesk Fusion**.
2. Press `Shift + S` (or go to **UTILITIES** > **Scripts and Add-Ins**).
3. Under **My Scripts**, click **+ (Create)**, choose **Python**, name it `UniversalMountingSystem`, and click **Create**.
4. Select the script, click **Edit**, and replace the contents of the Python file with the script code.
5. Click **Run** in Fusion, enter your desired parameters, and hit **OK**.

Script: https://github.com/chrisherman/UniversalBuildPlatform/blob/main/UniversalBuildPlatform.py

Or use the ready-meal examples and extrude to you liking:
https://www.printables.com/model/1897122-universal-build-platform

