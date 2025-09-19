import sys
import os
import argparse
import logging
import cv2
from src.detectors.face_detector import create_face_detector
from src.components.stream_processor import process_stream

# Ensure the project root directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def parse_args(argv=None):
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Camera-based face scanner demo')
    parser.add_argument('--source', '-s', default='0',
                        help='Video source: camera index (default 0) or path to video file')
    parser.add_argument('--quiet', '-q', action='store_true', help='Reduce logging output')
    return parser.parse_args(argv)

def main(argv=None):
    """Main entry point for the application."""
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO if not args.quiet else logging.WARNING,
                        format='[%(levelname)s] %(message)s')

    try:
        face_detector = create_face_detector()
    except Exception as e:
        logging.error('Face detector setup failed: %s', e)
        return 2

    try:
        cap = cv2.VideoCapture(int(args.source) if args.source.isdigit() else args.source)
        if not cap.isOpened():
            raise RuntimeError(f'Unable to open video source: {args.source}')
    except Exception as e:
        logging.error('Video source error: %s', e)
        return 3

    process_stream(cap, face_detector)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())