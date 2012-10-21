import os
import datetime


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


def make_tls_property(default=None):
	"""Creates a class-wide instance property with a thread-specific value."""
	class TLSProperty(object):
		def __init__(self):
			from threading import local
			self.local = local()

		def __get__(self, instance, cls):
			if not instance:
				return self
			return self.value

		def __set__(self, instance, value):
			self.value = value

		def _get_value(self):
			return getattr(self.local, 'value', default)

		def _set_value(self, value):
			self.local.value = value
		value = property(_get_value, _set_value)

	return TLSProperty()
