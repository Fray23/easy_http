import sys
from parser import HttpJsonParser
from fetcher import RequestSession, HttpFetcher, RequestObj
from vars import DefaultHeaderDecorator, BodyVarsDecorator, UrlVarsDecorator


def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <project_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    project_path = sys.argv[2]

    parser = HttpJsonParser(
        path_to_request_file=file_path,
        path_to_project_dir=project_path
    )
    parser = DefaultHeaderDecorator(parser)
    parser = BodyVarsDecorator(parser)
    parser = UrlVarsDecorator(parser)

    session = RequestSession(
        session_path=project_path,
        session_file_name='pysession'
    )

    http_fetcher = HttpFetcher(
        session=session
    )

    http_fetcher.send_with_save_session(
        RequestObj(
            body=parser.get_body_as_dict(),
            method=parser.get_method(),
            url=parser.get_url(),
            headers=parser.get_headers_as_dict()
        )
    )

if __name__ == '__main__':
    main()
