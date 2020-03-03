import os
import pandas
try:
    from openpyxl import Workbook, load_workbook
    _use_txt = False
except ImportError:
    _use_txt = True


class ResultsData:
    def __init__(self, results_directory_path):
        if not os.path.exists(results_directory_path):
            os.makedirs(results_directory_path)
        self.path = results_directory_path
        self._buffer = {}

    def flush(self):
        # TODO write output in flush, refactor buffer logic
        self._buffer = {}

    def print_data(self, data, filename, zone_numbers, colname):
        """Get/Create buf[filename] dataframe (with index=zone_numbers) -> set df[colname] to data -> save df to csv"""
        filepath = os.path.join(self.path, filename)
        if filename not in self._buffer:
            self._buffer[filename] = pandas.DataFrame(index=zone_numbers)
        self._buffer[filename][colname] = data
        # TODO MON: doesn't this write partial csv's repeatedly (to same file?) until last [colname]?
        self._buffer[filename].to_csv(filepath, sep='\t', float_format="%1.5f")

    def print_matrix(self, data, filename, sheetname):
        # If no Workbook module available (= _use_txt), save df (in arg data) to csv
        if _use_txt:
            data.to_csv(os.path.join(self.path, "{}_{}.txt".format(filename, sheetname)), sep='\t', float_format="%8.1f")

        # Else init Workbook -> write data to a new sheet of it -> save the workbook in .xlsx
        # TODO MON: same as print data, doesn't this do same rewrite for every worksheet?
        else:
            # Get/Create new worksheet
            if filename in self._buffer:
                ws = self._buffer[filename].create_sheet(sheetname)
            else:
                self._buffer[filename] = Workbook()
                ws = self._buffer[filename].active
                ws.title = sheetname

            # Write data to each cell
            for j in xrange(0, data.shape[1]):
                ws.cell(row=1, column=j+2).value = data.columns[j]
            for i in xrange(0, data.shape[0]):
                ws.cell(row=i+2, column=1).value = data.index[i]
                for j in xrange(0, data.shape[1]):
                    ws.cell(row=i+2, column=j+2).value = data.iloc[i, j]

            # Save the workbook
            self._buffer[filename].save(os.path.join(self.path, "{}.xlsx".format(filename)))

        # Create list file
        listfilepath = os.path.join(self.path, "{}.txt".format(filename))
        filename = "{}_list".format(filename)
        if filename not in self._buffer:
            self._buffer[filename] = []
        sheetname = sheetname.replace("_", "\t")
        for j in data.columns:
            for i in data.index:
                val = "{}\t{}\t{}\t{}\n".format(i, j, sheetname, str(data[j][i]))
                self._buffer[filename].append(val)
        with open(listfilepath, 'w') as f:
            for row in self._buffer[filename]:
                f.write(row)
