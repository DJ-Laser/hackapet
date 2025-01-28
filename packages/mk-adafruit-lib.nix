{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
}: let
  cleanAttrs = lib.flip.removeAttrs [
    "hash"
  ];
in
  {
    pname,
    version,
    hash,
    src ? {},
    ...
  } @ attrs: let
    rawPackage =
      buildPythonPackage (cleanAttrs attrs)
      // {
        inherit pname version;

        src = fetchPypi (src
          // {
            inherit pname version hash;
          });

        propagatedBuildInputs = [];

        pyproject = true;
        build-system = [
          setuptools-scm
          setuptools
          wheel
        ];

        dontCheckRuntimeDeps = true;
      };
  in
    rawPackage
