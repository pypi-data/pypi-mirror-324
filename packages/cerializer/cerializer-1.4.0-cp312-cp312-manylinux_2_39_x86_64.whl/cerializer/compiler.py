# pylint: disable=protected-access, deprecated-method, no-value-for-parameter
import distutils.core  # pylint: disable=deprecated-module
import hashlib
import importlib.machinery
import importlib.util
import os.path  # pylint: disable=no-name-in-module
import sys
from typing import Any, List, cast

import Cython.Build.Dependencies
import Cython.Build.Inline
import Cython.Compiler.Main
import Cython.Utils


def compile_code(code: str) -> Any:
	return _cython_inline(code)


def _load_dynamic(name: str, module_path: str) -> Any:
	loader = importlib.machinery.ExtensionFileLoader(name, module_path)
	spec = cast(importlib.machinery.ModuleSpec, importlib.util.spec_from_loader(name, loader))
	module = importlib.util.module_from_spec(spec)
	loader.exec_module(module)
	return module


def _cython_inline(
	complete_code: str,
	lib_dir: str = os.path.join(Cython.Utils.get_cython_cache_dir(), 'inline'),
) -> Any:
	key = complete_code, sys.version_info, sys.executable, 3, Cython.__version__
	module_name = '_cython_inline_' + hashlib.md5(str(key).encode('utf-8')).hexdigest()

	build_extension = Cython.Build.Inline._get_build_extension()
	module_path = os.path.join(lib_dir, module_name + build_extension.get_ext_filename(''))

	code = []
	for line in complete_code.split('\n'):
		code.append('    ' + line)

	if not os.path.exists(lib_dir):
		os.makedirs(lib_dir)
	cflags: List[str] = []
	c_include_dirs: List[str] = []
	pyx_file = os.path.join(lib_dir, module_name + '.pyx')
	fh = open(pyx_file, 'w', encoding = 'utf-8')
	try:
		fh.write(complete_code)
	finally:
		fh.close()
	extension = distutils.core.Extension(
		name = module_name,
		sources = [pyx_file],
		include_dirs = c_include_dirs,
		extra_compile_args = cflags,
	)
	if build_extension is None:
		build_extension = Cython.Build.Inline._get_build_extension()
	build_extension.extensions = Cython.Build.Dependencies.cythonize(
		[extension],
		include_path = ['.'],
		quiet = True,
	)
	build_extension.build_temp = os.path.dirname(pyx_file)
	build_extension.build_lib = lib_dir
	build_extension.run()

	module = _load_dynamic(module_name, module_path)

	return module.__invoke()
