import os
import pandas
try:
    from openpyxl import Workbook, load_workbook
    _use_txt = False
except ImportError:
    _use_txt = True

_path = ".."
_buffer = {}

# TODO: mapping where all this module is used and how. (to know how to refactor it)

# helmet.py -> set_path

# generation.py -> print_data( ... tours.txt ...)
# emme_assignment -> print_data ( ... X_kms.txt ... )
# purpose.py -> print_data & print_matrix
# trips.py -> print_matrix
# logit.py -> print_data

# test_models.py -> set_path
# test_logit.py -> set_path


def set_path(scenario):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.join(script_dir, "..", "..")
    data_dir = os.path.join(project_dir, "Results", scenario)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    global _path 
    _path = data_dir


def flush():
    # TODO write output in flush, refactor buffer logic
    global _buffer
    _buffer = {}


def print_data(data, filename, zone_numbers, colname):
    """Get/Create buffer[filename] dataframe (with index=zone_numbers) -> set df[colname] to data -> save df to csv"""
    # TODO MON: doesn't this write partial csv's repeatedly (to same file?) until last [colname]?
    filepath = os.path.join(_path, filename)
    if filename not in _buffer:
        _buffer[filename] = pandas.DataFrame(index=zone_numbers)
    _buffer[filename][colname] = data
    _buffer[filename].to_csv(filepath, sep='\t', float_format="%1.5f")


def print_matrix(data, filename, sheetname):
    # If no Workbook module available (= _use_txt), save df (in arg data) to csv
    if _use_txt:
        data.to_csv(os.path.join(_path, "{}_{}.txt".format(filename, sheetname)), sep='\t', float_format="%8.1f")

    # Else init Workbook -> write data to a new sheet of it -> save the workbook in .xlsx
    # TODO MON: same as print data, doesn't this do same rewrite for every worksheet?
    else:
        # Get/Create new worksheet
        if filename in _buffer:
            ws = _buffer[filename].create_sheet(sheetname)
        else:
            _buffer[filename] = Workbook()
            ws = _buffer[filename].active
            ws.title = sheetname

        # Write data to each cell
        for j in xrange(0, data.shape[1]):
            ws.cell(row=1, column=j+2).value = data.columns[j]
        for i in xrange(0, data.shape[0]):
            ws.cell(row=i+2, column=1).value = data.index[i]
            for j in xrange(0, data.shape[1]):
                ws.cell(row=i+2, column=j+2).value = data.iloc[i, j]

        # Save the workbook
        _buffer[filename].save(os.path.join(_path, "{}.xlsx".format(filename)))

    # Create list file
    listfilepath = os.path.join(_path, "{}.txt".format(filename))
    filename = "{}_list".format(filename)
    if filename not in _buffer:
        _buffer[filename] = []
    sheetname = sheetname.replace("_", "\t")
    for j in data.columns:
        for i in data.index:
            val = "{}\t{}\t{}\t{}\n".format(i, j, sheetname, str(data[j][i]))
            _buffer[filename].append(val)
    with open(listfilepath, 'w') as f:
        for row in _buffer[filename]:
            f.write(row)
