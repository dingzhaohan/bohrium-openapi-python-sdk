import rich
from rich import print
from rich.table import Table

class Util(object):
    def __init__(self):
        pass

    def nice_print_table(
            self,
            headers: list = [],
            items: list = []
        ) -> None:

        table = Table()
        for header in headers:
            table.add_column(header, style="bold blue")
        
        for row in items:
            table.add_row(*[str(item) for item in row])

        print(table)

if __name__ == '__main__':
    headers = [
      "Job ID",
      "Group Name",
      "Job Status",
      "Group ID",
      "Job Groups",
      "Project",
      "Duration",
      "Creation Time",
      "Cost",
      "Submission type"
    ]

    items = [
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
      [5578019, "dpgen_train_job", "Finished", 10362171, "dpgen_train_job", "dingzhaohan", "00:06:13", "2023-01-19 01:11:11", "¥0.46", "Command line"],
    ]
    util = Util()
    util.nice_print_table(headers=headers, items=items)

    print("asdf")