# Visual Feedback Instruction

**Objective:** Given a rendered image of a 3D shape, analyze it against the target shape description and provide feedback on:
1. Specific discrepancies or areas for improvement.
2. Suggestions for refining the corresponding code snippet.
3. Consistency between the visual output and the sub-task intent.

Note that the images contain only raw mesh from Blender viewport, so do not comment textures, lighting or any other aspects that are hardly achievable in a raw mesh rendering. Consider it consistent as long as the shape matches the intention. 

**Output Format:** (uses yml format only)
issues: 
  - description: [issue description]
    suggestion: [suggestion to correct or improve]
  - ...
consistency: [true/false based on the significance of identified issues]

# Shape Description
