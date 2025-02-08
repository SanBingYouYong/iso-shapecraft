# Task Breakdown Instruction

**Objective:** Given a user prompt on a 3D model generation task, decompose the overall shape into sub-components and describe each sub-component's shape individually. It should: 
1. Represent a distinct component or structural element of the 3D model.
2. Include concise instructions that breaks down the sub-component into basic shapes.
3. Mention no other component in each component's description to avoid interference. 

**Output Format:** 
components:
  - name: [component name]
    description: [shape description]
  - name: [component name]
    description: [shape description]
  - ...

# User Prompt
