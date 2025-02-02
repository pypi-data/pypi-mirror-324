# How the templates directory works/is used




## At build time

- MkDocs gathers all the files in the tree hierarchy that are either images, css or js files and uses those as base content for the built site directory (keeping the tree structure).
  Note that the templates content of material gathered even before that.
- The content of docs/ is then merged into the destination directory, potentially overriding files at the same final location.
- Html files may be used as templates for this or that, especially `main.html` and `base_pmt.html`


This defines the base content of the root directory of the web site. Files of the docs are then generated and added to it at the appropriated location.
Note that the files generated from `docs/` end up merged within the structure resulting from `templates/`.




## At runtime/page load time

The big question is: "what script is loaded when?".

All js scripts are systematically present on the server/built site, but their insertion/actual use in a page may  depend on how they are registered.

Here is how everything is loaded (JS + CSS contents): <br><br>



1. CSS files (see `pyodide-css/`) are __always added__ in the Jinja `libs` block, even if the related elements are not present in the page. This allows:

    - To get consistency on the end user's side, if they start to add their own overloaded rules.
    - These files are inserted before the css files coming from `mkdocs.yml:extra_css/`, so that the user _can_ overload the settings coming from the theme.

1. `templates/js-libs` scripts are __always added__ through the `libs` block, meaning, in the `<head>` of the page. Those are scripts that _have_ to be defined before the content is defined.

    This is not entirely true anymore, because most of PMT's scripts are now loaded as modules, but this still applies for some of them (mathjax, config, ...)

1. Some other CDNs and any data related to IDEs config or equivalent are loaded in the `libs` block. See `pyodide_mkdocs_theme/pyodide_macros/html_dependencies/deps.py`:
    * jQuery: always
    * pyodide, ace, jQuery terminal: __only if needed__
    * ...

    ---

1. Extra style sheets registered by the user in `mkdocs.yml:extra_css/` are loaded at the beginning of the `<body>`. They are __always added__.


1. The page content is the rendered and inserted by mkdocs.


1. `templates/js-per-pages` scripts are added at the end of the page content, __through mkdocs `on_page_context` event__ and are loaded __only if they are required in the page__.

    This reduces the amount of code/data to load, and _also_ allows to not start the pyodide environment when not needed.

    ---

1. `docs/extras/javascripts` (or so) that are registered into `mkdocs.yml:extra_javascript` are __always added__ to all rendered pages, in the Jinja `scripts` block, meaning they end up in the very end ot the `<body>`.


1. `templates/js-scripts` scripts are added to the Jinja `scripts` block, after the "mkdocs registered" scripts. They are __always loaded__.
