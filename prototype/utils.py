import os
import datetime
from zipfile import ZipFile
from contextlib import closing
from cStringIO import StringIO


def list_dir_if_changed(dir, dir_last_modified, ext_filter=None):
	if not os.path.isdir(dir):
		return None

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

	file_list.sort()

	if not dir_last_modified or last_modified > dir_last_modified:
		return (file_list, last_modified)

	return None


def zipdir(base_dir):
	assert os.path.isdir(base_dir)

	buffer = StringIO()

	with closing(ZipFile(buffer, "w")) as z:
		for base, dirs, files in os.walk(base_dir):
			for file_name in files:
				abs_path = os.path.join(base, file_name)
				rel_path = abs_path[len(base_dir) + len(os.sep):]
				z.write(abs_path, rel_path)

	buffer.flush()

	return buffer.getvalue()
