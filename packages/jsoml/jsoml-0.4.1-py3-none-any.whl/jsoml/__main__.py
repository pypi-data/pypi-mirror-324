import jsoml

# std lib
import argparse, json, sys
from pathlib import Path
from typing import Optional


class Main:
    inpath: Path
    inform: Optional[str]

    def __init__(self, cmd_line_args: Optional[list[str]] = None):
        self.parser = argparse.ArgumentParser(description="JSOML tool")
        self.parser.add_argument("inpath", type=Path, help="input file path")
        self.parser.add_argument(
            "--from",
            dest="inform",
            choices=["json", "xml", "jsoml"],
            help="format of source",
        )
        self.parser.parse_args(cmd_line_args, self)

    def run(self) -> int:
        sout = sys.stdout
        if self.inform == "json" or self.inpath.suffix == ".json":
            with open(self.inpath) as sin:
                data = json.load(sin)
            jsoml.dump(data, sout)
            sout.write("\n")
        elif self.inform in ("xml", "jsoml") or self.inpath.suffix == ".xml":
            data = jsoml.load(self.inpath)
            json.dump(
                data,
                sout,
                indent=4,
                default=str,
                ensure_ascii=False,
                sort_keys=True,
            )
            sout.write("\n")
        else:
            return 1
        return 0


def main(args: Optional[list[str]] = None) -> int:
    return Main(args).run()


if __name__ == "__main__":
    exit(main())
