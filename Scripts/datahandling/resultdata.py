import os
import pandas
try:
    from openpyxl import Workbook, load_workbook
    _use_txt = False
except ImportError:
    _use_txt = True


class ResultsData:
    """
    Saves all result data to same folder.
    """
    def __init__(self, results_directory_path):
        if not os.path.exists(results_directory_path):
            os.makedirs(results_directory_path)
        self.path = results_directory_path
        self._list_buffer = {}
        self._df_buffer = {}
        self._xlsx_buffer = {}

    def flush(self):
        """Save to files and empty buffers."""
        for filename in self._list_buffer:
            with open(os.path.join(self.path, "{}.txt".format(filename)), 'w') as f:
                for row in self._list_buffer[filename]:
                    f.write(row)
        self._list_buffer = {}
        for filename in self._df_buffer:
            self._df_buffer[filename].to_csv(
                os.path.join(self.path, filename),
                sep='\t', float_format="%1.5f")
        self._df_buffer = {}
        for filename in self._xlsx_buffer:
            self._xlsx_buffer[filename].save(
                os.path.join(self.path, "{}.xlsx".format(filename)))
        self._xlsx_buffer = {}

    def print_data(self, data, filename, colname):
        """Save data to DataFrame buffer (printed to text file when flushing).

        Parameters
        ----------
        data : pandas.Series
            Data to add as a new column to DataFrame
        filename : str
            Name of file where data is pushed (can contain other data)
        colname : str
            Desired name of this column
        """
        if filename not in self._df_buffer:
            self._df_buffer[filename] = pandas.DataFrame(data, columns=[colname])
        else:
            df = self._df_buffer[filename]
            self._df_buffer[filename] = df.reindex(
                df.index.union(data.index), copy=False)
            self._df_buffer[filename][colname] = data

    def print_matrix(self, data, filename, sheetname):
        """Save 2-d matrix data to buffer (printed to file when flushing).

        Saves matrix both in Excel format and as list in text file.

        Parameters
        ----------
        data : pandas DataFrame
            Data to add as a new sheet to WorkBook
        filename : str
            Name of file where data is pushed (without file extension)
        sheetname : str
            Desired name of excel sheet
        """
        if _use_txt:
            # If no Workbook module available (= _use_txt), save data to csv
            data.to_csv(
                os.path.join(self.path, "{}_{}.txt".format(filename, sheetname)),
                sep='\t', float_format="%8.1f")
        else:
            # Get/create new worksheet
            if filename in self._xlsx_buffer:
                ws = self._xlsx_buffer[filename].create_sheet(sheetname)
            else:
                self._xlsx_buffer[filename] = Workbook()
                ws = self._xlsx_buffer[filename].active
                ws.title = sheetname
            # Write data to each cell
            for j in xrange(0, data.shape[1]):
                ws.cell(row=1, column=j+2).value = data.columns[j]
            for i in xrange(0, data.shape[0]):
                ws.cell(row=i+2, column=1).value = data.index[i]
                for j in xrange(0, data.shape[1]):
                    ws.cell(row=i+2, column=j+2).value = data.iloc[i, j]
        # Create list file
        if filename not in self._list_buffer:
            self._list_buffer[filename] = []
        sheetname = sheetname.replace("_", "\t")
        for j in data.columns:
            for i in data.index:
                self._list_buffer[filename].append(
                    "{}\t{}\t{}\t{}\n".format(i, j, sheetname, str(data[j][i])))
