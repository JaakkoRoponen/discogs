"""
Excel to Pandas to Excel
"""

import sys

import pandas as pd


class Pexel():
    """Pandas excel conversions"""

    def __init__(self, filename):
        self.filename = filename
        self.df = self._get_sheets(self.filename)

    def _get_sheets(self, filename):
        """Get excel sheets as dataframe"""
        try:
            sheets_dict = pd.read_excel(filename, sheet_name=None)
        except FileNotFoundError:
            sys.exit(f"File '{filename}' not found")
        except PermissionError:
            sys.exit(f"Permission denied: '{filename}'. Is the file open?")
        except OSError as err:
            sys.exit(f"System error: {err}")

        df = pd.DataFrame()
        for sheet_name, sheet in sheets_dict.items():
            sheet['sheet_name'] = sheet_name
            df = df.append(sheet, sort=False)

        df.set_index('sheet_name', append=True, inplace=True)
        return df

    def add_data_to_row(self, index, data):
        """Add data dict to row defined by index"""
        df = self.df
        data = pd.Series(data)

        while True:
            try:
                df.loc[index, data.index] = data  # data.index == "columns"
            except KeyError:  # column not in df
                for col_name in data.index:
                    if col_name not in df.columns:
                        df[col_name] = pd.np.nan
            else:
                break

    def save(self):
        """Save dataframe to excel sheets"""
        df = self.df

        writer = pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            self.filename,
            engine='xlsxwriter')

        for sheet in df.index.get_level_values('sheet_name').unique():
            df.xs(sheet, level='sheet_name') \
                .to_excel(writer, sheet_name=sheet, index=False)

        writer.save()
