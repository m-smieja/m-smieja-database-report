# Configuration file for the Sphinx documentation builder.

import os
import sys

# -- Project information -----------------------------------------------------

project = 'Database Report'
copyright = '2024, Milosz Smieja'
author = 'Milosz Smieja'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.git', '*/.git']

language = 'pl'

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for PDF output --------------------------------------------------

pdf_documents = [
    ('index', 'database_report', 'Database Report', 'Milosz Smieja'),
]

pdf_stylesheets = ['sphinx']
pdf_language = "pl_PL"
pdf_fit_mode = "shrink"
pdf_break_level = 1
pdf_inline_footnotes = True
pdf_use_index = True
pdf_use_modindex = True
pdf_use_coverpage = True

# Dodatkowe ścieżki dla submodułów
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('2.chapter'))

latex_engine = 'pdflatex'  # lub 'xelatex' lub 'lualatex'

latex_documents = [
    ('index', 'DatabaseReport.tex', 'Database Report', 'Milosz Smieja', 'manual'),
]

