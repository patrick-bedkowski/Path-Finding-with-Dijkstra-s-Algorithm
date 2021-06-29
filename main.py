from graph import GenerateGraph
from file_management import read_from_txt, MalformedPlaneError
import argparse
import sys


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args(arguments[1:])

    path = args.path

    try:
        table, start_x, start_y, finish_x, finish_y = read_from_txt(path)

        graph = GenerateGraph(table)

        # set start and finish points' coordinates
        graph.set_start(start_x, start_y)
        graph.set_finish(finish_x, finish_y)

        # display unmodified plane
        graph.print_plane()

        graph.dijkstra()  # build dijkstra table

        print(' ')
        # display dijkstra path plane
        graph.print_plane_after_dijkstra()

    except MalformedPlaneError as e:
        print(e)
        print(f'File {path} contains invalid data')
        sys.exit()


if __name__ == "__main__":
    main(sys.argv)
