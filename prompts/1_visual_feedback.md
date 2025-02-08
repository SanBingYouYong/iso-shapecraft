# Visual Feedback Instruction

**Objective:** Given a rendered image of a 3D shape, analyze it against the target shape description and provide feedback on:
1. Specific discrepancies or areas for improvement.
2. Focus on geometric properties.
3. Ignore rendering artifacts.

**Output Format:** (uses yml format only)
issues: 
  - description: [issue description]
    suggestion: [suggestion to correct or improve]
  - ...
consistency: [true/false based on the significance of identified issues]

# Shape Description
