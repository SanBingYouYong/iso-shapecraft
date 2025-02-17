# ISO: ShapeCraft

## Overview

In recent years, large pre-trained models, especially LLMs, have shown impressive capabilities across diverse applications, including code generation, image synthesis, and even aspects of 3D model generation. However, attempts to harness LLMs for synthesizing shape programs and generating 3D models reveal both promise and critical limitations. Current efforts to employ LLMs for generating shape programs in text or code format provide an exciting bridge between natural language understanding and 3D vision, but the generated outputs often fall short in structural complexity, spatial awareness, and fidelity to real-world designs. Likewise, direct text-to-3D generation, while impactful in creative applications, struggles with achieving the precise, reusable, and scalable attributes necessary for high-quality 3D modeling.

Inspired by SceneCraft [2] on utilizing LLM to construct 3D scenes using Blender code by retrieving existing 3D models and placing them into places following inferred constraints, this proposal aims to explore the possibility of using similar pipelines in generating 3D shape as shape programs. By studying how LLMs can be better aligned to understand and reproduce the logic inherent in 3D shape programs, and by addressing the challenges in text-to-3D synthesis, this research seeks to enhance both the accuracy and utility of LLM-driven 3D modeling tools. Improvements in this area could lead to breakthroughs in fields ranging from automated design and CAD to virtual reality and game development, making 3D content creation more accessible and efficient.

## Related Work

Recent advancements in text-guided 3D modeling have explored the potential of large language models (LLMs) in generating structured, high-quality 3D content. Several notable approaches leverage LLMs to synthesize complex 3D objects and scenes while addressing inherent limitations, such as parametric control, procedural generation, and scene composition.

Recent advancements in text-to-3D synthesis leverage text-to-image diffusion models to generate high-quality 3D content despite the absence of large 3D datasets. DreamFusion [4] optimizes Neural Radiance Fields [3] using a 2D diffusion model as a prior, requiring no 3D training data. Fantasia3D [1] improves upon existing methods with a disentangled framework, using hybrid scene representations and BRDF modeling for photorealistic, editable 3D assets. ProlificDreamer [5] addresses limitations like over-smoothing in Score Distillation Sampling by introducing Variational Score Distillation, enhancing sample quality and diversity with optimized parameters. Together, these approaches highlight innovative uses of pretrained models for efficient and detailed 3D synthesis.

Building on these advancements in text-to-3D synthesis, there is potential to extend these techniques using large language models for generating discrete geometry directly. While current methods primarily focus on optimizing continuous representations like NeRFs, LLMs can enable the synthesis of structured, interpretable geometry in the form of shape programs. By leveraging LLMs' proficiency in code and structured data generation, we can aim for a more controllable and semantically rich 3D modeling process, facilitating applications in design automation and scene composition. This transition opens new avenues for integrating text-based and programmatic 3D synthesis within a cohesive framework.

Specifically, SceneCraft [2] presents an LLM-based system for translating natural language descriptions into executable Blender scripts that can composite 3D scenes from existing 3D models. SceneCraft achieves this by creating a scene graph that maps spatial relationships among assets, translating them into Python scripts with numerical layout constraints. It incorporates vision-language models to iteratively refine the scenes based on rendered outputs. SceneCraft also includes a library learning mechanism that accumulates reusable functions for improved efficiency, outperforming similar agents in adhering to spatial constraints and producing complex scenes. This approach showcases the potential of LLMs for highly structured 3D understanding and synthesis, and it will serve as the major inspiration for the proposed pipeline. In particular, components like task decomposition, library learning, and visual feedback would be valuable to adapt to the 3D shape program synthesis context.

## Method

This study proposes a multi-agent pipeline for improving large language models (LLMs) in the synthesis of 3D models and shape programs by leveraging task decomposition, shape component synthesis, structured aggregation, visual feedback loop, and function library. The approach is designed to overcome the challenges of generating complex 3D shapes and programs by breaking down the tasks, generating parts individually, and progressively aggregating them into a final coherent program. For figures, access the following link: (onedrive temporarily cannot share an uploaded pdf) (for access to fully structured proposal pdf, a link will be shared soon).

## Discussions

Inspired also by SceneCraft [2], as well as the game development process in the game industry, the proposed pipeline can also be used to construct a RAG-like 3D scene aggregation method based on existing directory of fine-grained 3D models: given a high-level scene description, the pipeline can break down the scene into individual objects, find matching 3D models by embedding-based search or text descriptions, and then aggregate the objects into a coherent 3D scene. This approach could be particularly useful in game development, virtual reality, and architectural design, where rapid prototyping and scene composition are essential.

## ISO Planning

As per required by the Independent Study Option module, the project needs to be split into a literature review phase and an experimental phase.

### Literature Review

The literature review phase aims to systematically evaluate existing research on Large Language Models (LLMs) for 3D model and scene synthesis, focusing on methods that decompose complex synthesis tasks. Special attention will be given to multi-agent frameworks, parametric control, procedural generation, and scene composition, assessing how these approaches address challenges in achieving coherent, high-quality 3D synthesis. Previous papers mentioned in the Related Work section constitute a starting point of study and detailed discussions will be provided, with additional research mentioned above to be included.

### Experimental Phase

The experimental phase will involve implementing a multi-agent pipeline for LLM-driven 3D model and shape program synthesis, building on insights from the literature review. The pipeline will consist of modules for task decomposition, component synthesis, and structured aggregation, leveraging LLMs to generate code snippets and combine them into coherent shape programs. The pipeline will be tested on a variety of 3D modeling tasks, evaluating its effectiveness in generating complex 3D shapes and programs. The results will be analyzed to assess the pipeline's performance, identify areas for improvement, and suggest future research directions.

## References

1. Rui Chen, Yongwei Chen, Ningxin Jiao, and Kui Jia. Fantasia3d: Disentangling geometry and appearance for high-quality text-to-3d content creation, 2023.
2. Ziniu Hu, Ahmet Iscen, Aashi Jain, Thomas Kipf, Yisong Yue, David A. Ross, Cordelia Schmid, and Alireza Fathi. Scenecraft: An llm agent for synthesizing 3d scene as blender code, 2024.
3. Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view synthesis, 2020.
4. Ben Poole, Ajay Jain, Jonathan T. Barron, and Ben Mildenhall. Dreamfusion: Text-to-3d using 2d diffusion, 2022.
5. Zhengyi Wang, Cheng Lu, Yikai Wang, Fan Bao, Chongxuan Li, Hang Su, and Jun Zhu. Prolificdreamer: High-fidelity and diverse text-to-3d generation with variational score distillation, 2023.
