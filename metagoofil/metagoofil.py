import sys, os
import argparse
import logging

import pkg_resources

from metagoofil import logger
from metagoofil.discovery.googlesearch import GoogleSearch
from metagoofil.downloader import Downloader
from metagoofil.extractor import Extractor

supported_extensions = ["pdf", "doc", "docx", "xls", "xlsx", "ppt" , "pptx", "odt", "ods", "odg", "odp"]


class Metagoofil:
    def __init__(
            self,
            file_types,
            working_directory=".",
            local_analysis=False,
            domain_name="",
            r_offset=0,
            r_limit=100,
            f_limit=100,
            inurl=False,
            wait=1,
            jitter=0,
            cookies="",
            force=False
    ):
        self.file_types = file_types
        self.working_directory = working_directory
        self.local_analysis = local_analysis
        self.domain_name = domain_name
        self.r_offset = r_offset
        self.r_limit = r_limit
        self.f_limit = f_limit
        self.inurl = inurl
        self.wait = wait
        self.jitter = jitter
        self.cookies = cookies
        self.force = force
        self.documents = []

        self.results = {}

    def setup_working_directory(self):
        if not os.path.exists(self.working_directory):
            try:
                os.mkdir(self.working_directory)
            except Exception as e:
                logging.debug(f"\"{self.working_directory}\" directory cannot be created", exc_info=True)
                return False
        logging.info(f"Working directory: {self.working_directory}")
        return True

    def get_documents(self):
        if self.local_analysis:
            return self.get_local_documents()
        else:
            return self.get_remote_documents()

    def get_local_documents(self):
        logging.success("Grabbing local documents")
        self.documents = [
            os.path.join(self.working_directory, f) for f in os.listdir(self.working_directory)
            if f.split(".")[-1] in self.file_types
        ]
        return True

    def get_remote_documents(self):
        logging.success("Fetching remote documents")
        for file_type in self.file_types:
            logging.success(f"Fetching {file_type} files...")
            if file_type not in supported_extensions:
                logging.warning(f"Filetype {file_type} is not supported")
                continue

            logging.debug(f"Searching for {self.r_limit} {file_type} files, starting at {self.r_offset}")
            google_search = GoogleSearch(
                self.domain_name,
                offset=self.r_offset,
                results_limit=self.r_limit,
                filetype=file_type,
                inurl=self.inurl,
                cookies=self.cookies
            )
            results = google_search.search()

            if len(results) == 0:
                logging.info("No file found.")
                continue
            
            logging.success(f"{len(results)} files found")

            if self.f_limit == 0:
                logging.success("No file should be downloaded. Skipping.")
                continue

            logging.debug(f"Starting to download {self.f_limit} files")
            counter = 0
            for result in results:
                if counter < self.f_limit:
                    logging.debug(f"[{counter + 1}/{self.f_limit}] " + result)
                    downloader = Downloader(result, self.working_directory, file_type)

                    file_path = downloader.download(wait=self.wait, jitter=self.jitter, force=self.force)
                    if not file_path or file_path == "":
                        logging.warning(f"Failed to download {result}")
                        continue

                    counter += 1
                    logging.success(f"[{counter}/{min(self.f_limit, len(results))}] {file_path} downloaded")
                    self.documents.append(file_path)
        return True

    def analyse_documents(self):
        logging.success(f"Analysing {len(self.documents)} documents")
        counter = 0
        for file_path in self.documents:
            logging.success(f"[{counter + 1}/{len(self.documents)}] {file_path}")

            extractor = Extractor(file_path).load()
            if extractor is None:
                logging.debug(f"Extractor for {file_path} does not exist")
                counter += 1
                continue

            try:
                extractor.get_metadata()
                for key, values in extractor.get_results().items():
                    if key in self.results:
                        for value in values:
                            if value not in self.results[key]:
                                self.results[key].append(value)
                    else:
                        self.results[key] = values
            except Exception as e:
                logging.warning(f"Error while parsing {file_path}", exc_info=True)
                counter += 1
                continue
            counter += 1
        return len(self.documents) == 0 or self.results

    def output_results(self):
        for key, values in self.results.items():
            if len(values) == 0 or all("" == v.strip() for v in values):
                continue
            print("")
            logging.success(logger.highlight(key.upper()))
            for value in list(set(values)):
                logging.success(value)


def run():
    """
    Command line function to call lsassy
    """
    version = pkg_resources.require("metagoofil")[0].version
    parser = argparse.ArgumentParser(
        prog="Metagoofil",
        description='Metagoofil v{} - Metadata harvester'.format(version)
    )

    parser.add_argument('-d', '--domain', action='store', help='Domain to search')
    parser.add_argument('-w', '--working-dir', action='store', default='.', help='Working directory')

    parser.add_argument('-t', '--types', action='store', default=",".join(supported_extensions),
                        help=f'Filetype to download ({",".join(supported_extensions)})')
    parser.add_argument('--inurl', action='store_true',
                        help='Set "inurl" filter instead of "site" filter on Google. Might find some false positives')
    parser.add_argument('-r', '--results-limit', type=int, action='store', default=100,
                        help='Limit of results to search (Default: 100)')
    parser.add_argument('-s', '--results-start', type=int, action='store', default=0,
                        help='Offset to look for results (Default: 0)')
    parser.add_argument('-l', '--local', action='store_true',
                        help='Local analysis of documents in working directory')
    parser.add_argument('-f', '--files-limit', type=int, action='store', default=5,
                        help='Limit of files to download (Default: 5)')
    parser.add_argument('--force', action='store_true', help='Force download even if files exists')
    parser.add_argument('--wait', action='store', type=int, default=1,
                        help='Time to wait between requests (Default: 1s)')
    parser.add_argument('--jitter', action='store', type=int, default=0,
                        help='Jitter to apply to wait between request (0 to 100, default: 0)')
    parser.add_argument('--cookies', action='store', default='', help='Custom cookies to use for requesting Google')
    parser.add_argument('-V', '--version', action='store', help='Version')
    parser.add_argument('-v', action='count', default=0, help='Verbosity level (-v or -vv)')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    logger.init()

    if args.v == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.v >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.ERROR)

    if args.domain is None and not args.local:
        logging.getLogger().setLevel(logging.INFO)
        logging.warning("You must choose between online (--domain) and offline (--local)")
        sys.exit(1)

    file_types = [t.strip() for t in args.types.split(',')]

    metagoofil = Metagoofil(
        file_types=file_types,
        working_directory=args.working_dir,
        local_analysis=args.local,
        domain_name=args.domain,
        r_offset=args.results_start,
        r_limit=args.results_limit,
        f_limit=args.files_limit,
        inurl=args.inurl,
        wait=args.wait,
        jitter=args.jitter,
        cookies=args.cookies,
        force=args.force
    )

    if not metagoofil.setup_working_directory():
        logging.error("An error occurred while creating working directory")
        return False

    if not metagoofil.get_documents():
        logging.error("An error occurred while getting documents")
        return False

    if not metagoofil.analyse_documents():
        logging.error("An error occurred while analysing documents")
        return False

    metagoofil.output_results()


if __name__ == "__main__":
    run()
