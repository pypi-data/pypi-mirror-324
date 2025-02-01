import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from task_6.src.f1_report_by_viacent.cli import main
from task_6.src.f1_report_by_viacent.functions import (
    parse_logs, calculate_lap_times, build_report,
    format_time, print_report,print_driver_report)


@pytest.fixture
def mock_log_files(tmp_path):
    abbreviations_content = """VET_Sebastian Vettel_Ferrari
HAM_Lewis Hamilton_Mercedes"""
    start_log_content = """VET2018-05-24_12:02:02.222
HAM2018-05-24_12:03:03.333"""
    end_log_content = """VET2018-05-24_12:04:04.444
HAM2018-05-24_12:06:06.666"""
    abbreviations_file = tmp_path / "abbreviations.txt"
    start_file = tmp_path / "start.log"
    end_file = tmp_path / "end.log"
    abbreviations_file.write_text(abbreviations_content)
    start_file.write_text(start_log_content)
    end_file.write_text(end_log_content)
    return str(tmp_path)


def test_parse_logs(mock_log_files):
    data = parse_logs(mock_log_files)
    assert data["abbreviations"]["VET"] == ["Sebastian Vettel","Ferrari"]
    assert data["abbreviations"]["HAM"] == ["Lewis Hamilton", "Mercedes"]
    assert isinstance(data["start_times"]["VET"], datetime)
    assert isinstance(data["end_times"]["HAM"], datetime)

def test_calculate_lap_times(mock_log_files):
    data = parse_logs(mock_log_files)
    lap_times = calculate_lap_times(data)
    assert len(lap_times) == 2
    assert lap_times[0]["abbreviation"] == "VET"
    assert lap_times[1]["abbreviation"] == "HAM"
    assert lap_times[0]["lap_time"] == timedelta(minutes=2, seconds=2, microseconds=222000)
    assert lap_times[1]["lap_time"] == timedelta(minutes=3, seconds=3, microseconds=333000)


def test_build_report(mock_log_files):
    report = build_report(mock_log_files)
    assert len(report["top_15"]) == 2
    assert len(report["rest"]) == 0


def test_format_time():
    assert format_time(timedelta(minutes=1, seconds=30, microseconds=500000)) == "1:30.500"
    assert format_time(timedelta(minutes=3, seconds=23)) == "3:23.000"
    assert format_time(timedelta(minutes=5)) == "5:00.000"


def test_print_report(mock_log_files, capsys):
    report = build_report(mock_log_files)
    print_report(report)
    captured = capsys.readouterr()
    assert "Top 15 Racers" in captured.out
    assert "Sebastian Vettel" in captured.out
    assert "Lewis Hamilton" in captured.out


def test_print_driver_report(mock_log_files, capsys):
    print_driver_report(mock_log_files, "Sebastian Vettel")
    captured = capsys.readouterr()
    assert "Driver: Sebastian Vettel" in captured.out
    assert "Team: Ferrari" in captured.out
    assert "Lap Time: 2:02.222" in captured.out


def test_missing_files_arg(capfd):
    with patch("sys.argv", ["cli.py", "--asc"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
    captured = capfd.readouterr()
    assert "the following arguments are required: --files" in captured.err
    assert excinfo.value.code != 0


def test_invalid_order_arg(mock_log_files, capfd):
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--asc", "--desc"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
    captured = capfd.readouterr()
    assert "Dont use both --asc & --desc" in captured.err
    assert excinfo.value.code != 0


def test_valid_asc_order(mock_log_files, capfd):
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--asc"]):
        main()
    captured = capfd.readouterr()
    assert "Top 15 Racers:" in captured.out
    assert captured.err == ""


def test_valid_desc_order(mock_log_files, capfd):
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--desc"]):
        main()
    captured = capfd.readouterr()
    assert "Top 15 Racers:" in captured.out
    assert captured.err == ""


def test_valid_driver_report(mock_log_files, capfd):
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--driver", "Sebastian Vettel"]):
        main()
    captured = capfd.readouterr()
    assert "Driver: Sebastian Vettel" in captured.out
    assert "Team: Ferrari" in captured.out
    assert captured.err == ""


def test_invalid_driver_report(mock_log_files, capfd):
    with patch("sys.argv", ["cli.py", "--files", mock_log_files, "--driver", "unknown driver"]):
        main()
    captured = capfd.readouterr()
    assert "No data found for driver" in captured.out
    assert captured.err == ""

if __name__ == "__main__":
    main()
