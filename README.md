# ProgramSynthesisPipeline
Repository for software artifacts concerning my Master's Thesis

The repository contains:

- The folder Code, which contains all python Scripts of the implemented prototype.
- This file also contains the modified KeY-Version which was used for the evaluation.
- The folder ExampleProblemDefinition, which contains structured exampls of SyGuS in case somebody wants to get a first impression of SyGuS
- The folder SyGuS-IF-Examples, which contains intermediate studies that took place to check different concepts before actually implementing them.
- The folder SyGuS_IF_Examples containing two versions of the SyGuS-IF standard since this was frequently unavailable online
- The folder diagrams containing the diagrams and the .drawio file for the submitted thesis
- The folder evalData_noPredicats which contains the evaluation case studies used in the thesis. Self-defined predicates from the CorC studies have been replaced since this replacing was not yet supported in KeY
- The folder pictures containing the pictures for the submitted thesis
- The files plan.txt and predicate_replacements.txt which were used to track my progress but are not important for the evaluation.

To reproduce results:
- clone
- setup virtual environment and use virtualEnvironmentRequirements.txt for the setup
- make sure that the file sygusEvaluation.py links to the correct folder of the case studies (see line 10)
- in the same file make sure that the desired case studies are not commented out
- run sygusEvaluation.py from concole or IDE

