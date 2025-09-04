# Text2Scenario: Text-Driven Scenario Generation for Autonomous Driving

## Installation Steps

### Step 1: Create and Activate Conda Environment
```bash
conda create -n t2s python=3.8
conda activate t2s
```

### Step 2: Clone the Repository
```bash
git clone git@github.com:caixxuan/Text2Scenario.GitHub.io.git
```

### Step 3: Install Dependencies
```bash
cd SafeBench
pip install -r requirements.txt
pip install -e .
```

### Step 4: Download and Extract CARLA_0.9.13

### Step 5: Add CARLA Python API to PYTHONPATH
Add the following lines to your `~/.bashrc`:
```bash
export CARLA_ROOT={path/to/your/carla}
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.13-py3.8-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/agents
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI
```

## Usage

> Note: The current demo has been updated, and the formal version is pending release. Some content differs from Text2Scenario and will be continuously optimized.

### Step 1: Convert JSON File Format
- Use `converter.py` to convert JSON file formats.

### Step 2: Build Knowledge Base (Recommended: Use RAG to check LLM API feasibility)
- Run `RAG_embbeding.py`.
- Users can customize their own LLM API.

### Step 3: Prompt Engineering Reference Case
- Run `RAG_query.py`.
- The case is simplified compared to T2S; users can optimize as needed.

### Step 4: Convert Scenario Representation to .xosc File
- Use `scenario_generator.py`.
- The code is for demonstration; full functionality will be supplemented later.

### Step 5: Execute Generated .xosc File in CARLA
- Use scenario runner to execute the OpenSCENARIO script.
- Reference: [Scenario Runner Documentation](https://scenario-runner.readthedocs.io/en/latest/)

### Step 6: Check Acknowledgement to Build carla-X Joint Simulation Framework

## Acknowledgement
- DORA: https://github.com/dora-rs
- Apollo: https://github.com/guardstrikelab/carla_apollo_bridge
- Autoware: https://github.com/autowarefoundation/autoware
- Interfuser: https://github.com/opendilab/InterFuser (0.9.10 is needed)