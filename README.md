# Python Rigging Tools
Various python rigging tools created by Kira Smith. Each tool is free to use and edit however you'd like. <br>
List last updated: 1.5.24

## Unreal Converstion Tool
Created to solve a compatability issue while working on Death Bloom with UTD. We had switched from animating the rigs in Maya to animating them in Unreal halfway through production and ran into an issue. Instead of re-creating all of my rigs, I created this tool that would convert the existing rigs into a format that was accepted by Unreal. The program also copies skin weights. <br>
Tool last updated: 2.10.23
- Converts existing weighted rigs into an Unreal-friendly rig while preserving weights.
- Made using PyCharm for Maya

## Auto Jaw Tool
Started as an exercise in python and turned into my passion project. I used online resources to complete it, but I wrote every line of code and added functionality to the product. It has pre-built joint realtionships, with many user-accessable values that make the jaw rig very versitile for any character mouth.<br>
Tool last updated: 4.13.23
- Creates a set of guides that can postioned by the user, which can then be turned into joints with pre-made connections and constraints.
- Made in Python
- [Click here to watch the tool in action.](https://www.youtube.com/watch?v=J-I3eLb5h4c)

## Auto Limb Tool
Created to speed up rigging time while ensuring quality. <br>
Tool last updated: 5.15.23
- Allows the user to select a given joint chain and a chain type. Based on the chain type, the tool will create an arm, leg or animal leg each with diffrent attributes and their own pole vector.
- Includes squash and strech features.
- Made in Python
