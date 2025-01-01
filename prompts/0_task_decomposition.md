# Task Breakdown Instruction

**Objective:** Given a user prompt on a 3D model generation task, decompose the overall shape into sub-components and describe each sub-component's shape individually. It should: 
1. Represent a distinct component or structural element of the 3D model.
2. Include clear instructions for the synthesis of the component.
3. Be mutually exclusive and collectively exhaustive in covering the user prompt.

**Output Format:** 
components:
  - name: [component name]
    description: [shape description]
  - name: [component name]
    description: [shape description]
  - ...

# User Prompt
