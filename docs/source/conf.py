import os, pkg_resources, sys, time
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../usb_protocol'))

import sphinx_rtd_theme

extensions = [
    'sphinx_rtd_theme'
]

# -- Project information -----------------------------------------------------

project = 'usb_protocol'
copyright = time.strftime('2021-%Y, Great Scott Gadgets')
author = 'Great Scott Gadgets'

version = pkg_resources.get_distribution('usb_protocol').version
release = ''


# -- General configuration ---------------------------------------------------

templates_path = ['_templates']
exclude_patterns = ['build']
source_suffix = '.rst'
master_doc = 'index'
language = 'en'
exclude_patterns = []
pygments_style = None

extensions = [
    'recommonmark',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinxcontrib.apidoc',
]

# configure extension: sphinxcontrib.apidoc
apidoc_module_dir = '../../usb_protocol'
apidoc_output_dir = 'api_docs'
apidoc_excluded_paths = ['test']
apidoc_separate_modules = True

# configure extension: extlinks
extlinks = {
    'repo':    ('https://github.com/greatscottgadgets/facedancer/blob/main/%s',          '%s'),
    'example': ('https://github.com/greatscottgadgets/facedancer/blob/main/examples/%s', '%s'),
}

# configure extension: napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_use_ivar = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_param = False


# -- Options for HTML output -------------------------------------------------
# run pip install sphinx_rtd_theme if you get sphinx_rtd_theme errors
html_theme = 'sphinx_rtd_theme'
html_css_files = ['status.css']
