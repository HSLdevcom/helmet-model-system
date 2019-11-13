import numpy
import os
import pandas
try:
    from openpyxl import Workbook, load_workbook
    _use_txt = False
except ImportError:
    _use_txt = True

_path = ".."
_buffer = {}

def set_path(scenario):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.join(script_dir, "..", "..")
    data_dir = os.path.join(project_dir, "Results", scenario)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    global _path 
    _path = data_dir

def print_data(data, filename, zone_numbers, colname):
    filepath = os.path.join(_path, filename)
    if filename not in _buffer:
        _buffer[filename] = pandas.DataFrame(index=zone_numbers)
    _buffer[filename][colname] = data
    _buffer[filename].to_csv(filepath, sep='\t', float_format="%1.5f")

def print_matrix(data, filename, sheetname):
    if _use_txt:
        txtfilepath = os.path.join(_path, filename + '_' + sheetname + ".txt")
        data.to_csv(txtfilepath, sep='\t', float_format="%8.1f")
    else:
        xlsxfilepath = os.path.join(_path, filename + ".xlsx")
        if filename in _buffer:
            ws = _buffer[filename].create_sheet(sheetname)
        else:
            _buffer[filename] = Workbook()
            ws = _buffer[filename].active
            ws.title = sheetname
        for j in xrange(0, data.shape[1]):
            ws.cell(row=1, column=j+2).value = data.columns[j]
        for i in xrange(0, data.shape[0]):
            ws.cell(row=i+2, column=1).value = data.index[i]
            for j in xrange(0, data.shape[1]):
                ws.cell(row=i+2, column=j+2).value = data.iloc[i, j]
        _buffer[filename].save(xlsxfilepath)
    listfilepath = os.path.join(_path, filename + ".txt")
    filename = filename  + "_list"
    if filename not in _buffer:
        _buffer[filename] = []
    rowtext = "{}\t{}\t{}\t{}\n"
    sheetname = sheetname.replace("_", "\t")
    for j in data.columns:
        for i in data.index:
            val = rowtext.format(i, j, sheetname, str(data[j][i]))
            _buffer[filename].append(val)
    with open(listfilepath, 'w') as f:
        for row in _buffer[filename]:
            f.write(row)
