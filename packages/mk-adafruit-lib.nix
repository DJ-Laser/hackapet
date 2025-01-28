{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
}: let
in
  {
    pname,
    version,
    runtimeInputs,
    src ? {},
    ...
  } @ attrs: let
    rawPackage = buildPythonPackage (attrs
      // {
        inherit pname version;

        src = fetchPypi (src
          // {
            inherit pname version;
          });

        propagatedBuildInputs = [];

        pyproject =
          if attrs ? format
          then null
          else true;
        build-system = [
          setuptools-scm
          setuptools
          wheel
        ];

        dontCheckRuntimeDeps = true;
      });

    final = runtimeInputs;
  in
    {
      rawPackage = rawPackage;
      package = rawPackage;
    }
