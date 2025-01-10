# Visual Feedback Instruction

**Objective:** Given a rendered image of a 3D shape, analyze it against the target shape description and provide feedback on:
1. Specific discrepancies or areas for improvement.
2. Suggestions for refining the corresponding code snippet.
3. Consistency between the visual output and the sub-task intent.

**Output Format:** 
issues: 
  - description: [issue description]
    suggestion: [suggestion to correct or improve]
  - ...
consistenct: [true/false based on the significance of identified issues]

# Shape Description
