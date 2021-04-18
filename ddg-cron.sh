# /usr/bin/bash
while getopts g:f:o: flag
do
    case "${flag}" in
    	g) generate_script_path=${OPTARG};;
        f) ddg_tracker_fingerprint_threshold=${OPTARG};;
		o) ddg_tracker_output_file_path=${OPTARG};;
    esac
done
echo "--Starting script with params--";
echo "generate.py script path: $generate_script_path";
echo "ddg tracker fingerprint threshold: $ddg_tracker_fingerprint_threshold";
echo "ddg tracker output file path: $ddg_tracker_output_file_path";


FULLPATH="/tmp/ddg-tracker-radar";
echo "Writing tracker radar repo to: $FULLPATH";

# clone ddg tracker radar repo
git clone https://github.com/duckduckgo/tracker-radar.git $FULLPATH

# execute tracker script
DOMAINFILES="$FULLPATH/domains"
python3 $generate_script_path $DOMAINFILES --fingerprinting_threshold $ddg_tracker_fingerprint_threshold --output $ddg_tracker_output_file_path

# clean repo
rm -fr $FULLPATH