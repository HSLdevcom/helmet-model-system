# Running the model system

The main entry point is `helmet.py`.
Run `python helmet.py --help` to see parameter syntax.
If you run `python helmet.py` without parameters,
all parameters will be taken from `dev-config.json`,
which can be used to setup the model run in advance.

## Configuring the model run with `dev-config.json`

### `HELMET_VERSION`

The version number is logged in model runs.
This should not be changed unless model code is changed.

### `LOG_LEVEL`

Model runs are logged to the command prompt and to a log file.
You can choose the level of detail of logging:
`DEBUG`, `INFO`, `WARNING`, `CRITICAL`, `ERROR`

### `LOG_FORMAT`

The default is `TEXT`, but this can be changed to `JSON`.

### `SCENARIO_NAME`

Then, you need to set the name of your scenario.
If you are trying the test model, write `"test"`.

### `RESULTS_PATH`

You need to set the path to your results folder where you wish your
result tables and matrices are written to.
This data will be written over during the model run.

If you are trying the test model, try
`"C:\\FILL_YOUR_PATH\\helmet-model-system\\Scripts\\tests\\test_data\\Results"`.
If you are trying another model, fill in whatever the path is.

When running the `SCENARIO_NAME` scenario, its results are written in `RESULT_PATH\\SCENARIO_NAME`.
If you are using mock assignment instead or proper Emme assignment,
you need to initialize temporary result matrices to `RESULT_PATH\\SCENARIO_NAME\\Matrices`.

### `EMME_PROJECT_PATH`

If you are using Emme assignment, you need to specify where your `.emp` file is located.

### `FIRST_SCENARIO_ID`

EMME scenario ID of the network.

### `FIRST_MATRIX_ID`

First matrix ID within EMME project (.emp).
Used only if `SAVE_MATRICES_IN_EMME` is set to `true`.

### `BASELINE_DATA_PATH`

You need data and matrices for the initialization phase.
This data will not be written over at any point - it is read-only.
The location of this data is defined in `BASELINE_DATA_PATH` key.

If you are trying the test model, try
`"C:\\FILL_YOUR_PATH\\helmet-model-system\\Scripts\\tests\\test_data\\Base_input_data"`.
If you are trying another model, fill in whatever the path is.

There should be two directiories under the path: `2016_zonedata` and `base_matrices`.
The names of these directories are hardcoded.
There are 10 different input vector files in `2016_zonedata` from `.car` to `.wrk`.
`base_matrices` contains `.omx` and `.txt` files for costs, demand, external
traffic and freight traffic.

### `FORECAST_DATA_PATH`

Then, you need data for the forecast scenario.
This data will also not be written over at any point - it is read-only.
The location of this data is defined in `FORECAST_DATA_PATH` key.

If you are trying the test model, try
`"C:\\FILL_YOUR_PATH\\helmet-model-system\\Scripts\\tests\\test_data\\Scenario_input_data\\2030_test"`.
If you are trying another model, fill in whatever the path is.

There should be 9 or 10 different input vector files in your forefact data path.
File extensions are similar to your `BASELINE_DATA_PATH\\2016_zonedata` files.
The file `.car` is optional (?).

In the .ext file there must be a value line for every external zone in use
(i.e. centroids 31000…31999 In the network).
In all other files (excluding files .cco, .tco and .trk) there must be a value
line for every internal zone in use (i.e. centroids 1…30999 In the network).
It means that if there are no inhabitants, workplaces, parking costs etc. in
some zone a zero value line instead of a missing line must be used.

### `ITERATION_COUNT`

Maximum number of demand model iterations to run
(each using re-calculated impedance from traffic and transit assignment).

### `MAX_GAP`

Convergence criterion: Car work matrix maximum change between iterations.

### `REL_GAP`

Convergence criterion: Car work matrix relative change between iterations.

### `OPTIONAL_FLAGS`

These should not be used when running model system from command line!
Instead `helmet.py` flag parameters should be used.
These can be set if model system is run from UI, to set parameters that cannot be set in UI.
A flag is activated by putting its name inside the brackets,
flags are separated by commas (e.g., `"OPTIONAL_FLAGS": ["RUN_AGENT_SIMULATION", "DO_NOT_USE_EMME"]`).

#### `END_ASSIGNMENT_ONLY`

Using this flag runs only end assignment of base demand matrices.

#### `RUN_AGENT_SIMULATION`

Using this flag runs agent simulations instead of aggregate model.

#### `DO_NOT_USE_EMME`

Add this flag if you do not have the Emme license or wish to use the mock assignment.

#### `SEPARATE_EMME_SCENARIOS`

Using this flag creates four new EMME scenarios and saves
network time-period specific results in them.

#### `SAVE_MATRICES_IN_EMME`

If active, demand and skim matrices (including transit trip parts) for all time
periods will be saved to EMME project Database folder.

#### `DELETE_STRATEGY_FILES`

Transit assignment in EMME stores large files which are used for assignment analyses.
If activated, these files will be deleted after the model run.

#### `USE_FIXED_TRANSIT_COST`

If set, pre-calculated transit costs are taken from the Results folder.
