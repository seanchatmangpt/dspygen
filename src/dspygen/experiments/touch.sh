#!/bin/bash

# Define the base directory for the POC
baseDir="tagee"

# Create the directory structure
mkdir -p "$baseDir"/{docs,src/{core,ui/modules,ui/data,ui/utils},tests/{unit,integration},assets/{images,sounds},lib,scripts,config}

# Create documentation files
touch "$baseDir"/docs/{GettingStarted.md,CurriculumAlignment.md,TechnicalOverview.md}

# Create source files
# Core engine files
touch "$baseDir"/src/core/{game_engine.py,narrative_engine.py,education_module.py}

# UI component files
touch "$baseDir"/src/ui/modules/{story_view.py,quiz_view.py,chatbot_view.py}
touch "$baseDir"/src/ui/data/{story_data.py,quiz_data.py,chatbot_data.py}
touch "$baseDir"/src/ui/utils/{ui_helpers.py,formatting_tools.py}

# Test files
touch "$baseDir"/tests/unit/{game_engine_test.py,narrative_engine_test.py,education_module_test.py}
touch "$baseDir"/tests/integration/{story_integration_test.py,quiz_integration_test.py,chatbot_integration_test.py}

# Asset placeholders
touch "$baseDir"/assets/images/.keep
touch "$baseDir"/assets/sounds/.keep

# Library placeholder
touch "$baseDir"/lib/.keep

# Script files
touch "$baseDir"/scripts/{setup.sh,deploy.sh,maintenance.sh}

# Configuration files
touch "$baseDir"/config/{dev.json,prod.json,test.json}

# Root files
touch "$baseDir"/{README.md,LICENSE,.gitignore}

echo "TAG-EE POC directory and file structure created."
