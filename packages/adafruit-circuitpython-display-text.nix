{
  lib,
  buildPythonPackage,
  fetchPypi,
  setuptools,
  setuptools-scm,
  wheel,
}:
buildPythonPackage rec {
  pname = "adafruit_circuitpython_display_text";
  version = "3.2.2";

  propagatedBuildInputs = [];

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-4TKrQidduvg6Z8Lo2pmNyQEE6GXurcChbg+5f702luU=";
  };

  pyproject = true;
  build-system = [
    setuptools-scm
    setuptools
    wheel
  ];

  dontCheckRuntimeDeps = true;
}
