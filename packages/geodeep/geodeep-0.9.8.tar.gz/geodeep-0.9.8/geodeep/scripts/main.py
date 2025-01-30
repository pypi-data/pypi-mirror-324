import argparse
import sys
try:
    from geodeep import detect, models, simple_progress, __version__
except ImportError:
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from geodeep import detect, models, simple_progress, __version__

def main():
    parser = argparse.ArgumentParser(prog="geodeep", description="AI object detection in geospatial rasters ")
    parser.add_argument(
        "geotiff", 
        type=str, 
        nargs="?",
        help="Path to GeoTIFF"
    )
    parser.add_argument(
        "model", 
        type=str, 
        nargs="?",
        help="Model type or path to onnx model"
    )

    parser.add_argument(
        "--output-type", "-t",
        type=str, 
        default="geojson",
        choices=["geojson", "bsc", "raw"], 
        required=False, 
        help='Type of output. One of: %(choices)s. Default: %(default)s'
    )
    parser.add_argument(
        "--geojson-output", "-o", 
        type=str, 
        default="boxes.geojson",
        required=False, 
        help='GeoJSON output filename. Default: %(default)s'
    )
    parser.add_argument(
        "--list-models", "-l",
        action="store_true",
        required=False,
        help="Print list of available models and exit"
    )
    parser.add_argument(
        "--conf-threshold", "-c",
        type=float,
        default=None,
        required=False,
        help="Confidence threshold [0-1]. Default: model default"
    )    
    parser.add_argument(
        "--resolution", "-r",
        type=float,
        default=None,
        required=False,
        help="Model resolution target (cm/px). Default: model default"
    )  
    parser.add_argument(
        "--classes",
        type=str,
        default=None,
        required=False,
        help="Only detect certain classes (comma separated, e.g. car,plane). Default: detect all"
    )  
    parser.add_argument(
        "--max-threads",
        type=int,
        default=None,
        required=False,
        help="Maximum number of threads to use. Default: %(default)s"
    )   
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        required=False,
        help="Don't print progress"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        required=False,
        help="Print version and exit"
    )
    args = parser.parse_args()

    if args.list_models:
        print(models.list_models())
        exit(0)
    
    if args.version:
        print(__version__)
        exit(0)
    
    if not args.model or not args.geotiff:
        parser.print_help(sys.stderr)
        exit(1)
    
    output = detect(args.geotiff, args.model, 
                output_type=args.output_type, 
                conf_threshold=args.conf_threshold,
                resolution=args.resolution,
                classes=args.classes,
                max_threads=args.max_threads,
                progress_callback=simple_progress if not args.quiet else None)
    
    if args.output_type == "geojson":
        with open(args.geojson_output, "w") as f:
            f.write(output)
        print("")
        print(f"Wrote {args.geojson_output}")
    else:
        print(output)

if __name__ == "__main__":
    main()
