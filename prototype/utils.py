import os
import datetime

def list_dir_if_changed(dir, dir_last_modified, ext_filter=None):
	file_list = []
	
	# Set last modified time to directory last modified time
	last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(dir))
	
	for path in os.listdir(dir):
		file_path = os.path.join(dir, path)
		# Filter out directories and apply extension filter
		if os.path.isfile(file_path) and (not ext_filter or file_path.split(".")[1] in ext_filter):
			file_list.append(path)
			file_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
			if file_last_modified > last_modified:
				last_modified = file_last_modified
	
	if not dir_last_modified or last_modified > dir_last_modified:
		return (file_list, last_modified)
	
	return None