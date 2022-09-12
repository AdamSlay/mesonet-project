from src import rank
from pandas import read_csv
import pytest
import pathlib


@pytest.fixture
def read_csv_inputs():
    test_parm = "tair"
    parent_dir = pathlib.Path(__file__).parent
    file = parent_dir / "data" / "nrmn_20210904.csv"
    test_csv_filepath = file
    test_df = read_csv(file, usecols=["time", test_parm])
    test_sorted_df_desc = test_df.sort_values(test_parm, ascending=False)
    test_sorted_df_asc = test_df.sort_values(test_parm, ascending=True)
    return [
        test_csv_filepath,
        test_parm,
        test_sorted_df_desc,
        test_sorted_df_asc,
    ]


def test_read_csv_file(read_csv_inputs):
    # read_csv_file(csv_file_path, parm, ascending=False)
    result = rank.read_csv_file(read_csv_inputs[0], read_csv_inputs[1], False)
    assert result.equals(read_csv_inputs[2])


def test_read_csv_file_asc(read_csv_inputs):
    # read_csv_file(csv_file_path, parm, ascending=True)
    result = rank.read_csv_file(read_csv_inputs[0], read_csv_inputs[1], True)
    assert result.equals(read_csv_inputs[3])


def test_format_time():
    # format_time(sorted_df, csv_file)
    parent_dir = pathlib.Path(__file__).parent
    file = parent_dir / "data" / "format_time"
    input_df_desc = read_csv(f"{file}/format_time_input.csv")
    input_csv_file = "nrmn_20210904.csv"
    expected_df = read_csv(f"{file}/format_time_result.csv")

    result = rank.format_time(input_df_desc, input_csv_file)
    assert result.equals(expected_df)


def test_format_time_asc():
    # format_time(sorted_df, csv_file)
    parent_dir = pathlib.Path(__file__).parent
    file = parent_dir / "data" / "format_time"
    input_df_asc = read_csv(f"{file}/format_time_input_asc.csv")
    input_csv_file = "nrmn_20210904.csv"
    expected_df = read_csv(f"{file}/format_time_result_asc.csv")

    result = rank.format_time(input_df_asc, input_csv_file)
    assert result.equals(expected_df)
