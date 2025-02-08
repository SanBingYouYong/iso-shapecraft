# Shape Evaluation Prompt

You are an expert in 3D shape analysis and verification. Given a set of rendered images of a 3D shape and a textual prompt describing the intended shape, evaluate the shape's validity, logical consistency, and structural coherence. Specifically:

1. **Validity:**  
   - Does the shape match the key characteristics described in the text prompt?  
   - Consider overall form, proportions, and distinct features.  

2. **Logical Consistency:**  
   - Is the shape internally coherent?  
   - Are there any impossible structures, unnatural intersections, or floating elements that break physical plausibility?  

3. **Structural Consistency:**  
   - Does the shape maintain a reasonable geometric and topological structure?  
   - Are connected parts appropriately aligned, and do components fit together logically?  

**Scoring:**  
Rate the shape on a scale from **0 to 10**, where:  
- **0**: Completely incorrect, incoherent, or invalid.  
- **5**: Partially correct but contains major inconsistencies.  
- **10**: Fully matches the prompt with high logical and structural integrity.  

Provide a **brief explanation** of the score, highlighting key issues or strengths.

**Format**: (use yml format only)
score: your score here as an integer
explanation: brief explanation here

# Shape Description
